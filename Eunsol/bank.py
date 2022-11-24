

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

while True :
    print("""========================================
    print      SOOKMYUNG BACK ATM
========================================
1. 신규 계좌 생성
2. 잔액 조회
3. 입금
4. 출금
5. 거래 내역 조회
6. 종료
-----------------------------------------""")
    
    
