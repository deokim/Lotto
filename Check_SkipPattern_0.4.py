import numpy as np
import pandas as pd

# 당첨번호의 Skip, 오름차순자리 발생데이터 추출, 보너스 포함 기록까지 확대 필요

data_file=r"D:\Detailed Analysis 04.xlsm"
df=pd.read_excel(data_file, sheet_name="Rawdata분석", usecols="A, C:I", header=0)

with pd.ExcelWriter(r"D:\test.xlsx", engine='openpyxl') as writer:
     num_cols=df.columns[1:6+1]
     df_onehot = pd.DataFrame(0, index=df.index, columns=range(1, 46))
     df_onehot_position= pd.DataFrame(0, index=df.index, columns=range(1, 46))

     # Skip기록 = df_onehot,  오름차순자리기록 = df_onehow_position
     for idx, col in enumerate(num_cols):
          df_onehot.values[np.arange(len(df)), df[col] - 1] = 1
          df_onehot_position.values[np.arange(len(df)), df[col] - 1] = idx+1

     skip_by_number={}
     position_by_number={}
     for col in df_onehot.columns:
          skip_by_number[col]=(df_onehot[df_onehot[col]>0]).index.tolist()
          #최초 Skip은 별도계산 후 추가
          skip_by_number[col].append(len(df))
          position_by_number[col]=df_onehot_position[df_onehot_position[col]>0][col].tolist()
          
     # Shift 연산을 위해 skip_by_number을 DataFrame으로 변환
     df_skip_result =pd.DataFrame({k: pd.Series(v) for k, v in skip_by_number.items()})

     # 최종회차 당첨번호여부에 따라 Skip계산을 별도로 적용
     for col in df_onehot.columns:
          if df_skip_result.loc[0,col]:                #최종회차 당첨번호가 아닌 경우
               first_skip=df_skip_result.loc[0,col]
               df_skip_result[col]=df_skip_result[col]-df_skip_result[col].shift(1)-1
               df_skip_result.loc[0,col]=first_skip
          else:
               df_skip_result[col]=df_skip_result[col]-df_skip_result[col].shift(1)-1
               df_skip_result.loc[0,col]=0
                    

     df_position_result=pd.DataFrame({k:pd.Series(v) for k,v in position_by_number.items()})

     df_skip_result.to_excel(writer,sheet_name='B제외')
     df_position_result.to_excel(writer,sheet_name="B제외_AsdP")
     df.to_excel(writer,sheet_name="raw_data",index=False)


         
