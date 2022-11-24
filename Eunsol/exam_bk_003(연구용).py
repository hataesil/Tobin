# 은행 프로그램
import os

# 파일 입출력 방식
file = "C:/Tobin/Eunsol/Bank.txt"   # 폴더를 생성해서 시작할것
#f = open(file,"r")
all_id = list()


#한 사람의 계좌정보를 담아서 관리할 목적으로 구현되는 클래스
class Account:
    def __init__(self, name = "", userid= "", balance=0):        # 생성자
        if(userid == ""):
            self.name = input("계좌 소유자 이름을 입력하세요:")
            self.userid = input("생성할 계좌번호를 입력하세요:")
            self.balance = int(input("입금할 금액을 입력하세요:"))
        else:
            self.name = name
            self.userid = userid            
            self.balance = balance
            
    # 출력함수
    def disp(self):            
        print("계좌번호 : {0}  . 소유자: {1}  . 잔액 = {2}".format(self.userid, self.name, self.balance))
    
    # 데이터 호출 함수
    def info(self):
        return "{0}:{1}:{2}\n".format(self.name, self.userid,  self.balance)
    
    # 
    def getid(self):
        return self.userid
   
    # 입금
    def deposit(self, money):
        self.balance += money
        return self.balance
    
    # 출금
    def withdraw(self, money):
        if self.balance < money:
            return 0
        else:
            self.balance -= money
            return money
    
    # 잔액 조회
    def getBalance(self):     
        return self.balance

###########################
# 저장된 계좌 파일 호출                 
try:
    f = open(file,"r")
    
    while True:
        line = f.readline()
        if not line:
            break

        a,b,c = line.split(":")
        all_id.append(Account(a,b,int(c)))
    f.close()
except Exception as ex:
    print("파일 없습니다")
    print(ex)
    
###########################
# 화면 초기화                 
def clr():
    os.system('cls')
    
###########################
# 계좌정보를 이용하여 구현될 기능을 담고 있는 클래스 멤버필드 
# 멤버메서드 : makeAccount() - 계좌개설을 담당할 메서드
class BankManager:
    # 출금처리를 담당할 메서드
    def withdraw(self,userid):    
        for i in all_id:
            if i.getid() == userid:
                money = int(input("출금금액 = "))
                return i.withdraw(money)
        print("해당하는 계좌가 없습니다.")
        
    # 입금처리를 담당할 메서드
    def deposit(self,userid):     
        for i in all_id:
            if i.getid() == userid:
                money = int(input("입금금액 = "))
                bal = i.deposit(money)
                print("잔액은 {0} 입니다.".format(bal))
                return 0
        print("일치하는 계좌번호가 존재하지 않습니다")
    
    # 계좌번호의 중복여부를 판단할 메서드
    def new_id(self,user):             
        for i in all_id:
            if i.getid() == user.getid():
                return "중복된 계좌번호이므로 다시 입력하십시요."
            
        all_id.append(user)
        return "계좌 개설이 완료되었습니다."

    # 전체고객의 계좌정보를 출력할 메서드
    def showAccount(self):             
        if len(all_id) != 0:
            for i in range(0,len(all_id)):
                all_id[i].disp()
        else:
            print("보유한 계좌가 없습니다.")

                 
    # 파일 저장 메서드
    def save(self):
        f = open(file,"w")
        for i in all_id:
            f.write(i.info())
            
        f.close()
            
############################
# 사용자와의 인터페이스를 담당할 목적의 클래스
class BanckingSystem: 
    def run():
        while True:
            print("=======================================")
            print("          SOOKMYUNG BANK ATM           ")
            print("=======================================")
            print("1. 신규계좌생성")
            print("2. 잔액조회")
            print("3. 입금")
            print("4. 출금")
            print("5. 거래내역 조회")
            print("6. 종료")
            print("--------------------")
            cho = input("입력: ")
            if cho == "1":       # 신규계좌개설
                clr()
                print("=======계좌개설=======")
                print(BankManager().new_id(Account()))
                print("===================")

            elif cho == "2":  # 잔액조회
                clr()
                print("========조 회========")
                BankManager().showAccount()
                print("===================")               
                
            elif cho == "3":     # 입금
                clr()
                print("========입 금========")
                userid = input("계좌번호 =")
                BankManager().deposit(userid)
                print("===================")
                 
                
            elif cho == "4":    # 출금
                clr()
                print("========출 금========")
                userid = input("계좌번호 =")
                a = BankManager().withdraw(userid)
                if a != None:
                    print("{0}원 출금하셨습니다.".format(a))
                

                
            elif cho == "6":  # 종료
                BankManager().save()
                print("종료")
                break

##############################
if __name__ =='__main__':
    BanckingSystem.run()