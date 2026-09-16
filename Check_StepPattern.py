import pandas as pd

def find_stairstep_patterns(df, min_len=3, max_period=5):
    """
    df: 로또 데이터프레임
    min_len: 최소 연속 횟수 (예: 3회 이상 이어져야 패턴으로 인정)
    max_period: 검색할 주기 (1회 차이, 2회 차이... 5회 차이까지 검색)
    """
    
    patterns = []
    
    # 데이터프레임의 값을 쉽게 조회하기 위해 리스트 형태로 변환 (속도 향상)
    # 각 회차별 번호 집합을 딕셔너리로 만듦: {1187: {5, 13, 26...}, 1188: ...}
    # for _, row  index값을 사용하지 않기 때문에 관례적으로 _ 를 사용하여 이 변수는 무시한다는 것을 표기
    rounds_data = {row['Round']: set(row[['#1','#2','#3','#4','#5','#6',"B"]].values) for _, row in df.iterrows()}    
    round_list = df['Round'].tolist()
    
    # 1) 등차수열 찾기 (Step이 고정: +7, +7, +7...)
    print("🔍 등차수열(일정 간격) 패턴 검색 중...")
    
    for period in range(1, max_period + 1): # 주기 반복 (1주기, 2주기...)
        for i, start_round in enumerate(round_list):
            # 검색 범위를 벗어나면 중단
            if i + (min_len - 1) * period >= len(round_list):
                break
                
            start_nums = rounds_data[start_round]
            
            # 현재 회차의 각 번호에 대해 시작점 테스트
            for start_num in start_nums:
                # 다음 주기의 회차에 있는 모든 번호와 비교하여 'Step' 후보를 찾음
                next_round = round_list[i + period]
                next_nums = rounds_data[next_round]
                
                for next_num in next_nums:
                    step = next_num - start_num
                    # Step이 0인 경우(같은 번호 연속)도 포함할지 결정 (여기선 포함)
                    
                    # 패턴 추적 시작
                    current_seq = [start_num, next_num]
                    current_r_idx = i + period
                    
                    while True:
                        next_r_idx = current_r_idx + period
                        if next_r_idx >= len(round_list):
                            break
                        
                        expected_num = current_seq[-1] + step
                        target_round = round_list[next_r_idx]
                        
                        if expected_num in rounds_data[target_round]:
                            current_seq.append(expected_num)
                            current_r_idx = next_r_idx
                        else:
                            break
                    
                    # 최소 길이 이상이면 저장
                    if len(current_seq) >= min_len:
                        convert_seq=[int(num) for num in current_seq]
                        is_end="Y" if start_round + len(current_seq)*period <= final_round else "N"
                        patterns.append({
                            'Type': '등차수열',
                            'Period': period,
                            'Start_Round': start_round,
                            'Length': len(current_seq),
                            'Sequence': convert_seq,
                            'Step': step,
                            'Acc': 0,
                            'Is_End': is_end,
                        })

    # 2) 계차수열 찾기 (Step이 일정하게 증가: +1, +2, +3...)
    print("🔍 계차수열(간격 증가/감소) 패턴 검색 중...")
    
    for period in range(1, max_period + 1):
        for i, start_round in enumerate(round_list):
            # 최소 3개는 있어야 가속도(Step의 변화)를 알 수 있음
            if i + 2 * period >= len(round_list):
                break
            
            start_nums = rounds_data[start_round]
            
            for n1 in start_nums:
                # 두 번째 숫자 찾기
                r2 = round_list[i + period]
                for n2 in rounds_data[r2]:
                    diff1 = n2 - n1 # 첫 번째 간격
                    
                    # 세 번째 숫자 찾기
                    r3 = round_list[i + 2 * period]
                    for n3 in rounds_data[r3]:
                        diff2 = n3 - n2 # 두 번째 간격
                        
                        acc = diff2 - diff1 # 간격의 변화량 (가속도)
                        
                        # 가속도가 0이면 등차수열이므로 제외 (위에서 이미 찾음)
                        # |가속도| * 길이(최소 반복 길이)가 최초 step보다 크면 가속방향의 역전이기 때문에 제외 
                        if acc == 0 or ( acc*diff1<=0 and abs(acc)*min_len>diff1):
                            continue
                            
                        # 패턴 추적 시작
                        current_seq = [n1, n2, n3]
                        current_diff = diff2
                        current_r_idx = i + 2 * period
                        
                        while True:
                            next_r_idx = current_r_idx + period
                            if next_r_idx >= len(round_list):
                                break
                            
                            expected_diff = current_diff + acc
                            expected_num = current_seq[-1] + expected_diff
                            
                            # 번호 범위를 벗어나면 중단 (1~45)
                            if not (1 <= expected_num <= 45):
                                break
                                
                            target_round = round_list[next_r_idx]
                            if expected_num in rounds_data[target_round]:
                                current_seq.append(expected_num)
                                current_diff = expected_diff
                                current_r_idx = next_r_idx
                            else:
                                break
                        
                        # 최소 길이(여기선 3) 이상이면 저장
                        if len(current_seq) >= min_len:
                            # 중복 제거를 위한 키 생성 (간단하게 문자열로)
                            convert_seq=[int(num) for num in current_seq]
                            is_end="Y" if start_round + len(current_seq)*period <= final_round else "N"
                            patterns.append({
                                'Type': '계차수열',
                                'Period': period,
                                'Start_Round': start_round,
                                'Length': len(current_seq),
                                'Sequence': convert_seq,
                                'Step': diff1,
                                'Acc':acc,
                                'Is_End': is_end,
                            })

    return pd.DataFrame(patterns)

def remove_subset_patterns(df):
    """
    찾은 패턴들 중, 더 긴 패턴 안에 완전히 포함되는 짧은 패턴(부분 집합)을 제거합니다.
    """
    if df.empty:
        return df

    # 1. 계산 편의를 위해 'End_Round'(끝나는 회차) 컬럼을 임시로 만듭니다.
    # 끝나는 회차 = 시작회차 + (길이 - 1) * 주기
    df['End_Round'] = df['Start_Round'] + (df['Length'] - 1) * df['Period']        
    
    # 2. 가장 긴 패턴부터 처리하기 위해 정렬합니다. (길이 내림차순)
    # 길이가 같다면 시작 회차가 빠른 순서로 정렬
    df = df.sort_values(by=['Length', 'Start_Round'], ascending=[False, True])

    final_patterns = []
    
    # 3. 같은 종류(Type), 같은 주기(Period), 같은 간격(Step)끼리 그룹을 묶어 비교합니다.
    # 예: "등차수열, 주기 12, Step 0" 인 애들끼리만 비교해야 함
    grouped = df.groupby(['Type', 'Period', 'Step', 'Acc'])

    for _, group in grouped:
        # 이 그룹 내에서 이미 등록된 '형님 패턴'들의 범위를 저장할 리스트
        accepted_ranges = [] 

        for _, row in group.iterrows():
            current_start = row['Start_Round']
            current_end = row['End_Round']
            
            is_subset = False
            
            # 이미 등록된 패턴들(더 긴 패턴들) 안에 내가 포함되는지 검사
            for (acc_start, acc_end) in accepted_ranges:
                # 내 시작점이 형님 시작점보다 같거나 뒤에 있고(>=)
                # 내 끝점이 형님 끝점보다 같거나 앞에 있으면(<=)
                # 나는 형님의 부분 집합이다!
                if current_start >= acc_start and current_end <= acc_end:
                    is_subset = True
                    break
            
            # 부분 집합이 아니면(새로운 패턴이면) 등록
            if not is_subset:
                final_patterns.append(row)
                accepted_ranges.append((current_start, current_end))

    # 4. 결과 정리
    clean_df = pd.DataFrame(final_patterns)
    # 임시로 만든 End_Round 컬럼 제거 및 다시 정렬
    if not clean_df.empty:
        # clean_df = clean_df.drop(columns=['End_Round'])
        clean_df = clean_df.sort_values(by=['Length', 'Period'], ascending=[False, True]).reset_index(drop=True)
    
    return clean_df

# -----------------------------------------------------------
# 데이터 준비
# -----------------------------------------------------------
df=pd.read_excel(r"D:\Detailed Analysis 04.xlsm", sheet_name="Rawdata분석", usecols="A, C:I", header=0)

final_round=len(df.index)
# final_round=1201

#정렬 과정에서 기존 인덱스를 버리고 **새로운 인덱스(0, 1, 2, ...)**를 생성. (drop=True): 기존의 인덱스(index 열)를 새로운 컬럼으로 저장하지 않고 삭제
df = df.sort_values('Round').reset_index(drop=True) # 회차 오름차순 정렬
df=df.iloc[:final_round]


# 최소 3개 이상 연속, 주기(텀)는 1~3회차까지 검색
iteration_len=3
iteration_period=10
result_df = find_stairstep_patterns(df, iteration_len, iteration_period)

# 기존에 찾은 result_df를 넣어서 정제합니다.
clean_result_df = remove_subset_patterns(result_df)

# 중복 제거 (알고리즘 특성상 부분 집합이 나올 수 있음)
if not clean_result_df.empty:
    clean_result_df = clean_result_df.drop_duplicates(subset=['Start_Round', 'Period', 'Type', 'Step', 'Acc'])
    # 최근회차부터, 주기가 짧은 순서대로 정렬
    clean_result_df = clean_result_df.sort_values(by=['End_Round','Period'], ascending=[False, True])
    # 적용가능한 회차만 선택
    clean_result_df=clean_result_df.loc[clean_result_df['Is_End']=="N",:].copy().reset_index(drop=True)
    # clean_result_df = clean_result_df[clean_result_df['Is_End']=="N"].copy().reset_index(drop=True)
    clean_result_df['Target_Round'] = clean_result_df['Start_Round'] + (clean_result_df['Length'] ) * clean_result_df['Period']  

    #[성능 개선] Target_Number 벡터화 연산 계산
    # 수열 공식: a_n = a_0 + (n * d1) + (n * (n-1) / 2 * d2)
    # 여기서 n = Length (0-indexed가 아니라 개수이므로 다음 항은 Length 인덱스와 같음)
    # Sequence 컬럼의 첫 번째 요소(Start Num)를 가져오기 위해 .str[0] 사용
    # Series의 요소가 리스트나 튜플, 딕셔너리 같은 복합 자료형일 때는 .str 속성을 사용하여 접근 가능
    start_nums = clean_result_df['Sequence'].str[0]
    lengths = clean_result_df['Length']
    clean_result_df['Target_Number'] = (
          start_nums +  
         (clean_result_df['Step'] *lengths) + 
         ((lengths - 1) * lengths * clean_result_df['Acc'] / 2)  )

    clean_result_df = clean_result_df[
              (clean_result_df['Target_Number'] >= 1) & (clean_result_df['Target_Number'] <= 45) ].copy()
    clean_result_df = clean_result_df[clean_result_df['Target_Round']==final_round+1]
    
    # print("\n--- 🎯 발견된 패턴 목록 ---")
    # 보기 좋게 출력
    # for _, row in result_df.iterrows():
    #     print(f"[{row['Type']}] 주기: {row['Period']}회 | 시작회차: {row['Start_Round']} | 길이: {row['Length']}")
    #     print(f"   👉 수열: {row['Sequence']}")
    #     print(f"   👉 내용: {row['Step_Info']}")
    #     print("-" * 50)
    print(f"👉 최소반복횟수: {iteration_len}")
    print(f"👉 최대반복회차: {iteration_period}")
    print(f"🎯Total patterns found : {len(clean_result_df.index)}")    
    
    
    with pd.ExcelWriter(r"D:\Step_Pattern.xlsx",engine='xlsxwriter') as writer:
        workbook=writer.book
        clean_result_df.to_excel(writer, sheet_name='step_pattern')
        worksheet=writer.sheets['step_pattern']      
        worksheet.freeze_panes('B2')

        cell_format = workbook.add_format({'font_name':'나눔고딕','font_size':8})
        worksheet.set_column('A:L',None,cell_format)
        worksheet.autofit()        
        worksheet.autofilter(0,0,len(clean_result_df.index),11)

        df = df.sort_values('Round',ascending=False)
        df.to_excel(writer,sheet_name='raw_data',index=False)
        worksheet=writer.sheets['raw_data']      
        worksheet.freeze_panes('B2')
        cell_format = workbook.add_format({'font_name':'나눔고딕','font_size':8})
        worksheet.set_column('A:L',None,cell_format)

    # # 다음 회차(예: 1202회)를 가리키는 패턴들만 추출
    # next_round_patterns = clean_result_df[clean_result_df['Target_Round'] == 1202]
    # # 번호별 카운트
    # prediction_counts = next_round_patterns['Target_Number'].value_counts().sort_index()
    # print(prediction_counts)
else:
    print("조건에 맞는 패턴을 찾지 못했습니다.")