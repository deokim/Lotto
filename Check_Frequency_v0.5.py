import numpy as np
import pandas as pd
#from openpyxl.formatting.rule import CellIsRule
from collections import Counter
from openpyxl.utils import get_column_letter
from openpyxl.styles import PatternFill, Font, Border, Side, Alignment

def process_binary_data2(df,col,occur):
    """
    원본 데이터를 불러와서 출현/미출현 상태로 이진화함 (출현: 1, 미출현: 0)
    """
    # df[column_index] == 0 은 True/False 시리즈를 반환하며, astype(int)는 이를 1/0으로 변환
    # occr==True는 target_freq가 발생한 경우, False이면 미발생한 경우
    if occur :        
        binary_series = (df.loc[:,col] >= 1).astype(int)
    else:
        binary_series = (df.loc[:,col] == 0).astype(int)

    return binary_series

def process_binary_data(df,col,exact_match,target_freq):
    """
    원본 데이터를 불러와서 출현/미출현 상태로 이진화함 (출현: 1, 미출현: 0)
    """
    # df[column_index] == 0 은 True/False 시리즈를 반환하며, astype(int)는 이를 1/0으로 변환
    # exact_match==True는 target_freq와 정확하게 일치하는 경우, False이면 발생여부만 파악
    if exact_match :        
        binary_series = (df.loc[:,col] ==target_freq).astype(int)
    else:
        binary_series = (df.loc[:,col] >= 1).astype(int)

    return binary_series

def calculate_run_length(binary_series):
    """
    이진화된 시리즈를 입력받아 각 행의 '연속된 0 또는 1의 길이'를 반환
    """
    # 변화 지점 감지 및 그룹 ID 생성
    # shift 배열을 오른쪽으로 이동
    # cumsum() :  (binary_series != binary_series.shift(1)) 이 True가 나타날 때, 누적합이 +1씩 증가
    group_id = (binary_series != binary_series.shift(1)).cumsum()
    
    # 그룹별 크기를 원본 시리즈 크기로 확장 (미사용. 각 Run Length의 동일값으로 배열을 채움)
    #run_lengths = binary_series.groupby(group_id).transform('size')

    # 각 그룹 내에서 누적 카운트(0부터 시작)를 계산합니다.
    # .cumcount()는 그룹 내에서 0, 1, 2, 3... 순서로 번호를 매깁니다.
    sequence_count_0_indexed = binary_series.groupby(group_id).cumcount()

    # 사용자의 원래 로직에 맞게 1부터 시작하도록 1을 더합니다.
    sequence_position = sequence_count_0_indexed + 1
    
    return sequence_position

def count_run_length(binary_series):
    group_id=(binary_series != binary_series.shift(1)).cumsum()
    run_sizes=binary_series.groupby(group_id).sum()

    # run length가 1이상인 경우만 반환
    return run_sizes[run_sizes>0]

# -----------------------------------------------------------
# 데이터 준비
# 컬럼 구조: ['Round', '#1', '#2', '#3', '#4', '#5', '#6', 'B'] (A열 및 C:I열)
# -----------------------------------------------------------

data_file=r"D:\Detailed Analysis 04.xlsm"
df=pd.read_excel(data_file, sheet_name="Rawdata분석", usecols="A, C:I", header=0)
final_round=len(df.index)

# 엑셀 스타일 지정
light_orange=PatternFill(start_color="FDE9D9", end_color="FDE9D9", fill_type="solid")
orange=PatternFill(start_color="F79646", end_color="F79646", fill_type="solid")
aqua=PatternFill(start_color="DAEEF3", end_color="DAEEF3", fill_type="solid")
border_thick = Side(style='thick')

try:    
    with pd.ExcelWriter(r"D:\Freq_Len.xlsx",engine='openpyxl') as writer:   
        #당첨번호 컬럼들만 선택(Round컬럼 제외), Bonus 제외 [1:7], Bonus 포함시 [1:8]        
        for i in range(7,9):
            num_cols=df.columns[1:i]        

            if len(num_cols)==7:
                sht_affix="B포함"
                cell_offset=-7
            else:
                sht_affix="B제외"
                cell_offset=-6

            # -------------------------------------------------------------------------
            # 1~45 원핫 매트릭스(One-Hot Matrix) 생성
            # (1회 ~ 최종회차) * (1~45번 숫자) 행렬에 당첨여부를 0/1로 표시
            # -------------------------------------------------------------------------
            # 전체 0으로 채워진 기본 틀을 만듭니다. (행 개수 x 45열)
            df_onehot = pd.DataFrame(0, index=df.index, columns=range(1, 46))

            # 고속 벡터화 연산: 각 당첨번호 컬럼을 순회하며 해당 번호 위치(값-1)에 1을 채웁니다.
            for col in num_cols:
                df_onehot.values[np.arange(len(df)), df[col] - 1] = 1

            # 직관적인 확인을 위해 인덱스를 'Round'로 변경합니다.
            df_onehot.index = df["Round"]

            # -------------------------------------------------------------------------
            # Rolling Window를 이용한 과거 P회차 빈도 계산 (예: period = 11이라면 이전 10회차 발생빈도로 계산)
            # -------------------------------------------------------------------------
            min_period=5
            max_period=150

            # pos_result_matrix (최종회차 발생빈도의 연속출현 기록), freq_result_matrix (빈도별 연속출현 기록)
            pos_result_matrix=[]
            pos_record_matrix=[]
            multi_pos_record_matrix=[]
            freq_result_matrix=[]
            freq_record_matrix=[]

            for period in range(min_period,max_period+1):
                # rolling(period).sum()으로 누적 합을 구하되, 
                # [수정] 1. 계산을 위해 확실하게 회차 기준 오름차순(과거 -> 최신)으로 정렬합니다.
                df_onehot_asc = df_onehot.sort_index(ascending=True)

                # 오름차순 상태에서 Rolling 과거 빈도를 계산합니다. (이제 과거 데이터가 위에 있으므로 정상 계산됩니다)
                # rolling을 사용하게 되면. window=3인 경우, 3번째 행에 누적합이 계산되기 때문에, Shift함수를 이용하여 4번째 행에 이전 3번째 합이 나오게 조정
                df_freq_asc = df_onehot_asc.rolling(window=period).sum().shift(1)                        

                # 계산이 끝난 후, 엑셀 보기 방식처럼 다시 최신 회차가 위로 오게(내림차순) 정렬
                # 다음회차 기준 빈도를 next_freq에 저장
                df_freq = df_freq_asc.sort_index(ascending=False)   
                next_freq=df_onehot.iloc[0:period,:].sum()

                # -------------------------------------------------------------------------
                # 주기별 발생빈도를 freq_buckets에 저장
                # df_freq_counts        : 기준 주기  / 회차별 / 빈도별 개수(1~45개 전체 숫자 대상)
                # df_win_freq           : 기준 주기  / 회차별 / 당첨번호별 빈도
                # df_freq_win_counts    : 기준 주기  / 회차별 / 빈도별 당첨개수
                # -------------------------------------------------------------------------
                valid_freq_matrix = df_freq.dropna()                
                min_freq=int(valid_freq_matrix.values.min())
                # max_freq = int(valid_freq_matrix.max().max())
                max_freq = int(valid_freq_matrix.values.max())
                freq_buckets = list(range(min_freq, max_freq + 1))  # 예: [0, 1, 2, 3, 4, 5, 6]
                
                df_freq_counts = pd.DataFrame(index=valid_freq_matrix.index, columns=freq_buckets)
                next_freq_counts={}                

                # 넘파이 벡터화 연산: 2차원 배열 전체를 f값과 통째로 비교한 뒤 행별(axis=1)로 합산
                for f in freq_buckets:                    
                    df_freq_counts[f] = (valid_freq_matrix.values == f).sum(axis=1)
                    next_freq_counts[f]=(next_freq.values==f).sum()                                        
                    
                # 각 빈도별 평균 개수 
                all_counts_avg = df_freq_counts.mean()  
                

                df_win_freq = pd.DataFrame(index=df_freq.index, columns=num_cols)
                #i=0
                for col in num_cols:    
                    col_index=df[col].values-1
                    df_win_freq[col]=df_freq.values[np.arange(len(df)),col_index] 

                #df_win_freq.index = df["Round"]
                df_win_freq = df_win_freq.iloc[:final_round-period+1,:]

                # df_win_freq에서 유효한 데이터만 선택
                valid_pos_freq = df_win_freq.dropna()
                df_freq_win_counts = pd.DataFrame(index=valid_pos_freq.index, columns=freq_buckets)

                freq_occur_rate=[]          # 기준 주기 / 회차별 / 빈도별 발생비율 (전체 회차에서 몇 번 발생)
                # 넘파이 벡터화 연산: 빈도값 f가 당첨번호로 몇개 등장하는지 카운트
                for f in freq_buckets:
                    df_freq_win_counts[f]=(valid_pos_freq.values == f).sum(axis=1)
                    freq_occur_rate.append( (df_freq_win_counts[f]>0).sum() / len(df_freq_win_counts) )

                # 각 빈도별 당첨번호로 출현한 평균 개수 
                freq_counts_avg = df_freq_win_counts.mean()

                # -------------------------------------------------------------------------
                # 최종회차 기준으로 특정빈도별 출현/미출현 연속여부를 계산
                # -------------------------------------------------------------------------
                binary_coding_col={}
                result_by_freq={}                            

                for f in freq_buckets:
                    result_by_freq['Period']=period                    
                    chk_record=False

                    final_freq_occur=True if df_freq_win_counts.loc[final_round,f] else False
                    temp_str=""

                    if final_freq_occur:  #최종회차, 해당빈도가 출현한 경우라면
                        binary_coding_col[f]=process_binary_data2(df_freq_win_counts,f,True)
                        temp_str='출'
                    else:
                        binary_coding_col[f]=process_binary_data2(df_freq_win_counts,f,False)
                        temp_str="미"
                    freq_final_rec=((calculate_run_length(binary_coding_col[f])*binary_coding_col[f])==0).argmax(axis=0)
                    result_by_freq[str(f)+'-현재']=str(freq_final_rec) + temp_str
                    
                    # 특정빈도 연속 출현
                    binary_coding_col[f]=process_binary_data2(df_freq_win_counts,f,True)
                    freq_hits=count_run_length(binary_coding_col[f])
                    freq_max_hits=np.max(freq_hits)
                    # freq_max_hits=np.max(calculate_run_length(binary_coding_col[f])*binary_coding_col[f])
                    result_by_freq[str(f)+'-M출']=freq_max_hits

                    # 특정빈도 연속 미출
                    binary_coding_col[f]=process_binary_data2(df_freq_win_counts,f,False)
                    freq_misses=count_run_length(binary_coding_col[f])
                    freq_max_misses=np.max(freq_misses)
                    # freq_max_misses=np.max(calculate_run_length(binary_coding_col[f])*binary_coding_col[f])
                    result_by_freq[str(f)+'-M미']=freq_max_misses

                    # -------------------------------------------------------------------------
                    # 현재 기록이 Max기록에 근접했을 경우 별도 기록 저장
                    # -------------------------------------------------------------------------
                    if next_freq_counts[f]:
                        if final_freq_occur and freq_max_hits - freq_final_rec <= 1:
                            chk_record=True
                        elif not final_freq_occur and freq_max_misses - freq_final_rec <= 1:
                            chk_record=True
                    
                    if chk_record:
                        record_by_freq={}  
                        record_by_freq['Period']=period
                        record_by_freq['Frq-Range']=f'{min_freq} ~ {max_freq}'
                        record_by_freq['Cur-Range']=f'{np.min(next_freq)} ~ {np.max(next_freq)}'
                        record_by_freq['Freq']=f
                        record_by_freq['Frq-Avg']=freq_counts_avg[f]
                        record_by_freq['Frq-occ_rate']=freq_occur_rate[f-min_freq]
                        record_by_freq['Cur_status']=str(freq_final_rec) + temp_str
                        record_by_freq['Cur_Cnt']=next_freq_counts[f]
                        pool_numbers=next_freq[next_freq == f].index.tolist()
                        pool_str = ",".join(map(str, pool_numbers))   
                        record_by_freq['Pool']=pool_str

                        if final_freq_occur:
                            count_run=dict(sorted(Counter(freq_hits).items(),reverse=True))
                            pos_rec_str = ",  ".join([f"{k}:{v}" for k, v in count_run.items()])
                            record_by_freq['Rec'] =pos_rec_str
                        else:
                            count_run=dict(sorted(Counter(freq_misses).items(),reverse=True))
                            pos_rec_str = ",  ".join([f"{k}:{v}" for k, v in count_run.items()])
                            record_by_freq['Rec'] = pos_rec_str

                        freq_record_matrix.append(record_by_freq)                   

                freq_result_matrix.append(result_by_freq)
                
                # -------------------------------------------------------------------------
                #최종회차(final_round)발생빈도를 기준으로 특정자리별 / 특정빈도가 얼마나 연속으로 출현하고 있는 지 확인
                # -------------------------------------------------------------------------
                binary_coding_col={}
                result_by_final_win={}            
                
                for col in num_cols:
                    binary_coding_col[col]=process_binary_data(df_win_freq,col,True,df_win_freq.loc[final_round,col])
                    result_by_final_win[col]=calculate_run_length(binary_coding_col[col])*binary_coding_col[col]

                stats_df=pd.DataFrame(result_by_final_win)                    

                #cur_consecutive_len=[]
                # result_by_period={}
                # for col in num_cols:
                #     cur_consecutive_series=pd.Series(range(final_round,period-1,-1),index=df_win_freq.index)
                #     #cur_consecutive_len.append(final_round-np.max((stats_df.loc[:,col]==0)*cur_consecutive_series))
                #     len_by_column=final_round-np.max((stats_df.loc[:,col]==0)*cur_consecutive_series)
                #     result_by_period['Period']=period
                #     result_by_period[col+"frq"]=int(df_win_freq.loc[final_round,col])
                #     result_by_period[col + '-len']=len_by_column

                # (stats_df.values == 0)는 0과 1로 구성된 배열
                # 역순(최신회차 -> 과거회차)으로 내려가면서 처음으로 True(1)가 되는 위치(인덱스)를 찾습니다.                
                # 넘파이의 argmax(axis=0)는 최대값의 인덱스 반환. 최대값이 여러개일 경우 처음 만나는 위치 반환                
                consecutive_lenghs=(stats_df.values == 0).argmax(axis=0)

                #pos_record_matrix.: 특정기준(3주?) 이상 연속출현한 자리/자리의 빈도/이전 출현기록
                result_by_period = {'Period-'+str(final_round): period}

                # 최종(적용) 당첨번호 빈도의 연속출현기록을 코드화 [1xx-x2x]
                consecutive_pos_cnt = (consecutive_lenghs[0:5+1]>=2).sum()
                if consecutive_pos_cnt >=1:
                    # freq_pos_code_str=f'{consecutive_pos_cnt} ['
                    # for i, pos in enumerate(consecutive_lenghs[0:5+1]):
                    #     pos_freq=str(int(df_win_freq.iloc[1, i]))
                    #     if i==3:
                    #         freq_pos_code_str+="-"                        
                    #     if pos >=2:                                             
                    #         # freq_pos_code_str+="{:g}".format(pos_freq)
                    #         freq_pos_code_str+=pos_freq
                    #     else:
                    #         freq_pos_code_str+='x'
                    # freq_pos_code_str += "]"
                    freq_pos_code_arr=np.where(consecutive_lenghs[0:5+1]>=2, df_win_freq.iloc[1,:5+1].astype(int).astype(str), "x")
                    freq_pos_code_str=f"{consecutive_pos_cnt} [{''.join(freq_pos_code_arr[:3])}-{''.join(freq_pos_code_arr[3:])}  ]"
                else:
                    freq_pos_code_str='-'
                result_by_period['2연속 이상개수']=freq_pos_code_str

                for i, col in enumerate(num_cols):
                    result_by_period[col+"-frq"] = int(df_win_freq.loc[final_round, col])

                # -------------------------------------------------------------------------
                # 특정 자리/최종회차 출현 빈도가 일정기준 이상 연속출현했을 경우, 해당 기록을 추출
                # 추출기준  1) 해당자리 연속출현 2회 & 출현빈도의 평균발생 1 미만,  2) 해당 자리 & 연속출현이 3회 이상일 경우
                for i, col in enumerate(num_cols):                    
                    result_by_period[col+'-len'] = int(consecutive_lenghs[i])    # 다른 자료이지만, 예전 코드에 덧붙여 써서 유지됨
                    found_in_period = False
                    target_freq=int(df_win_freq.loc[final_round, col])
                    if consecutive_lenghs[i] ==2 and freq_counts_avg[target_freq] < 1:
                        found_in_period = True
                    elif consecutive_lenghs[i] >=3:
                        found_in_period = True
                    
                    if found_in_period:                    
                        #해당 자리 & 빈도의 기네스기록 계산 및 저장
                        ref_rec_str = f'{target_freq}빈도- '
                        for j, col2 in enumerate(num_cols):
                            if j==6: continue   # 보너스자리인 경우 제외, j=0에서 시작함
                            binary_coding_col[col2]=process_binary_data(df_win_freq,col2,True,target_freq)
                            exact_runs=count_run_length(binary_coding_col[col2])
                            count_run=dict(sorted(Counter(exact_runs).items(),reverse=True))
                            pos_rec_str = ",  ".join([f"{k}:{v}" for k, v in count_run.items()])
                            ref_rec_str += f'#{j+1} {pos_rec_str}  //  '                                
                            if col==col2:   # 해당자리기록
                                rec_str = pos_rec_str                                

                        #해당빈도에 속하는 숫자 저장..다음회차여야 함. 
                        pool_numbers=next_freq[next_freq == target_freq].index.tolist()
                        pool_str = ",".join(map(str, pool_numbers))                

                        pos_record_matrix.append({
                            'Period' : period,
                            '#' : i+1,
                            'Frq' : target_freq,
                            'Frq-Avg' : freq_counts_avg[target_freq],
                            'Frq-Occ_rate' : freq_occur_rate[target_freq-min_freq],
                            'Len' : int(consecutive_lenghs[i]),
                            'Rec' : rec_str,
                            'Pool' : pool_str,
                            'Ref' : ref_rec_str,
                        })

                # 만약 해당 Period에 3회 이상 출현 자리가 하나도 없었다면? (Period 행 유지용)
                if not found_in_period:
                    pass

                # 참고목적으로 빈도별 평균출현 횟수 추가
                for i in freq_buckets:
                    result_by_period[i]=freq_counts_avg[i]
                pos_result_matrix.append(result_by_period)            

                # -------------------------------------------------------------------------
                # 2연속 이상 출현한 빈도/자리가 2개 이상일 경우
                if consecutive_pos_cnt >=2:                    
                    multi_pos=[]
                    multi_pos_consecutive=np.ones(len(stats_df.index))
                    target_freqs=set()
                    pool_strs=""
                    for i, pos in enumerate(consecutive_lenghs[0:5+1]):
                        if pos>=2:
                            multi_pos_consecutive *= stats_df.iloc[:,i]
                            multi_pos.append(i+1)
                            target_freq=int(df_win_freq.iloc[1, i])
                            target_freqs.add(target_freq)
                            pool_numbers=next_freq[next_freq == target_freq].index.tolist()
                            pool_str = f"#{i+1} : " + ",".join(map(str, pool_numbers))
                            pool_strs = pool_strs + pool_str + " // "
                    
                    # multi_pos_len_code_str = str(consecutive_lenghs.tolist()).replace('1','x')
                    # multi_pos_len_code_str = [str(x).replace('1','x') for x in consecutive_lenghs.tolist()]
                    multi_pos_len_code_str = consecutive_lenghs.astype(str)
                    multi_pos_len_code_str[multi_pos_len_code_str=='1'] = 'x'
                    multi_pos_str=" * ".join(f'#{i}'for i in multi_pos)
                    multi_pos_freq_avg_str = ", ".join([f"{i}빈도 : {freq_counts_avg[i]:.2f}" for i in target_freqs])
                    multi_pos_consecutive_length = (multi_pos_consecutive >0).astype(int)
                    exact_runs=count_run_length(multi_pos_consecutive_length)
                    count_run=dict(sorted(Counter(exact_runs).items(),reverse=True))
                    pos_rec_str = ",  ".join([f"{k}:{v}" for k, v in count_run.items()])

                    multi_pos_record_matrix.append( {
                        'Period': period,
                        'Code' : freq_pos_code_str,
                        'Pos_len' : f"{''.join(multi_pos_len_code_str[:2+1])} - {''.join(multi_pos_len_code_str[3:5+1])}",
                        '#' : multi_pos_str,
                        'Freq-Avg' : multi_pos_freq_avg_str,                        
                        'Cur_Rec': np.min(consecutive_lenghs[consecutive_lenghs>=2]),
                        'Rec': pos_rec_str,
                        'Pool' : pool_strs
                    })

            stats_pos_df=pd.DataFrame(pos_result_matrix)   
            record_pos_df=pd.DataFrame(pos_record_matrix)
            record_multi_pos_df=pd.DataFrame(multi_pos_record_matrix)
            stats_freq_df=pd.DataFrame(freq_result_matrix)     
            record_freq_df=pd.DataFrame(freq_record_matrix)     

            # -------------------------------------------------------------------------
            # 엑셀 시트 기본 스타일 지정 (폰트, 헤더, 틀고정 등)
            # -------------------------------------------------------------------------
            def basic_sht_Style(worksheet):
                    # font 및 Size 지정
                    for col in range(1,worksheet.max_column+1):                    
                        for row in range(1,worksheet.max_row+1):
                            if col==1 or row==1:
                                worksheet.cell(row=row, column=col).font=Font(name='나눔고딕', size=8, bold=True)
                            else:
                                worksheet.cell(row=row, column=col).font=Font(name='나눔고딕', size=8)        
                        if col==1: continue
                        worksheet.column_dimensions[get_column_letter(col)].width=4.7          # 4.7 * 10 = 47 픽셀로 엑셀에 적용됨
                    # 헤더행 서식 지정
                    worksheet.row_dimensions[1].height=35.0
                    for cell in worksheet[1]:
                        cell.alignment = Alignment(wrap_text=True,vertical='top')                    
                    # Freeze Pane 적용
                    worksheet.freeze_panes='B2'                    
                    return worksheet
            
            # -------------------------------------------------------------------------
            # 최종회차 당첨번호 빈도기준 연속출현 시트 생성
            stats_pos_df.to_excel(writer, sheet_name=f"{sht_affix}_최종회차빈도", index=False)
            worksheet=writer.sheets[f"{sht_affix}_최종회차빈도"]
            style_sht=basic_sht_Style(worksheet)
                        
            if len(num_cols)==6:
                first_indent=9
                second_indent=15
                target_idxs=range(first_indent,first_indent+6)
            else:            
                first_indent=10
                second_indent=17
                target_idxs=range(first_indent,first_indent+6)

            worksheet.column_dimensions['B'].width=11
            for cell in style_sht['B']:
                cell.number_format='0;-0;-'
            for cell in style_sht['C']:
                cell.border=Border(left=border_thick)                

            # 현재 자리별 빈도 2연속 이상 출현 시 별도색으로 표시
            for col_idx in target_idxs:            
                for cell in style_sht[get_column_letter(col_idx)]:
                    if col_idx==first_indent:
                        cell.border=Border(left=border_thick)
                    if cell.row==1: continue                
                    if cell.value is not None and cell.value ==2:
                        cell.fill=light_orange
                        cell.offset(0,cell_offset).fill=light_orange
                    elif cell.value is not None and cell.value >=3:
                        cell.fill=orange
                        cell.offset(0,cell_offset).fill=orange
                        style_sht.cell(row=cell.row, column=second_indent+cell.offset(0,cell_offset).value).fill=orange
            
            # 2연속 이상 출현 빈도 경계선 및 별도 숫자 서식 지정
            target_idxs=range(second_indent,style_sht.max_column+1)
                        
            for col_idx in target_idxs:            
                for cell in style_sht[get_column_letter(col_idx)]:
                    if col_idx==second_indent:
                        cell.border=Border(left=border_thick)
                    if cell.row == 1 : continue
                    cell.number_format='0.00'

            # -------------------------------------------------------------------------
            # 복수 자리별 연속출현 기록 시트 
            record_multi_pos_df.to_excel(writer, sheet_name=f"{sht_affix}_복수자리기록",index=False)
            worksheet=writer.sheets[f"{sht_affix}_복수자리기록"]
            style_sht=basic_sht_Style(worksheet)

            style_sht.column_dimensions['B'].width=11            
            style_sht.column_dimensions['C'].width=11            

            # -------------------------------------------------------------------------
            # 자리별 연속출현 기록 시트 
            record_pos_df.sort_values(by=['#','Period'],inplace=True)
            record_pos_df.to_excel(writer,sheet_name=f"{sht_affix}_자리기록",index=False)
            worksheet=writer.sheets[f"{sht_affix}_자리기록"]
            style_sht=basic_sht_Style(worksheet)

            for col_idx in [4,5]:
                for cell in style_sht[get_column_letter(col_idx)]:
                    if cell.row ==1:
                        continue
                    cell.number_format='0.00'

            for cell in style_sht['F']:
                if cell.row ==1:
                    continue
                if cell.value >= 3:
                    cell.fill=orange

            # 자리 별 경계선(Border)서식 지정
            target_idxs=range(1,style_sht.max_column+1)
            for col_idx in target_idxs:            
                max_len=0
                for cell in style_sht[get_column_letter(col_idx)]:
                    if style_sht.cell(row=cell.row, column=2).value != style_sht.cell(row=cell.row+1, column=2).value:
                        cell.border=Border(bottom=border_thick)

                    # Autofit 서식지정                    
                    if cell.value is not None and cell.column >=6:
                        val_str=str(cell.value)
                        # 한글 등 멀티바이트 문자는 길이를 2로 계산하는 로직
                        byte_len = sum(2 if ord(char) > 127 else 1 for char in val_str)
                        if byte_len > max_len:
                            max_len=byte_len
                max_len=max_len * 7/11
                style_sht.column_dimensions[get_column_letter(col_idx)].width=max(max_len, 6)

            # -------------------------------------------------------------------------
            # 빈도기준 연속출현 시트 생성
            stats_freq_df.to_excel(writer,sheet_name=f"{sht_affix}_빈도별", index=False)
            worksheet=writer.sheets[f"{sht_affix}_빈도별"]
            style_sht=basic_sht_Style(worksheet)

            target_idxs=range(2, style_sht.max_column+1,3)
            for col_idx in target_idxs:
                for cell in style_sht[get_column_letter(col_idx)]:
                    # print(cell)
                    if cell.row==1 : continue
                    if cell.value is not None and len(str(cell.value)):                       
                        if str(cell.value)[len(str(cell.value))-1]=="미":
                            if int(float(cell.offset(0,2).value))-int(str(cell.value)[:len(cell.value)-1]) <=1:
                                cell.fill=aqua
                                cell.offset(0,2).fill=aqua
                                style_sht.cell(row=cell.row, column=1).fill=orange
                        else:
                            if int(float(cell.offset(0,1).value))-int(str(cell.value)[:len(cell.value)-1]) <=1:
                                cell.fill=light_orange
                                cell.offset(0,1).fill=light_orange
                                style_sht.cell(row=cell.row, column=1).fill=orange

            # -------------------------------------------------------------------------
            # 빈도기준 연속출현 기록 시트 생성
            record_freq_df.to_excel(writer,sheet_name=f"{sht_affix}_빈도별기록", index=False)
            worksheet=writer.sheets[f"{sht_affix}_빈도별기록"]
            style_sht=basic_sht_Style(worksheet)

            for col_idx in [5,6]:
                for cell in style_sht[get_column_letter(col_idx)]:
                    if cell.row ==1: continue
                    cell.number_format='0.00'

            for cell in style_sht['G']:
                if str(cell.value)[len(cell.value)-1]=="출":
                    cell.fill=light_orange                        
            
            print(f"✅ {final_round}회차 빈도별 계산 - 데이터파일 {data_file}")
            print("최소 계산주기: "+str(min_period), "     최대 계산주기 : "+str(max_period))        
            print(f"{sht_affix} 빈도별 계산 및 시트 생성")            
except PermissionError:
    # 파일이 열려 있어서 쓰기 권한이 없을 때 발생하는 에러 포착
    print("❌ 파일 생성 실패: 'Freq_Len.xlsx' 파일이 현재 열려 있습니다.")
    print("⚠️ 엑셀 파일을 닫은 후 다시 실행해 주세요.")
except Exception as e:
    print(f"예기치않은 오류 발생 {e}")