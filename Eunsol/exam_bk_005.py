class Account:
    
    def __init__(self,i_d,name,balance):    #생성자
        self.i_d = i_d                      #계좌번호
        self.name = name                    #이름
        self.balance = balance               #잔고
     
    def print_info(self):
        print("이름 : ",self.name)             #고객정보
        print("계좌번호 : ",self.i_d)
        print("잔고 : ",self.balance)
        
    def get_info():
        print("정보를 입력해주세요")       #정보확인을 위한 함수.
        i_d = input("계좌 번호 : ") 
        name = input("이름 : ")
        return i_d,name                        #계좌번호랑 이름을 반환.

 

#사용자 메뉴

def view():
    account_list = []  #정보를 담을 배열 생성.
    while True:         #True를 통한 무한 반복.
        choose = int(input("1. 계좌개설 2. 입금처리 3. 출금처리 4. 전체고객 잔액현황 5. 프로그램 종료"))
       #사용자에게 입력받은 수를 int형으로 형변환 후 변수 choose에 넣는다 .(형변환 안할때 문자타입)

        if choose == 1:   # 고객 등록
            c_register=register(account_list)   #고객 등록함수 호출.
            account_list.append(c_register)    #리스트에 리턴받은 값을 넣는다.
        
        elif choose ==2:  # 입금
            account_list=deposit(account_list)  #입금 함수 호출.
        
        elif choose ==3:  # 출금
            c_withdraw=withdraw(account_list) #출금 함수 호출.
        
        elif choose == 4:  # 잔고                 #잔고 함수 호출.
            getBalance(account_list)
            
        elif choose == 5:  #종료                  #break를 통해 반복문을 나감.
                break
                
if __name__ == "__main__":   #인터프리터에서 실행시를 위한 실행문.
    view()

#계좌개설
def register(account_list):  #고객정보를 매개변수로 받는다.
    i_d = input("계좌 번호 : ")  #각각 입력받은 정보를 변수에 담는다.
    name = input("이름 : ")
    balance = int(input("예금 금액 : "))
    for i,account in  enumerate(account_list):   #기존의 고객정보를 for문을 통해 계좌정보 중복 검사.
        if account.i_d == i_d:  
            account_list[i]
            print("id가중복됩니다.")
            register()                                     # register 본인을 호출 위에서부터 다시 시작.
            
    account = Account(i_d, name, balance)      #중복이 없을때 Account타입으로 변수에 넣는다.
    print("계좌 개설이 완료되었습니다.")
            
    return account                                      #Account 타입의 변수 account를 반환.


 
#입금처리
def deposit(account_list):
    i_d,name = Account.get_info()                                #기본클래스의 개인 정보 확인 함수 호출.
    
    for i,account in  enumerate(account_list):                   #반복문을 통한 개인정보 확인.
        if account.name == name and account.i_d == i_d:  # id와 name 모두 같을때 if 진입.
            account_list[i] 
            print("정보가 확인 되었습니다")
            
            money=int(input("입금하실 금액을 입력해주세요 : ")) #입금 할 금액을 입력받음. 
            account_list[i].balance += money   #기존의 잔고에 입력받은 금액을 더하여 저장.
            print("입금처리가 완료되었습니다.")
            return account_list                      #잔고가 업데이트된 리스트를 반환.
                    
        else:
            print("입력하신 정보가 맞지 않습니다.")       #개인 정보 확인 함수에 입력한 id와name이
            break                                                   #일치하지않을때 반복문 종료.
             

#출금처리                       #대부분의 코드가 입금처리와 같다.
def withdraw(account_list):               
    i_d,name = Account.get_info()
    
    for i,account in  enumerate(account_list):
        if account.name == name and account.i_d == i_d:
            account_list[i]
            print("정보가 확인 되었습니다")
            
            money=int(input("출금하실 금액을 입력해주세요 : "))
            a=account_list[i].balance - money      #입금처리와 다른 부분.
            if(a<0):                                        #계산후의 잔고가 0보다 작다면 안내문 출력
                print("잔액이 부족합니다.")
            else:                                            #문제가 없다면 정상처리
                account_list[i].balance -= money           
                print("출금처리가 완료되었습니다.")
                return account_list                      #잔고가 업데이트된 리스트 반환

        else:
            print("입력하신 정보가 맞지 않습니다.")
            break

 

#전체고객 잔액현황
def getBalance(account_list):         # 고객 리스트를 매개변수로 받는다.
    for account in account_list:       # 현재 있는 고객의 정보만큼 반복. 
        account.print_info()             # 기본클래스의 함수 사용.
        print("========출력되었습니다.======")