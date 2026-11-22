# from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from datetime import datetime, timedelta,timezone
import sys
import os

# filename=r'D:\Program_Pjt\Lotto\lotto_raw.csv'
filename=r'lotto_raw.csv'
# df_raw=pd.read_excel('lotto_raw.xlsx')
df_raw=pd.read_csv(filename)
old_round=df_raw.iloc[0,0]
old_date=df_raw.iloc[0,1]

add_win_numbers = []
missing_round=[]

KST = timezone(timedelta(hours=9))
now = datetime.now(KST).replace(tzinfo=None)

cnt=0

df_new=df_raw.sort_values(by='Round',ascending=True)
tmp_date=pd.to_datetime(old_date)
# tmp_date=datetime.strptime(old_date,"%Y-%m-%d %H:%M:%S")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


while ((now-tmp_date).days // 7 ):
    cnt +=1
    tmp_round=old_round+cnt
    URL = f"https://www.dhlottery.co.kr/lt645/selectPstLt645Info.do?srchLtEpsd={tmp_round}"

    win_number_byround={}

    try:
        response = requests.get(URL, headers=headers, timeout=15) # 타임아웃 설정
        # 웹사이트에 접속을 요청했을 때, 서버가 정상 응답(200 OK)이 아닌 에러 페이지(404 Not Found, 500 Internal Server Error, 503 점검 중 등)를 돌려주었을 때 이를 강제로 파이썬 에러(Exception)로 발생시켜 주는 안전장치
        response.raise_for_status()
        data=response.json()

        # "data": null 인 경우 안전하게 처리
        data_body=data.get("data")
        if not data_body or not data_body.get("list"):
            msg=data.get("resultMessage","데이터없음")
            print(f"⏳ {tmp_round}회차 조회 불가 ({msg})")
            missing_round.append(tmp_round)
            break

        # lotto_info = data["data"]["list"][0]
        lotto_info = data_body["list"][0]

        win_number_byround['Round']=tmp_round
        win_number_byround['date']=datetime.strptime(lotto_info["ltRflYmd"],"%Y%m%d")
        for idx in range(1,6+1):
            win_number_byround[f'#{idx}'] = lotto_info[f'tm{idx}WnNo']
        win_number_byround['B']=lotto_info["bnsWnNo"]
        add_win_numbers.append(win_number_byround)        
        print(f"✅ {tmp_round}회차 데이터 추출 완료")
    except Exception as e:
        missing_round.append(tmp_round)
        print(f"❌ {tmp_round}회차 요청 실패: {e}")        

    time.sleep(1)
    tmp_date=tmp_date+timedelta(weeks=1)

# 최신 상태인 경우 (주중 수동 실행 등) -> 정상 종료(0)
if cnt==0:
    print(f"ℹ️ 이미 최신 회차({old_round}회, {old_date}) 상태입니다.")
    latest_row = df_raw.iloc[0,2:].astype(int).tolist()
    nums_str=f"{', '.join(map(str,latest_row[:6]))} + B:{latest_row[6]}"
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"],"a") as f:
            f.write(f"latest_round={old_round}\n")
            f.write(f"win_nums={nums_str}\n")
    sys.exit(0)
# 업데이트할 회차가 있는데 실패한 경우 -> 비정상 종료(1) -> 실패 알림 발송
if len(missing_round):
    print(f'\n--총 {len(missing_round)}개 회차 누락')
    sys.exit(1)
else:
    print(f"\n---총 {cnt} 개회차 정보 추가 ---")
    df_add=pd.DataFrame(add_win_numbers)
    df_new=pd.concat([df_new,df_add])
    df_new=df_new.sort_values(by="Round", ascending=False)
    # df_new.to_excel(r'lotto_raw.xlsx',index=False,sheet_name='rawdata')    
    df_new.to_csv(filename,index=False)

    latest_row= df_new.iloc[0,2:].astype(int).tolist()
    nums_str=f"{', '.join(map(str,latest_row[:6]))} + B:{latest_row[6]}"
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"],"a") as f:
            f.write(f"latest_round={tmp_round}\n")
            f.write(f"win_nums={nums_str}\n")    
    
    sys.exit(0)
