import random

한글 = list("가나다라바바사아자차카타파하")

# 파일 = open("BMI.txt", "w")

# #header 만들기
# 파일.write("이름,몸무게,키\n")

# for i in range(1, 1000+1) :
#     이름=random.choice(한글) + random.choice(한글)
#     몸무게 = random.randrange(30, 120)
#     키 = random.randrange(140,200,2)
#     # print(f"{이름},{몸무게},{키}")
#     # print(",".join(이름,str(몸무게),str(키)))
#     #파일.write(이름 + "," +str(몸무게)+ "," + str(키)+"\n")
#     # 파일.write(f"{이름},{몸무게},{키}\n")
#     파일.write(",".join([이름, str(몸무게),str(키),"\n"]))

# 파일.close()

# 파일 = open("BMI.txt", "r")

# for i in 파일:
#     이름,몸무게,키=i.strip().split(",")
##     if "몸무게" in 몸무게 :
#      if not 몸무게.isdigit() :
#         continue
#     몸무게=int(몸무게)
#     키=int(키)
#     bmi=몸무게/(키/100)**2

#     print("\n".join( [
#         f"이름 : {이름}", 
#         f"몸무게 : {몸무게}",
#         f"키 : {키}", 
#         f"bmi : {bmi}", ""] ))

# 파일.close()

범위 = range(1,100+1)
제너레이터표현식 = (
    i*i
    for i in 범위
)

for 요소 in 제너레이터표현식:
    print(요소)