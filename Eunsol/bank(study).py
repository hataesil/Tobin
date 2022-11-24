
file = "C:/Tobin/Eunsol/Bank.txt"   # 폴더를 생성해서 시작할것
all_id = []

class Account :
    def _init_(self, name, number, balance, history) :
        self.name = name
        self.number = number
        self.balance = balance
        self.history = []
        history.append(("신규", balance, balance))
        bank = {}
        bank[self.name] = Account
    def _str_(self) :
        msg = "계좌번호 :" + self.number ," 소유자 :" + self.name, " 잔액 =" + self.balance
        return msg
    def deposit(self, amount) :
        self.balance += amount
        self.history.append(("입금", amount, self.balance))
        print(amount, "원이 입금되었습니다.")
    def withdraw(self, amount) :
        if amount <= self.balance :
            self.balance -= amount
            self.history.append("출금", amount, self.balance)
            print(amount, "원이 출금되었습니다.")
        else :
            print("잔액이 부족합니다.")


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
               
                print("=======계좌개설=======")
                print(BankManager().new_id(Account()))
                print("===================")

            elif cho == "2":  # 잔액조회
                
                print("========조 회========")
                BankManager().showAccount()
                print("===================")               
                
            elif cho == "3":     # 입금
                
                print("========입 금========")
                userid = input("계좌번호 =")
                BankManager().deposit(userid)
                print("===================")
                 
                
            elif cho == "4":    # 출금
                
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
    
    
