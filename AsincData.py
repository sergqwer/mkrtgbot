import os
from os import path
from handlers import warning_msg


chat_id = '667281903'
def check_inform():
    print('Начанаю работать')
    file = open(f'C://Xevil//keys.txt', 'r')
    alluserkeys = file.read().splitlines()
    for item in alluserkeys:
        try:
            file = open(f'C://Xevil//Keys_Xevil//{item}//Balance.txt', 'r')
            balance = float(file.read())
        except:
            file = open(f'C://Xevil//Keys_Xevil//{item}//Balance.txt', 'w')
            file.write('0')
            balance = float(0)
        balance = round(balance, 2)
        try:
            file = open(f'C://Xevil//Keys_Xevil//{item}//HCAPTCHA_PAY.txt', 'r')
            hcaptcha = float(file.read())
            file = open(f'C://Xevil//Keys_Xevil//{item}//RECAPTCHA_PAY.txt', 'r')
            recaptcha = float(file.read())
            file = open(f'C://Xevil//Keys_Xevil//{item}//IMGCAPTCHA_PAY.txt', 'r')
            imgcaptcha = float(file.read())
        except:
            print(f'Ошибка при списании с {item}')
        else:
            with file:
                moneyforh = (hcaptcha * 0.03)
                moneyforre = (recaptcha * 0.02)
                moneyforimg = (imgcaptcha * 0.001)
                allmoneycaptcha = (moneyforh + moneyforimg + moneyforre)
                allmoneycaptcha = round(allmoneycaptcha, 2)
        pay_balance = balance - allmoneycaptcha
        pay_balance = round(pay_balance, 2)
        if pay_balance > 0:
            file = open(f'C://Xevil//Keys_Xevil//{item}//Balance.txt', 'w')
            file.write(str(pay_balance))
            file = open(f'C://Xevil//Keys_Xevil//{item}//PAY.txt', 'w')
            file.write(str(100))
            file = open(f'C://Xevil//Keys_Xevil//{item}//HCAPTCHA_PAY.txt', 'w')
            file.write('0')
            file = open(f'C://Xevil//Keys_Xevil//{item}//RECAPTCHA_PAY.txt', 'w')
            file.write('0')
            file = open(f'C://Xevil//Keys_Xevil//{item}//IMGCAPTCHA_PAY.txt', 'w')
            file.write('0')
            print(f'Списания с {item} произошло успешно')
        else:
            print(f'Недостаточно денег для списания с {item}')
            for filename in os.listdir("C://Xevil//chat_id"):
                if ".tmp" not in filename:
                    with open(os.path.join("C://Xevil//chat_id", filename), 'r') as f:
                        text = f.read()
                        if str(text) == str(item):
                            ather_chat_id = path.splitext(filename)[0]
                            warning_msg(chat_td=chat_id, text=f'У пользователя {item} недостаточно денег')



