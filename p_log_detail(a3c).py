import pandas as pd
import os


target = os.listdir('D:/project/rltrader-master/output/p_dqn_train/')

# target = ['017670', '030000', '030200', '032640', '035420', '036570', '079160', '214320']  # 커뮤니케이션서비스
# target = ['000670', '001230', '004020', '005490', '010130', '014820', '103140']    # 철강/소재

log = open('D:/project/rltrader-master/output/p_a3c_train/20210830193130.log', 'rt')
fileLines = log.readlines()

output = pd.DataFrame(columns=['ticker', 'Buy', 'Sell', 'Hold', 'LC'])
for i in target:
    r1 = [s for s in fileLines if f"[{i}][Epoch " in s]

    df1 = pd.DataFrame(r1)
    df1 = df1[0].str.split(' ', expand=True)

    df1[9] = [s.replace('LC:', '') for s in df1[9]]

    meanLC = df1[9].astype(float).mean()

    df1[4] = [s.replace('#Buy:', '') for s in df1[4]]
    df1[5] = [s.replace('#Sell:', '') for s in df1[5]]
    df1[6] = [s.replace('#Hold:', '') for s in df1[6]]

    meanBuy = df1[4].astype(int).mean()
    meanSell = df1[5].astype(int).mean()
    meanHold = df1[6].astype(int).mean()

    tmp_df = pd.DataFrame([{'ticker': 'A'+i, 'Buy': meanBuy, 'Sell': meanSell, 'Hold': meanHold, 'LC': meanLC}])
    output = pd.concat([output, tmp_df])

print(output)
output.to_csv('D:/project/rltrader-master/output/ANOVA/a3c.csv', index=False)

# r2 = [s for s in fileLines if "Epoch 100/100" in s]
# df2 = pd.DataFrame(r2)
# df2 = df2[0].str.split(' ', expand=True)
#
# df2[4] = [s.replace('#Buy:', '') for s in df2[4]]
# df2[5] = [s.replace('#Sell:', '') for s in df2[5]]
# df2[6] = [s.replace('#Hold:', '') for s in df2[6]]
#
# meanBuy = df2[4].astype(int).mean()
# meanSell = df2[5].astype(int).mean()
# meanHold = df2[6].astype(int).mean()
#
# print(df2[:6])
#
# print(meanBuy)
# print(meanSell)
# print(meanHold)
# print(meanLC)