import matplotlib.pyplot as plt
from old_model.Scrab import Scrab
from dateutil.parser import parse
import datetime

if __name__ == '__main__':
    a = Scrab()
    text = a.scrab('233740', 'Kosdaq leverage')
    alter = a.scrab('251340', 'Kosdaq inverse')
    kosdaq = a.scrab('kosdaq', '')

    start_date = int(input("시작할 일시를 입력해주세요."))
    end_date = int(input("종료할 일시를 입력해주세요."))

    initial_balance = 2000000
    balance = initial_balance
    safebox = 0
    balance_history = []
    kosdaq_history = []

    stock = 0
    date_history = []

    count = 0
    count_1 = -1
    count_2 = -1
    initial_kosdaq = 0

    temp = 0
    win = 0
    win_streak = 0
    yesterday = 0
    score = 0

    for data in kosdaq:
        if data[0] < start_date:
            count_1 += 1
            continue

        if data[0] >= start_date:
            initial_kosdaq = data[2]
            break

    for data in alter:
        if data[0] < start_date:
            count_2 += 1
            continue
        if data[0] >= start_date:
            break

    tmp = False

    for data in text:
        if data[0] < start_date:
            continue

        count += 1

        count_1 += 1
        count_2 += 1

        if tmp is False:
            if yesterday < data[1]:
                win += 1
                win_streak += 1
                print("win")
            else:
                win_streak = 0
                print('lose')
            balance -= stock * data[1] * (0.015 / 100)
            balance += stock * data[1]
            stock = 0
        else:
            balance -= stock * alter[count_2][4] * (0.015 / 100)
            balance += stock * alter[count_2][4]
            stock = 0
            tmp = False

        now_balance = safebox + balance
        if score >= 2:
            balance = now_balance * 1
            safebox = now_balance - balance
        elif score < 0:
            balance = now_balance * 0.6
            safebox = now_balance - balance
        else:
            balance = now_balance * 0.3
            safebox = now_balance - balance

        kosdaq_history.append(kosdaq[count_1][4] / initial_kosdaq)
        date_history.append(parse(str(data[0])))
        balance_history.append(now_balance/initial_balance)

        if data[0] > end_date:
            break

        sumof = [0, 0, 0, 0]
        for i in range(20):
            if i <= 1:
                sumof[0] += kosdaq[count_1 - i][4]
            if i <= 4:
                sumof[1] += kosdaq[count_1 - i][4]
            if i <= 9:
                sumof[2] += kosdaq[count_1 - i][4]
            sumof[3] += kosdaq[count_1 - i][4]

        sumof[0] /= 2
        sumof[1] /= 5
        sumof[2] /= 10
        sumof[3] /= 20

        score = 0
        for a, i in enumerate(sumof):
            scoreboard = [1, 1, 1, -2]
            if kosdaq[count_1][4] > i:
                score += scoreboard[a]

        if score <= 2:
            stock  = balance // data[4]
            balance -= stock * data[4]
            yesterday = data[4]

    plt.figure()
    plt.plot(date_history, balance_history)
    plt.plot(date_history, kosdaq_history)
    plt.title("Balance Graph")
    plt.xlabel("Date")
    plt.ylabel("Balance")
    plt.show()
    print(win/count * 100)
    print(balance_history)
