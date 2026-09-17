#################     VSCODE
#  주석 단축키 : ctrl + k + c, 주석해제는 ctrl + k + u
#  주석 단축키 : ctrl + /,  주석해제는 동일 단축키
#  Multi Cursor : Ctrl + alt + ↓ (화살표), or alt + 마우스

# 터미널화면 불러오기 : Ctrl + `  (` backtick키 - tab키 위에 있는 키),  아니면 화면 하단부를 끌어올려도 됨
# 터미널 화면 지움 : cls    아마 clear Screen 일듯
# VSCODE 설정화면 불러오기  Ctrl + ,
# 여러행 선택 : ALT + 마우스왼쪽버튼
# 현재 선택된 텍스트와 일치하는 모든 항목 선택 : CTRL + SHITF + L
# CTRL+D  순차적으로 해당 텍스트 선택
# Shift + Alt를 누른 상태에서 마우스를 세로로 드래그합니다.

#위의 행 코드 복사  SHIFT + ALT + 아래화살표


############################## 혼자 공부하는 파이썬 개정판 - 윤인성

### 문자열 연산자
## 문자열합치기 +,  문자열반복 문자열 * 정수(?)
## Escape 문자 \

## 할당 연산자와 같음을 비교하는 연산자가 다름. vba에서는 둘다 "=" 사용
## 파이썬에서는 할당 연산자, "=" 같음 연산자 "=="

### 문자열 함수
##  strip() 공백제거, lstrip() 왼쪽공백제거, rstrip()오른쪽공백제거


##비교 연산자를 중복해서 사용 가능,  10< 20 < 30
a=52
b=273

#print(a,"+", b, "=", a+b)

#print("#Test1")
#print("{}".format(10, 20, 30))

#print("#Test2")
#print("{}, {}".format(10))

## Format함수
#print("{} + {} = {}".format(a, b, a+b))
#print("{}+{}={}".format(a, b, a+b))

## f문자열
#print(f"{a}+{b}={a+b}")

#print("10 20 30 40".split(" "))

#a="안 녕 하 세 요"
#a=a.split()
#print(a)

##find함수, rfind함수 =>vba의 InstrRev와 동일

## in 연산자. not in 연산자도 가능
#print("안녕" in '안녕하세요')


## 정수를 규격화해서 출력, 정수 = d,  부동소수점 = f
#print("{:d}".format(52))

##특정 칸만큼 출력
#print("{:05d}".format(52))


########## list : 배열은 기본적으로 길이가 고정. 요소를 추가하거나 제거 등의 기능을 추가
##여러 개의 자료 형을 섞어 사용할 수 있음, 파이썬에서는 대괄호 [ ] 로 리스트를 만듦

#요소 추가 : append(), insert(), extend()
#요소 제거 : del(제거하고 싶은 인덱스), pop(제거하고 싶은 인덱스, 기본값 -1), remove(제거하고 싶은 요소(값)), clear()
#clear()함수는 리스트 자체를 메모리에서 삭제
# 리스트를 초기화하고 싶으면 리스트명 = [] 사용
#요소 정렬 : sort(), sort(reverse=True)
#요소 존재를 확인: in, not in

## 중첩 리스트, 이차원 리스트, 예를 들어 삼차원 리스트를 분해하려면, 반복문을 3개 중첩해서 분해해야 함
# a=[[1,2,3],[4,5,6,7],[8,9]]

# for i in a:
#     print(i)
#     for j in i:
#         print(j)

## 중첩리스트를 만드려면 append()함수를 이용해야 함. 
## 5행, 10열, 50개 요소(element)를 갖는 중첩 리스트
two_d_list=[]
for i in range(5):
    line=[]
    for j in range(10):
        line.append(j)
    two_d_list.append(line)

print(two_d_list)

## 전개연산자, *list , 요소를 하나하나 분리함
# 리스트 내부
# a=[1,2,3]
# b=[*a,4,5]

# 함수 매개 변수
# date=[2024,2,5,10,14]
# print("{}년 {}월 {}일 {}시 {}분".format(*date))

########## Dictionary
## 딕셔너리 중괄호{} 로 묶어 줌.  key : value,  키 콜론 값 쉼표 로 구분
# product={
#     #키 : 숫자, 문자열, Bool(튜플)
#     #값 : 모든 값
#     "제품명":"건망고 슬라이스",
#     "가격" : 4000,
#     "분류": "식품"
# }
# product["제품명"]

# for key in product:
#     print(key)
#     print(product[key])
#     print("-" * 20)

##딕셔너리 요소의 값을 변경하는 방법
#product["제품명"]="습망고 슬라이스"

##요소를 추가하는 방법, 키를 추가하는 방법
#product["price"]="3000"

##요소를 제거하는 방법 : del keyword
#del product["price"]

##키의 존재를 확인하는 방법, in, not in 함수  // get()함수
# product["original" in product]
# product.get("price")    #해당되는 키가 없으면 None 을 반환


##딕셔너리와 리스트를 조합
# pets=[
#     {"name":"구름", "age":5},
#     {"name":"초코", "age":3},
#     {"name":"아지", "age":1},
#     {"name":"호랑이", "age":1}
# ]

# print("#우리 동네 애완 동물들")
# for pet in pets:
#     #print(f"{pet['name']} {pet['age']살}")
#     print( pet['name'],pet['age'])

##### 딕셔너리로 빈도 계산, 카운터
##### Collections 모듈에 있는 Counter 함수를 사용하면 이터러블객체 안에 있는 모든 요소의 빈도수를 세어 딕셔너리 형태로 받아올 수 있음
# numbers=[1,2,6,8,4,3,2,1,9,5,4,9,7,2]
# counters={}

# for number in numbers:
#     # 딕셔너리와 키와 값을 추가한다.중복된 값이 들어오면 키의 값을 하나 추가한다.
#     # 딕셔러이에 키가 있는지 확인, 키가 없으면 추가한다.
#     # if counters.get(number) == None :
#     #     counters[number]=1
#     # else :
#     #     counters[number] +=1
#     if number not in counters:
#         counters[number]=""
#     counters[number]+="■"

# for key in sorted(counters.keys()):
#     print(f"{key}: {counters[key]}")

character={
    "name": "기사",
    "level": 12,
    "items": {
        "sword": "불꽃의 검",
        "armor": "플레이드"
    },
    "skill": ["베기","세게 베기","아주 세게 베기"]
}



########## 반복문과 Range
## Range(숫자) : 해당되는 숫자는 포함하지 않음. 왜냐하면 초기값을 지정하지 않으면 0부터 시작하기 때문
## 반복문의 반복 범위를 설정할 때 사용 가능
# list(range(10))
# list(rnage(1,10+1))  #[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# list(range(10, 0-1, -1))
    

### 반복문으로 수열의 일반항, 점화식, 피보나치 수열 만들기
### append() 함수를 사용하면 배열의 크기를 늘리느라 실행 속도가 느림. 배열 크기를 미리 알면 미리 만들어 놓는 것이 빠름
# n=20
# a=[None] * (n+1)

# for i in range(1,n+1):
#     if i==1 or i==2:
#         a[i]=1
#     else :
#         a[i]=a[i-1]+a[i-2]
#     #a.append(a_n)
        


### reversed() 함수,  매개변수 : 반복 가능한 것,  결과: 그 것을 뒤집은 것,  결과 자료형: 이터레이터????
### reversed 함수는 한번만 사용 가능?????????????????
# print(list(reversed(range(10))))

# 별 피라미드
s=""
step=14
for i in range(1,step+1):
    for j in range(1,step-i+1):
        s+=" "
    for k in range(2*i-1):
        s+="*"
    s+="\n"

print(s)


### 별 피라미드
height=10

# for i in range(1, height+1):
#     print("*"*i)

for i in range(1, height+1):
    result=""
    for j in range(i):
        result +="*"
    print(result)

## Triangular Number
limit=10000
i=1
sum_value=0

import time
number=0
start=time.time()
while time.time()-start<5:
    number+=1
print(number)

number=0
time_tick=time.time()+5
while time.time() < time_tick:
    number+=1
print("5초 동안 {}번 반복함".format(number))




while sum_value <= limit:
    sum_value +=i
    i+=1

print("{}를 넘을 때 {}을 넘으며 그 때의 값은 {}입니다.".format(i-1, limit, sum_value))

### 리스트, 딕셔너리와 관련된 기본 함수
## min(), max()
a=[52,273,32,43, 38, "os"]

print(max(a))
print(max(52,273,32,43, 38))
print(max(*a))    #전개 연산자도 사용 가능

## sum()함수, 만약 계산할 수 없는 내용이 리스트에 있어도 무시하고 계산
print(sum(a))

## enumerate 함수, 딕셔너리의 인덱스와 키 값을 튜플로 만들어줌
# fruits=["바나나", "사과", "포도"]

# for fruit in enumerate(fruits):
#     print(fruit[0], fruit[1])

# for i, fruit in enumerate(fruits):
#     print(i, fruit)


## items()함수. 딕셔너리의 키 와 값을 튜플로 만들어줌.
# for 키, 값 in 딕셔너리.items():
#     print(키, 값)

########## 리스트 내포 list comprehension
## 반복가능한 것을 기반으로 새로운 리스트를 만들어내는 문법. 함수형?
## 세트 내포, 딕셔너리 내포, 제너레이터 표현식

## [표현식 반복문]
# A=[
#     2*i+1                       #표현식 
#     for i in range(0,10)        #반복절
#     if i %2 ==0                 #조건절
# ]

# print(A)

### 진법변환, 십진법 --> b : binary 2진법, o : 8진법, h : hexa? 16진법
### 반대로    십진법으로 변환할 때는 int 함수
# f"{10:b}"
# int('1010',2)

## 1~100 사이에 있는 숫자 중, 2진법으로 변환했을 때, 0이 하나만 포함된 숫자
# a=[
#     i
#     for i in range(1, 100+1)
#     if f"{i:b}".count("0")==1
# ]

# for i in a:
#     print(i, ":", f"{i:b}")
# print("합계:", sum(a))


list_nest=[1, 2, [3, 4], 5, [6, 7], [8, 9]]
list_flat=[]

for element in list_nest:
    if type(element)==list:
        for item in element:
            list_flat.append(item)
    else:
        list_flat.append(element)
print(list_flat)



##### 프로그램, 루틴, 프로시저, 메서드 함수
## 코드 전체: 프로그램, 루틴 (+프로세서, 메서드)
## 작은 코드 : 서브 프로그램, 서브 루틴
## 매개변수(parameter)를 갖는 서브 프로그램/서브 루틴  : 프로시저(procedure)
## 리턴값을 갖는 프로시저 : 함수(function)
## 클래스 내부에 있는 함수 : 메서드(method)

## ADA : 프로시저 문법과 함수 문법이 완전히 분리
## 현대적 프로그래밍 언어: 함수로 통합! 파이썬도 함수로 통합!

## parameter(매개변수): 함수의 괄호 안에 넣는 변수
## argument(인수) : 함수 호출할 때 넣은 값


##### 파이썬에서의 stack 스택과 Heap 힙
## 기본자료형(숫자, 문자열, 불 등)은 스택(상자)에 차곡차곡 보관
## 복합자료형(리스트, 딕셔너리, 객체 등)은 힙(창고)에 보관. 단 창고 어느 선반에 있는 지 주소가 있어 야 함
## 힙은 마치 이케아에서 물건을 찿을 때, 어느 선반에 있는지 위치를 따로 가지고 있고, 실제 문건은 그 선반에 있는 것과 동일

## 함수 외부의 스택을 전역 스택(global stack)이라고 부름
## 함수를 호출할 때마다 함수를 위한 Stack이 새로 만들어짐 & 리턴될 때 스택을 제거함

## 변수의 할당과 참조
## 파이썬에서는 자신과 가까운 스택부터 위로 올라가면서 참조

## 전역 위치에서 a,b라는 변수를 생성
# a=10
# b=[1,2,3,4]

# def function():
##    global 키워드를 선언하면 함수 내부의 별도 스택을 만들지 않음
##    함수는 실행되기 전에, 내부에서 형성되는 모든 변수에 대한 정보를 미리 파악
##    따라서 변수를 선언하지 않고, print(a), print(b)를 하면 UnboundLocalError가 발생
#     global a, b
    # a=20
    # 함수 스택에 새로운 변수를 만듦
    #  b=[5,6,7,8]
    # b.extend 를 하게 되면 함수 내부에서 새롭게 변수를 만들지 않고 전역 위치에 있는 b를 참조 
#     b.extend([5,6,7,8])
#     print(a)
#     print(b)

# function()
# print(a)
# print(b)

##### 함수의 값복사와 레퍼런스복사 (유튜브 강의록 56강 - 메모리 구조(3)-복사)
## 변수를 변수에 할당하면[복사하면], 스택에 있는 것이 할당[복사]되는 것이다.
## 기본 자료형 복사(스택)와, 복합 자료형 복사(힙)
## C 언어의 & 주소? * 값? 연산자??

# a=10
# b=[1,2,3,4]

# print(a,b)

# def function_a(c,d):
#     c=20
#     d=[5,6,7,8]
# function_a(a,b)

# print(a,b)

# def function_b(c,d):
#     c=30
#     d.extend([9,10])

# function_b(a,b)
# print(a,b)


##### 재귀함수
## 팩토리얼 연산, 반복문으로 구현, 재귀함수로 구현
## 재귀함수 : 수열의 점화식(이웃한 항의 관계)을 통해 구현
## 팩토리얼 점화식 : 1!=1, n이 2이상의 수일 때, n!=n*(n-1)

# def factorial(n):
#     if n ==1 :
#         return 1
#     elif n >= 2 :
#         return n*factorial(n-1)


# factorial(6)

##### 메모화
## 피보나치 수열을 재귀함수로 구현, 실행흐름이 Tree 형태가 됨
## !!!!!!! 그래프 - 깊이 우선 탐색(BFS)와 트리 - 전위 순회(PreOrder Traversal)
## 트리가 계속 가지를 치면서 늘어가고, 이 과정 중에 함수값을 중복으로 계속 계산
## 이를 줄이기 위해 기존에 계산된 값을 재활용하기 위해 "메모화" 과정을 거치게 됨

#메모화 memonization를 위해 memo 라는 딕셔너리 선언
memo={1:1, 2:1}
def f(n):
    if n in memo:
        return memo[n]
    # if n==1:
    #     return 1
    # elif n==2 :
    #     return 1
    else:
        temp=f(n-1)+f(n-2)
        memo[n]=temp
        return temp
        # return memo[n] :=f(n-1)+f(n-2)
print(f(50))

##### 조기리턴(early return)
memo={1:1, 2:1}
def f(n):
    if n in memo:
        return memo[n]
    temp=f(n-1)+f(n-2)
    memo[n]=temp
    return temp
print(f(50))

##### List Flatten 리스트 평탄화 : 중첩된 리스트가 있을 때, 중첩을 모두 제거하고 풀어서 1차원 리스트로 만드는 작업 

# data=[[1,2,3],[4,5,6],7,[8,9]]
data =[[1,2,3],
       [4,[5,6]],
       [7,[[[[[1,2,3],4]]]]]
       [8,9]]
def flatten(data):
    output=[]
    for 요소 in data:
        if type(요소) !=list :
            output.append(요소)
        else:
            output.extend(flatten(요소))           #list를 매개변수로 받으니, list를 추가할 때 extend()함수 사용
    return output

print(flatten(data))

#### flatten함수 자체 작성 코드, 함수 내부에 output선언하고 output=[]로 선언하면 결과가 제대로 안나올까
data=[[1,2,3],[4,5,6],7,[8,9]]
#output=[]
def flatten(data):
     output=[]     
     for item in data:
         if type(item)!=list:
             output+=[item]    #output.append(item) 과 동일
         else:
             output+=flatten(item)
     return output

flatten(data)

##### 확인문제 - 인원수를 나누는 패턴(조합), 개개인의 사람까지 고려 X, 한 사람만 앉는 테이블 X
##### 예를 들어 6명을 테이블에 나누는 경우, 2+2+2, 2+4, 3+3, 6 의 4가지 경우
##### 한개의 테이블에 앉을 수 있는 사람 = 10명, 100명의 사람이 하나 이상의 테이블에 나누어 앉는 패턴은???

## 최대 필요 테이블 수량 = 인원 // 2 , 여기서 2는 테이블에 앉을 최소한의 사람수인 2명, 또한 홀수인 7명이더라도, 테이블 수량은 3개임. 1명만은 앉지 못하기 때문에 2+2+2+1 불가능
## 최소 필요 테이블 수량 = Roundup(인원 / 테이블좌석수)
## 100명이라면 최소 10개 ~ 최대 50개까지의 테이블이 필요함
## 분할(partition)문제와 유사

########################실패작 1    
# total=6
# table_size=10
# person=2
# count=0
# result=[]

# max_table= int(total/2)
# if total/table_size - int(total/table_size)>0:
#     min_table=int(total//table_size) +1
# else: 
#     min_table=int(total/table_size)

# for i in reversed(range(min_table, max_table+1)):
#     #tmp_table_count=i

#     # j -> each table
#     for j in reversed(range(i)):
        
#         #Initiate a variable or List
#         #chk_table_size=0
#         table_pattern=[]    
#         for tmp in range(i):
#             table_pattern.append(person)
        
        
#         # 자릿수가 늘어날 때마다, for 문의 중첩이 늘어나는 형태? 이 형태는 안됨. 자릿수가 고정된게 아니기 때문에
#         for k in range(person,table_size):
            
#             table_pattern[j]=k
            
#             #chk_table_size +=j
                        
#             if sum(table_pattern) == total:
#                 count +=1
#                 #result=result + table_pattern
#             elif sum(table_pattern) > total :
#                 break    
        
#         # if chk_table_size == total :
#         #    count +=1


# print(count)
# # print(result)

########################실패작 2
# total=6
# table_size=10
# person=2
# global count
# result=[]

# count=0
# max_table= int(total/2)
# if total/table_size - int(total/table_size)>0:
#     min_table=int(total//table_size) +1
# else: 
#     min_table=int(total/table_size)

# def DivideTable(index, table):
#     global count
#     if index == 1:
#         for p in range(2, table_size+1):
#             table[index-1]=p
#             if sum(table) == total:
#                 count +=1
#             elif sum(table) > total:
#                 break
#     else:
#         return DivideTable(index-1, table)


# for i in range(min_table, max_table+1):
#     # j -> each table
#     for j in range(1,i+1):
#         #Initiate a variable or List
#         table_pattern=[]
#         for tmp in range(i):
#             table_pattern.append(2)
#         DivideTable(j, table_pattern)
 
# print(count)

########## 확인문제 5 깊이 우선 탐색(DFS),  분할(partition)수를 구하는 알고리즘으로도 활용 가능
#### 재귀함수는 Stop 조건을 만나거나, 더 이상 재귀호출이 이루어지지 않으면 종료되어 상위로 올라가는 구조임
import time

total=6
table_size =10
min_person=2

# counter=0
memo={
    # 키 : 값
    # 키 = 함수의 매개변수 : 값 = 리턴값
}

def graph(node, previous):
    #튜플, 이뮤터블 자료형 -> 딕셔너리 키로 사용가능
    if (node, previous) in memo:
        return memo[(node, previous)]
        
    result =0
    if node ==0:
        # global counter
        # counter +=1
        result =1
    for i in range(max(min_person,previous), min(node,table_size)+1):
        result += graph(node-i, i)
    
    memo[(node, previous)]=result
    return result

실행이전시간 = time.time()
print(graph(total,0))
실행이후시간 = time.time()
print(실행이후시간 - 실행이전시간)

##########################################################################################################
min_input=2
max_input=10
#all_man=6
#output=0
count=0
memo={}

def part(remain, inputed):
    global count
    count+=1
    #key=str([remain, inputed])

    if (remain, inputed) in memo:
        return memo[(remain, inputed)]
    if remain<0:
        return 0
    elif remain==0:
        return 1        
    counter=0
    for i in range(inputed, max_input+1):
        counter+=part(remain-i, i)    
    memo[(remain, inputed)]=counter
    return counter
    
result=part(4,2)
print("Result: ", result)
print("Total Iteration: ", count)
print(memo)

############################################ 결과를 저장하는 부분 추가(작업 중). 
total=6
table_size =10
counter=0
tmp_list=[]
result_list=[]

# memo={
#     # 키 : 값
#     # 키 = 함수의 매개변수 : 값 = 리턴값
# }

def graph(node, previous):
    # if (node, previous) in memo:
    #     return memo[(node, previous)]
        
    result =0
    global tmp_list
    
    if node ==0:
        # global counter
        # counter +=1
        result =1
        global result_list
        result_list.append(tmp_list)
        tmp_list=[]
        
    if node < 2:
         tmp_list=[]
    for i in range(max(2,previous), min(node,table_size)+1):
        
        # if node < total:
        #      tmp_list.append(total-node)
        tmp_list.append(i)
        result += graph(node-i, i)
    
    # memo[(node, previous)]=result
    return result

print(graph(total,0))
print(result_list)
# graph(total,0)
# print(counter)

###########################################################################제미나이코드
def get_partitions(remain, max_val):
    """
    정수 remain을 max_val 이하의 양의 정수들로 분할하는 모든 경우를 리스트의 리스트로 반환합니다.
    """
    # 1. 기본 사례 (Base Case)
    if remain == 0:
        # 분할에 성공 (리스트가 비어 있음을 나타내는 리스트를 반환)
        return [[]]
    if remain < 0 or max_val == 0:
        # 실패 또는 더 이상 사용할 수가 없음
        return []

    # 최종적으로 찾은 모든 분할을 저장할 리스트
    all_partitions = []
    
    # 2. 현재 선택(i)을 포함하는 경우
    # i를 현재 분할에 사용하고, 다음 재귀 호출에서는 i 이하의 수만 사용하도록 합니다.
    for i in range(max_val, 0, -1):
        # i를 사용하고 남은 remain-i를 분할하는 모든 경우를 재귀 호출로 얻음
        sub_partitions = get_partitions(remain - i, i)
        
        # 3. 조합: 현재 선택한 i를 얻어온 나머지 분할 리스트 앞에 추가
        for partition in sub_partitions:
            # 새로운 분할 리스트를 만들고 i를 맨 앞에 추가
            new_partition = [i] + partition
            all_partitions.append(new_partition)
            
    return all_partitions

# 6의 전체 정수 분할 (최대 6 이하의 수 사용)
n = 6
all_results = get_partitions(n, n)

print(f"{n}의 전체 정수 분할 경우의 수: {len(all_results)}가지")
print("--- 모든 분할 경우 ---")
for p in all_results:
    # 결과를 보기 좋게 출력
    print(" + ".join(map(str, p)))


##### tuple 튜플
### 튜플은 소괄호로 만듦 ()
## 요소를 하나 갖는 튜플 b=(1,) 뒤에 괄호 추가   상황에 따라 소괄호 생략 가능
## 외관이 간단!, 기능이 간단, 용량도 적게 먹고 빠름

## 다중할당구문. 왼쪽 = 오른쪽,  각각 반복할 수 있는 것, 왼쪽에는 '리스트와 튜플 형태의 구문'만 가능, 딕셔너리는 불가능
## [a,b]=range(2) , a=0, b=1
## [a,b]={"1":2, "3""4"},  a=1, b=3
##  a,b = [10,20] 과 같이 혼합해서도 사용 가능
## (a,b)=(10,20)  or a,b=10,20 으로 더 간단히 표현 가능!

## 함수의 다중 리턴, 즉 반환하는 값을 여러개 돌려줄 때 사용 가능 
def a():
    return 10,20,30

b,c,d=a()
print(b,c,d)

## 함수 다중 리턴은 enumerate() 과 items() 함수에 적용됨

## 요소를 변경할 수 없음: 리스트와 달리 튜플은 값을 변경할 수 없음

##### 자료:  이뮤터블 + 뮤터블 자료형

## immutable 이뮤터블 : 변수에 넣었을 때, 스택에 있는 값을 변경해야만 + 값을 변경할 수 있는 자료
a=10
a=20 # 숫자는 이뮤터블, 불, 문자열, 튜플 이뮤터블 (문자열이나 튜플은 내부의 한 요소 값 변경 불가능)
c="안녕하세요"
c[0]="가"
# TypeError: 'str' object does not support item assignment

d=(1,2,3)
d[1]=4
# TypeError: 'tuple' object does not support item assignment'

## 이뮤터블 자료를 딕셔너리의 키로 사용할 수 있음 !!!!!!! Hashable
## 이뮤터블 --> Hashable(성립함),   Hashable --> 이뮤터블 (성립안함)
A = {
    (2022,1,1): "새해",
    (2022,1,6): "생일",
    (2022,12,25) : "크리스마스",

}

## mutable 뮤터블(변할 수 있는): 변수에 넣었을 때, 스택에 있는 값을 변경하지 않아도 + 값을 변경할 수 있는 자료
## 리스트, 딕셔너리
## 뮤터블 자료 중, _hash_()함수가 구현된 자료는 뮤터블도 딕셔너리의 키로 사용 가능
## 프로그래밍 언어 별로 뮤터블, 이뮤터블 자료 구분은 달라질 수 있음

## mutability(뮤터블, 이뮤터블 자료), variance(공변/반공변/무공변자료), variable/constant(변수/상수)

##### 콜백함수
## 함수는 변수에 저장할 수 있다. 함수를 저장한 변수를 호출할 수 있다(함수처럼??)

def call_10_times():
    print("호출되었습니다")

a=call_10_times
print(a)
a()

def call_10_times(콜백함수):
    for i in range(10):
        콜백함수(i)

def print_hello(매개변수):
    print("안녕하세요!",매개변수)

#매개변수로 함수를 입력해서 전달
call_10_times(print_hello)

### map 함수
## 리스트 각각의 요소에 함수를 적용해서, 새로운 이터레이터를 리턴한다.
## 이터레이터 = map(함수,리스트)

## filter함수[함수, 리스트]
## 리스트의 요소를 함수에 전달했을 때 결과로 True가 나오는 녀석을 모아서 새로운 이터레이터를 만듦


def my_map(콜백함수, 리스트):
    # output=[]    
    #  for 요소 in 리스트:
    #     output.append(콜백함수(요소))
    # return output
    return [
        콜백함수(요소)
        for 요소 in 리스트
    ]

def power(숫자):
    return 숫자 **2

A=[1,2,3,4,5]

print(my_map(power,A))

##### 람다 : 간단한 함수를 간단하게 해주는 문법. 한줄에 리턴코드를 갖는 함수
## lambda 매개변수: 리턴해주고 싶은 값 

power=lambda 숫자: 숫자 **2
is_odd = lambda 숫자: 숫자 % 2 ==1

power(2)

## 람다를 인라인 함수로 사용하기 : 인라인 : 한 줄안에 무엇인가를 넣는 것
A=[1,2,3,4,5]
이터레이터=map(lambda 숫자:숫자**2, A)
print(list(이터레이터))

A=[
    {"제목": "혼공파", "가격":18000},
    {"제목":  "머신러닝", "가격":26000},
    {"제목": "혼공자", "가격":24000}
]

def 가격(책):
    #print(책)
    return 책["가격"]

print(min(A, key=가격))
# print(min(A, key=lambda 책:책["가격"]))



##### 파일 처리, 읽기 처리 / 쓰기 처리


## 한글의 경우 인코딩이 다르면, 문자가 깨져서 보이는 문제가 발생함

### (1) 스트림(stream) 연결
## 파일 = open("파일경로", "모드")
## w 쓰기모드, a (기존)파일에 추가해서 쓰기, r 읽기 모드

# 파일 = open("text.txt","r")
### (2) 스트림을 통해 데이터 통신
# 문자열 = 파일.read()
# print(문자열)
### (3) 스트림 해제
# 파일.close()

## close()없이 with 구문으로 해결하기. 자동으로 파이썬에서 파일을 close 해줌

# with open("a.txt","a") as 파일:
#     파일.write(입력)

## read() 함수는 읽기(r) 모드로 사용할 때만 가능?



books=[
    {
        "제목":"혼자 공부하는 파이썬",
        "가격": 18000
    }, 
    {
        "제목":"혼자 공부하는 머신러닝 + 딥러닝",
        "가격": 26000
    }, 
    {
        "제목":"혼자 공부하는 자바스크립트",
        "가격": 24000
    }, 
]

print(min(books, key=lambda dict:dict["가격"]))



##### 제너레이터
## 이터러블 iterable : 반복할 수 있는 것. 반복문 뒤에 넣을 수 있는 것, 리스트, 튜플, 딕셔너리

def test():
    print("A지점 통과")
    yield 1
    print("B지점 통과")
    yield 2
    print("C지점 통과")

output=test()
print("D지점 통과")    
a=next(output)
print(a)
b=next(output)
print(b)
print("F지점 통과")
c=next(output)
print(c)

next(output)

## 이터레이터 : Iterate + or : 이러터블을 만드는 방법 중의 하나
## 1) 제너레이터 표현식 : 이터레이터를 만드는 방법 중 하나
##    리스트 내포와 형태는 비슷..단 대괄호가 아닌 소괄호를 사용
##    next(이터레이터) : 내부의 요소를 꺼낼 수 있음

범위 = range(1,100+1)
제너레이터표현식 = (
    i*i
    for i in 범위
)

for 요소 in 제너레이터표현식:
    print(요소)


## 제너레이터 함수 : 호출했을 때, 내부의 코드가 즉시 실행되지 않고, 제너레이터를 리턴함
## map 함수와 filter 함수도 "제너레이터 함수"임
def 함수():
    for i in range(1, 100+1):
        yield i*i
"""
제너레이터=제너레이터함수()
for 요소 in 제너레이터:
    print(요소)
"""

## 리스트 내포는 해당 코드를 실행하는 순간, 1) 새로운 리스트를 생성(메모리 2개까지 사용)
## 2) 새로운 요소를 만들어내야 함으로 표현식 연산(?)을 즉시 함. -> 해당 코드를 실행하는 순간 자원(CPU, 메모리)를 많이 차지함
## 반면 제너레이터 표현식은 해당 코드를 실행하는 순간, 1)기존의 데이터를 사용, 2)특정 요소를 사용할 때, 표현식 연산을 함 
## -> 즉 메모리를 적게 차지하고, 연산이 분산됨

##이터레이터 클래스

##### 도전문제 : 하노이탑

counter=0

def 하노이탑(원판,시작기둥,대상기둥,보조기둥):
    global counter
    if 원판 ==1:
        counter +=1
        #print(시작기둥 + "->" + 대상기둥)
    else:
        하노이탑(원판-1, 시작기둥, 보조기둥,대상기둥)
        하노이탑(1, 시작기둥, 대상기둥,보조기둥)
        하노이탑(원판-1, 보조기둥, 대상기둥,시작기둥)


하노이탑(20, "A", "B","C")
print(counter)

#################################################################################################
# 예외처리

list_input_a=["52", "273", "32", "스파이", "103"]
list_number=[]

for item in list_input_a:
    try:
        float(item)
        list_number.append(item)
    except:
        pass

print(list_number)


#####################################################################################################
list_number=[52,273,32,72,100]

try:
    number_input=int(input("정수입력: "))
    print("{}번째 요소: {}".format(number_input, list_number[number_input]))
    # 예외.발생해주세요()
except ValueError as exception:
    print("정수를 입력해주세요")
    print(type(exception), exception)
except IndexError as exception:
    print("리스트의 인덱스를 벗어났습니다.")
    print(type(exception), exception)
except Exception as exception:
    print("미리 파악하지 못한 예외가 발생했습니다")
    print(type(exception), exception)


#########################################################################################################
### 폴더열기 - GEMINI 수정
import os
def read_folder_safe(path):
    try:
        output = os.listdir(path)
    except PermissionError as e:
        # 권한이 없는 폴더는 건너뛰고 경고 메시지 출력
        print(f"⚠️ 권한 오류로 인해 폴더를 건너뜁니다: {path} ({e})")
        return # 함수 종료
    except FileNotFoundError:
        # 경로가 잘못되었을 경우 처리
        print(f"❌ 폴더를 찾을 수 없습니다: {path}")
        return

    for item in output:
        # 항상 전체 경로를 사용하도록 os.path.join() 사용
        full_path = os.path.join(path, item) 

        if os.path.isdir(full_path):
            read_folder_safe(full_path) # 재귀 호출 시에도 전체 경로 사용
        else:
            print("file:", full_path)

##############################################################################################################
#  리스트내포, 세트내포, 딕셔너리내포
# 제너레이터 표현식 generator expression

a=(
    item*item for item in range(0,20) if item%2==0
)
type(a)