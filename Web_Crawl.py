from bs4 import BeautifulSoup
import requests
import pandas as pd

winning_numbers_byRound = []
start_round = 1190
end_round = 1198
cnt=0

for i in range(start_round, end_round + 1):
    URL = f"https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo={i}"
    
    try:
        # 1. HTTP 요청 및 오류 상태 확인 (4XX/5XX 에러 시 바로 예외 발생)
        response = requests.get(URL, timeout=10) # 타임아웃 10초 설정
        response.raise_for_status() 

        # 2. 인코딩을 서버 응답에 따라 자동 설정
        response.encoding = response.apparent_encoding
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 3. 데이터 추출 로직
        number_spans = soup.select('.win_result .num.win p span')
        bonus_span = soup.select_one('.win_result .num.bonus p span')
        
        # 4. 데이터가 모두 정상적으로 추출되었는지 확인
        if len(number_spans) == 6 and bonus_span is not None:
            winning_numbers = {'Round':i}
            
            # 당첨 번호 6개
            for idx, span in enumerate(number_spans):
                winning_numbers[f'#{idx+1}']=int(span.text)
                
            # 보너스 번호 1개
            bonus_number = int(bonus_span.text)
            winning_numbers['#B']=bonus_number
            
            winning_numbers_byRound.append(winning_numbers)
            cnt+=1
            print(f"✅ {i}회차 데이터 추출 완료")
        else:
            # 5. 데이터 구조가 예상과 다를 경우 처리
            print(f"⚠️ {i}회차: 데이터 구조 불일치 또는 번호 누락.")
            
    except requests.exceptions.RequestException as e:
        # 네트워크/URL 관련 오류 발생 시
        print(f"❌ {i}회차 요청 실패: {e}")
    except AttributeError:
        # soup.select_one()이 None을 반환했을 때 (태그를 못 찾았을 때)
        print(f"❌ {i}회차 파싱 실패: 예상된 태그를 찾을 수 없습니다.")
    except ValueError:
        # 문자열을 int로 변환할 수 없을 때
        print(f"❌ {i}회차 값 변환 오류: 추출된 내용이 숫자가 아닙니다.")
        

df=pd.DataFrame(winning_numbers_byRound)

# 최종 결과 출력
print(f"\n---총 {cnt} 개회차 정보 추출 ---")
# for round_num, numbers in winning_numbers_byRound.items():
#     print(f"회차 {round_num}: {numbers}")
