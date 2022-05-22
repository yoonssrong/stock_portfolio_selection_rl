import pandas as pd
import os

PATH = 'D:/project/rltrader-master/output/p_dqn_train/'

folders = os.listdir(PATH)

output = pd.DataFrame(columns=['ticker', 'PV'])

for folder in folders:
    f = open(PATH+folder+f"/{folder}.log", 'r', encoding='utf-8')
    lines = f.readlines()
    line = lines[-2:-1]
    f.close()

    line = line[0].split(' ')
    ticker = 'A'+str(line[0][1:7])
    PV = line[8][3:]

    df = pd.DataFrame([[ticker, PV]], columns=['ticker', 'PV'])
    output = output.append(df)

output.to_csv('./output/p_dqn_train.csv', index=False, encoding='euc-kr')
print(output)
