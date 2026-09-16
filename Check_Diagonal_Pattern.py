import pandas as pd
import numpy as np
import openpyxl
from excel_utils import basic_sht_Style

def calculate_diagonal_length(df, min_hit):
    stat_results=[]
    diagonal_run_results={}

    total_rows = len(df)
    total_cols = len(df.columns)
    max_diff = total_cols        
    modulo_base = total_cols     

    for diagonal_index in range(max_diff):
        current_consecutive_length = 0
        l_current_consecutive_length = 0
        max_consecutive_length = 0
        l_max_consecutive_length = 0

        r_present_length=total_rows
        l_present_length=total_rows
    
        r_diagonal_result=[]
        l_diagonal_result=[]

        results = {}
        results['diagonal_idx']=diagonal_index+1
    # 전체행에 대해 우하향 대각선패턴 찾기
        for row_index in range(total_rows):        
        # 우하향 대각선 계산
            right_diagonal_col_index = (row_index + diagonal_index) % modulo_base
            cell_value = df.iloc[row_index, right_diagonal_col_index]
            if cell_value >= min_hit:
                current_consecutive_length += 1
                if current_consecutive_length > max_consecutive_length:
                    max_consecutive_length = current_consecutive_length
                    results['r_row']=str(row_index+2) + ":" + str(right_diagonal_col_index+1)       #최대연속패턴의 위치: 행:열
            else:
                current_consecutive_length = 0
                if row_index <= r_present_length:
                    r_present_length=row_index
                    results['r_present']=r_present_length
            r_diagonal_result.append(current_consecutive_length)

        # 좌하향 대각선 계산
            left_diagonal_col_index = (diagonal_index - row_index) % modulo_base
            cell_value = df.iloc[row_index, left_diagonal_col_index]  
            if cell_value >= min_hit:
                l_current_consecutive_length += 1
                if l_current_consecutive_length > l_max_consecutive_length:
                    l_max_consecutive_length = l_current_consecutive_length
                    results['l_row']=str(row_index+2) + ":" + str(left_diagonal_col_index+1)
            else:
                l_current_consecutive_length = 0
                if row_index <= l_present_length:
                    l_present_length=row_index
                    results['l_present']=l_present_length
            l_diagonal_result.append(l_current_consecutive_length)

        diagonal_run_results[f"R-{diagonal_index+1}"]=r_diagonal_result
        diagonal_run_results[f"L-{diagonal_index+1}"]=l_diagonal_result

    # 우하향 대각선 [0 ~ 열개수-1] 각각에 대해 최대연속발생 개수 저장 
        results['max_r_diagonal'] = max_consecutive_length
    # 좌하향 대각선 [0 ~ 열개수-1] 각각에 대해 최대연속발생 개수 저장 
        results['max_l_diagonal'] = l_max_consecutive_length

        stat_results.append(results)
    return stat_results, diagonal_run_results


file_name=r"D:\Detailed Analysis 04.xlsm"
# 각 그룹마다 발생한 최소개수
data_area={
    'interval_15':{'sht_name':'15구간분석', 'cols':'C:Q' },
    'interval_09':{'sht_name':'9구간,십단위분석', 'cols':'D:L'},
    'interval_05':{'sht_name':'5구간분석','cols':'C:G'},
    'mod_15' :{'sht_name':'Mod_X분석', 'cols':'BT:CH' },
    'mod_09' :{'sht_name':'Mod_X분석', 'cols':'AK:AS' },    
    'mod_05' :{'sht_name':'Mod_X분석', 'cols':'R:V' },    
}

min_hit = 1
wb=openpyxl.load_workbook(file_name,data_only=True)
final_round=wb['Rawdata분석']['AJ1'].value

with pd.ExcelWriter(r"D:\Diagonal.xlsx",engine='openpyxl') as writer:    
    row=0
    for key in data_area:    
        sht_name=data_area[key]['sht_name']
        cols=data_area[key]['cols']
        data=pd.read_excel(file_name, sheet_name=sht_name, usecols=cols, header=0)

        # apply함수를 사용하여 데이터프레임의 열 전체 속성을 숫자로 변경
        df=data.apply(pd.to_numeric, errors='coerce')
        df=df[:final_round]

        # 좌대각 / 우대각 연속 계산
        stat_results, diagonal_results = calculate_diagonal_length(df, min_hit)
        
        result_df=pd.DataFrame(stat_results)
        result_df['G_Type']=np.repeat(f'{key}',len(result_df))
        ordered_column=['G_Type','diagonal_idx', 'max_r_diagonal', 'r_row','r_present','max_l_diagonal', 'l_row','l_present']
        result_df=result_df[ordered_column]
        
        diagonal_result_df=pd.DataFrame(diagonal_results)
        diagonal_result_df['Round']=np.arange(final_round,0,-1,dtype=np.int64)
        new_columns=[ f'R-{i}' for i in range(1,len(df.columns)+1) ] + [ f'L-{i}' for i in range(1,len(df.columns)+1) ]
        new_columns=['Round'] + new_columns
        diagonal_result_df = diagonal_result_df[new_columns]
        

        print(key, "min_hit: ", min_hit)
        # print(result_df.to_string(index=False))        
        result_df.to_excel(writer,sheet_name="Summary",index=False,startrow=row)
        row=row+len(result_df)+2

        diagonal_result_df.to_excel(writer,sheet_name=f'{key}', index=False)
        ws=writer.sheets[f'{key}']
        style_sht=basic_sht_Style(ws,col_width=2.5)

