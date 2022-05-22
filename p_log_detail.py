import pandas as pd
import os
from tqdm import tqdm


PATH = 'D:/project/rltrader-master/output/p_dqn_train/'

folders = os.listdir(PATH)  # 전체 종목
# folders = ['017670', '030000', '030200', '032640', '035420', '036570', '079160', '214320']  # 커뮤니케이션서비스
# folders = ['000670', '001230', '004020', '005490', '010130', '014820', '103140']    # 철강/소재

folders = tqdm(folders)

output = pd.DataFrame(columns=['ticker', 'Buy', 'Sell', 'Hold', 'LC'])

# tmpBuy = 0
# tmpSell = 0
# tmpHold = 0
# tmpLC = 0

for i, folder in enumerate(folders):
    workPATH = os.path.join(PATH, folder)

    log = open(os.path.join(workPATH, f'{folder}.log'), 'rt')
    fileLines = log.readlines()
    r = [s for s in fileLines if "Epsilon" in s]

    df = pd.DataFrame(r)
    df = df[0].str.split(' ', expand=True)

    # 필요없는 문자열 지우기
    df[4] = [s.replace('#Buy:', '') for s in df[4]]
    df[5] = [s.replace('#Sell:', '') for s in df[5]]
    df[6] = [s.replace('#Hold:', '') for s in df[6]]
    df[9] = [s.replace('LC:', '') for s in df[9]]

    tmpBuy = df[4].astype(int).mean()
    tmpSell = df[5].astype(int).mean()
    tmpHold = df[6].astype(int).mean()
    tmpLC = df[9].astype(float).mean()

    tmp_df = pd.DataFrame([{'ticker':'A'+folder, 'Buy':tmpBuy, 'Sell':tmpSell, 'Hold':tmpHold, 'LC':tmpLC}])
    output = pd.concat([output, tmp_df])

print(output)
output.to_csv('D:/project/rltrader-master/output/ANOVA/dqn.csv', index=False)

# print(meanBuy)
# print(meanSell)
# print(meanHold)
# print(meanLC)