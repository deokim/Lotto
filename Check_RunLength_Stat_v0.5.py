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


target_indices=get_col_range_indices("R", "Z")

# 파일 경로 문자열 앞에 붙이는 r은 **Raw String (날 문자열)**을 의미하며, 이는 파이썬에서 이스케이프 시퀀스(Escape Sequence) 해석을 방지
# "C:\users\new"인 경우 \n 을 줄바꿈으로 인식하지 않도록 함
df=pd.read_excel(r"D:\Stair_Step Analysis 02.xlsx", sheet_name='Mod_9', usecols=target_indices,header=0)

all_columns=df.columns.to_list()
#all_columns=range(1, len(df.columns)+1)

result={}
stat_result_run={}
total_max_run=[]

# N = 전체개수 중 뽑을 개수
N=2
for combo in combinations(all_columns,N):
    # combo는 ('Column1', 'Column3') 형태의 튜플
    # .values : Pandas DataFrame을 NumPy 배열로 변환
    # np.min(..., axis=1) : 각 행(동일 인덱스)별 최소값을 구함
    min_values = np.min(df[list(combo)].values, axis=1)

    # Counter로 대체
    #each_run=set(min_values)
    #max_run=int(max(each_run))  
    #count_run={}
    #result_run={}

    #for cell in min_values:
    #    count_run[cell]=count_run.get(cell,0)+1

    count_run=Counter(min_values)
    if 0 in count_run:
        del count_run[0]
    
    if not count_run:
        continue
    
    max_run=max(count_run.keys())
    total_max_run.append(int(max_run))

    result_run={}

    for run in range(max_run, 1-1, -1):
        # 'run+1'의 카운트를 안전하게 가져오기 위해 .get(run+1, 0) 사용
        # 키가 없으면 0을 반환하여 KeyError 방지
        next_run=count_run.get(run+1, 0)
        currnt_run=count_run.get(run,0)
        
        #차분계산
        result_run[run]=currnt_run-next_run

    # combo를 키(예: 'Col1-Col3')로, 차분계산식을 값으로 저장
    #result["-".join(map(str,combo))]=min_values
    key="-".join(map(str,combo)).replace("\n연속미출", "")
    stat_result_run[key]=result_run
    

#results_df=pd.DataFrame(result_run)
# results_df.to_excel('조합별_최소값_결과.xlsx', index=False)                 
# print(f"{N}개 조합에 대한 최소값 계산 완료. '조합별_최소값_결과.xlsx' 파일 저장됨.")

stats_df=pd.DataFrame.from_dict(stat_result_run, orient='index')

#run_cols = sorted([col for col in stats_df.columns])
run_cols = sorted(stats_df.columns, key=int)
stats_df['Max Run'] = total_max_run
final_cols = run_cols + ['Max Run']
stats_df = stats_df[final_cols]

try:
    stats_df.to_excel("조합별_최대런.xlsx", index=True, index_label="조합", sheet_name='Result')
    print(" 조합별 최대런 계산 완료 및 파일 저장.")
except PermissionError:
    # 파일이 열려 있어서 쓰기 권한이 없을 때 발생하는 에러 포착
    print("❌ 파일 저장 실패: '조합별_Run_통계_결과.xlsx' 파일이 현재 열려 있습니다.")
    print("⚠️ 엑셀 파일을 닫은 후 다시 실행해 주세요.")
except Exception as e:
    print(f"예기치않은 오류 발생 {e}")



# print(stat_result_run)
# print("Total Max Run: :", total_max_run)

