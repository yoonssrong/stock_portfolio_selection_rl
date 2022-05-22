# p_log_detail test폴더

import pandas as pd
import os
import glob


PATH = 'D:/project/rltrader-master/output/test모음/'

df = pd.read_csv(PATH + 'p_dqn_test_모음결과.csv')
df = df.drop(['max'], axis=1)

target = pd.DataFrame(columns=['ticker', 'best'])

for i, row in df.iterrows():
    best = row[row.isnull()==False].index[1]
    tmp = pd.DataFrame([{'ticker':row[0], 'best':best}])
    target = pd.concat([target, tmp])

df1 = []

for i, row in target.iterrows():
    ticker = row[0]
    folder = row[1]

    workPATH = os.path.join(PATH, 'p_dqn_test_모음', folder)

    logName = r"{}/*.log".format(workPATH)
    log = open(glob.glob(logName)[0], 'rt', encoding='UTF8')
    fileLines = log.readlines()

    r = [s for s in fileLines if f'[{ticker[1:]}][Epoch 1/1]' in s]

    df1.append(r[0])

df1 = pd.DataFrame(df1)
df1 = df1[0].str.split(' ', expand=True)

df1[4] = [s.replace('#Buy:', '') for s in df1[4]]
df1[5] = [s.replace('#Sell:', '') for s in df1[5]]
df1[6] = [s.replace('#Hold:', '') for s in df1[6]]

meanBuy = df1[4].astype(int).mean()
meanSell = df1[5].astype(int).mean()
meanHold = df1[6].astype(int).mean()

print(df1)
print(meanBuy)
print(meanSell)
print(meanHold)
