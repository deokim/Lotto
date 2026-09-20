### Lotto RawData 
#### lotto_raw.xlsx
- 대한민국 Lotto 역대당첨번호 정보
- Header : 회차, 추첨일자, #1, #2, #3, #4, #5, #6, #B 

```python
import pandas as pd

url="https://raw.githubusercontent.com/deokim/Lotto/main/lotto_raw.xlsx"
df = pd.read_excel("lotto_raw.xlsx",usecols="A, C:I")

print(df.head())
```

#### Web_Crawl.py, .github/workflows/auto_crawl.yml
- 매주 토요일 오후 11시 30분 ~ 일요일 새벽 3시에 당첨정보 업데이트.<br> (단 Git Actions의 스케줄링으로 인해 변동가능)
- 당첨정보 업데이트 성공/실패 여부를 텔레그램 bot으로 전달.<br>
  Github - settings - secrets and variables - Actions 내 repository secrets에 TELEGRAM_TO, TELEGRAM_TOKEN 세팅필요