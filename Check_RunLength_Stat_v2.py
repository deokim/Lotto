import pandas as pd
import numpy as np
from itertools import combinations
from collections import Counter

def excel_col_to_index(col_name):
    """엑셀 열 알파벳 이름(예: 'R')을 0부터 시작하는 인덱스로 변환합니다."""
        # 열 이름은 대문자로 변환하여 처리합니다.
    col_name = col_name.upper()
    index = 0
    
    # 26진수 원리를 이용한 계산
    for char in col_name:
        # A=1, B=2 ... Z=26에 해당하도록 아스키 코드 값을 이용해 변환합니다.
        # ord('A')는 65이므로, ord('A')-64를 하면 A=1이 됩니다.
        index = index * 26 + (ord(char) - ord('A') + 1)
        
    # Pandas/Python 인덱스는 0부터 시작하므로 -1을 해줍니다.
    return index - 1

def get_col_range_indices(start_col, end_col):        
    start_index = excel_col_to_index(start_col)
    end_index = excel_col_to_index(end_col)
    
    # range() 함수를 사용해 시작 인덱스부터 끝 인덱스까지 리스트를 만듭니다.
    # range(시작, 끝+1)
    return list(range(start_index, end_index + 1))

def process_binary_data(df,column_index,occurrence,min_occur=1):
    """
    원본 데이터를 불러와서 출현/미출현 상태로 이진화함 (출현: 1, 미출현: 0)
    """
    # df[column_index] > 0 은 True/False 시리즈를 반환하며, astype(int)는 이를 1/0으로 변환
    # 연속출현일 경우, occurrence=True, 연속미출현일 경우 occurrence=False로 지정
    if occurrence :
        binary_series = (df.iloc[:,column_index] >=min_occur).astype(int)
    else:
        binary_series = (df.iloc[:,column_index] == 0).astype(int)

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

    # 3. 사용자의 원래 로직에 맞게 1부터 시작하도록 1을 더합니다.
    sequence_position = sequence_count_0_indexed + 1
    
    return sequence_position

# 파일 경로 문자열 앞에 붙이는 r은 **Raw String (날 문자열)**을 의미하며, 이는 파이썬에서 이스케이프 시퀀스(Escape Sequence) 해석을 방지
# "C:\users\new"인 경우 \n 을 줄바꿈으로 인식하지 않도록 함
file_name=r"D:\Detailed Analysis 04.xlsm"

data_area={
    'interval_15': {'sht_name':'15구간분석', 'cols':'C:Q' },
    'interval_09': {'sht_name':'9구간,십단위분석', 'cols':'D:L'},
    'interval_05': {'sht_name':'5구간분석', 'cols':'C:G'},
    'mod_15' : {'sht_name':'Mod_X분석', 'cols':'BT:CH' },
    'mod_09' :{'sht_name':'Mod_X분석', 'cols':'AK:AS' },
    'last_digit':{'sht_name':'끝수분석', 'cols':'C:L'},
    'slit_col':{'sht_name':'용지행렬분석', 'cols':'Y:AE'},
}

# 전체 데이터 크기 강제지정(=최종라운드)
df_index=pd.read_excel(file_name, sheet_name='Rawdata분석', usecols="A",header=0)
final_round=len(df_index.index)

#해당 데이터가 존재하는 sheet명과 컬럼열 세팅
data_type='mod_09'
sht_name=data_area[data_type]['sht_name']
cols=data_area[data_type]['cols']
# target_indices=get_col_range_indices("BU", "CR")

df=pd.read_excel(file_name, sheet_name=sht_name, usecols=cols,header=0)
column_length=len(df.columns)
df=df[:final_round-1]

new_columns=range(0, column_length)
df.columns=new_columns

# 연속출현 = True, 미출현 = False
occurrence=False
min_occur=1
# N = 전체개수 중 뽑을 개수
N=2
counters=0
stat_result_run={}
total_max_run=[]

for combo in combinations(range(1, column_length+1),N):
    counters+=1
    #처리할 열
    binary_coding_col=[]
    result_by_column={}
    count=0
    for target in list(combo):
        binary_coding_col.append(process_binary_data(df, target-1, occurrence,min_occur))    
        result_by_column[target-1]=calculate_run_length(binary_coding_col[count])*binary_coding_col[count]
        count+=1

    stats_df=pd.DataFrame(result_by_column)

    min_values=np.min(stats_df[stats_df.columns].values, axis=1)
    stats_df['min_values']=min_values
    # stats_df.to_excel("intemediate_result.xlsx")    

    count_run=Counter(min_values)
    if 0 in count_run:
        del count_run[0]
    if not count_run:
         continue

    #각 결과에 대한 최대길이를 저장
    max_run=max(count_run.keys())
    total_max_run.append(int(max_run))

    result_run={}

    for run in range(max_run, 1-1, -1):
        # 'run+1'의 카운트를 안전하게 가져오기 위해 .get(run+1, 0) 사용
        # 키가 없으면 0을 반환하여 KeyError 방지
        next_run=count_run.get(run+1, 0)
        currnt_run=count_run.get(run,0)    
        #차분계산
        result_run[run]=currnt_run - next_run

    # combo를 키(예: 'Col1-Col3')로, 차분계산식을 값으로 저장    
    if occurrence:
        key="-".join(map(str,combo)) + "出"
    else:
        key="-".join(map(str,combo)) + "未"
    stat_result_run[key]=result_run

# final_stats_df=pd.DataFrame.from_dict(stat_result_run)
final_stats_df=pd.DataFrame(stat_result_run)
final_stats_df=final_stats_df.sort_index(ascending=True)
final_stats_df=final_stats_df.T
final_stats_df['max']=total_max_run
# print(final_stats_df)

try:
    final_stats_df.to_excel(r"D:\Run_Len.xlsx", index=True, index_label='occur:'+str(min_occur), sheet_name=data_type)
    print("✅ 조합별 최대런 계산 완료 및 파일 저장.")
    print("Data type: "+str(data_type), "     min_occur : "+str(min_occur))
    print("total combination: ", counters)
    print(final_stats_df['max'].value_counts().sort_index())
except PermissionError:
    # 파일이 열려 있어서 쓰기 권한이 없을 때 발생하는 에러 포착
    print("❌ 파일 저장 실패: '조합별_Run_통계_결과.xlsx' 파일이 현재 열려 있습니다.")
    print("⚠️ 엑셀 파일을 닫은 후 다시 실행해 주세요.")
except Exception as e:
    print(f"예기치않은 오류 발생 {e}")

