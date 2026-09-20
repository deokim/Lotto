# from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from datetime import datetime, timedelta

df_raw=pd.read_excel('lotto_raw.xlsx')
old_round=df_raw.iloc[0,0]
old_date=df_raw.iloc[0,1]

add_win_numbers = []
missing_round=[]

now=datetime.now()
cnt=0

df_new=df_raw.sort_values(by='Round',ascending=True)

tmp_date=old_date

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
        data=response.json()
        lotto_info = data["data"]["list"][0]

        win_number_byround['Round']=tmp_round
        win_number_byround['date']=datetime.strptime(lotto_info["ltRflYmd"],"%Y%m%d")
        for idx in range(1,6+1):
            win_number_byround[f'#{idx}'] = lotto_info[f'tm{idx}WnNo']
        win_number_byround['B']=lotto_info["bnsWnNo"]

        add_win_numbers.append(win_number_byround)        
        print(f"✅ {tmp_round}회차 데이터 추출 완료")
    except requests.exceptions.RequestException as e:
        missing_round.append(tmp_round)
        print(f"❌ {tmp_round}회차 요청 실패: {e}")        

    time.sleep(1)
    tmp_date=tmp_date+timedelta(weeks=1)

if len(missing_round):
    print(f'\n--총 {len(missing_round)}개 회차 누락')
else:
    print(f"\n---총 {cnt} 개회차 정보 추가 ---")
    df_add=pd.DataFrame(add_win_numbers)
    df_new=pd.concat([df_new,df_add])
    df_new=df_new.sort_values(by="Round", ascending=False)
    df_new.to_excel(r'lotto_raw.xlsx',index=False,sheet_name='rawdata')
