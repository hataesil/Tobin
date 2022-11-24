class Account:
    def __init__(self, name, accountNum, balance):
        self.name = name
        self.__accountNum = accountNum
        self.__balance = balance

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        if(self.__balance < amount):
            return 1
        else:
            self.__balance -= amount
            return 0

    def print_accountInfo(self):
        return "{:>10} {:>10} {:>10}".format(self.name, self.__accountNum, self.__balance)

i = 0

number_count = 0

my_objects = []

while True:

    number_count = 0

    if(i == 3):
        break

    print("{:>10} {:>10} {:>10}".format("이름", "계좌번호", "잔고"))
    print("user{}: ".format(i+1), end='')

    name, accountNum, balance = input().split(' ')

    for k in accountNum:
        if(k.isnumeric()):
            number_count = number_count + 1

    if(len(accountNum) == 13 and number_count == 11 and accountNum[3] == '-' and accountNum[8] == '-'):
        my_objects.append(Account(name, accountNum, int(balance)))
        i = i + 1
    else:
        print("재입력")

for b in my_objects:
    print(b.print_accountInfo())

i = 0

my_list = [0, 0]

while True:

    if(i == 2):
        break

    i = 0

    print("사용자 이름 입력: ", end='')

    name1, name2 = input().split(' ')

    for idx, b in enumerate(my_objects):
        if(b.name == name1):
            i = i + 1
            my_list[0] = idx
        elif(b.name == name2):
            i = i + 1
            my_list[1] = idx

    if(i != 2):
        print("사용자가 없습니다.")
        print("다시 입력")
        continue

    while True:
        amount = int(input('출금액: '))

        if(my_objects[my_list[0]].withdraw(amount)):
            print("재입력")
        else:
            my_objects[my_list[1]].deposit(amount)
            break

print(my_objects[my_list[0]].print_accountInfo())
print(my_objects[my_list[1]].print_accountInfo())