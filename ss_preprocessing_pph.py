import pandas as pd
import os

path = 'D:/project/rltrader-master/data/raw/priceperhour_raw/'
savepath = 'D:/project/rltrader-master/data/raw/priceperhour_pre/'

files = os.listdir(path)

for i, file in enumerate(files):
    data = pd.read_csv(path + file, thousands=',', header=0, converters={'date': lambda x: str(x)})
    dates = set(data['date'].tolist())
    final = pd.DataFrame(columns=['date', 'p9', 'p10', 'p11', 'p12', 'p13', 'p14', 'p15'])

    for j, date in enumerate(dates):
        target = data.loc[data['date'] == date]

        if len(target['time']) == 6 and target.iloc[0, 1] == 1500:
            p9 = target.iloc[5, 2]
            p10 = target.iloc[4, 2]
            p11 = target.iloc[3, 2]
            p12 = target.iloc[2, 2]
            p13 = target.iloc[1, 2]
            p14 = target.iloc[0, 2]
            p15 = target.iloc[0, 5]

        elif len(target['time']) == 6 and target.iloc[0, 1] == 1600:
            p9 = target.iloc[5, 2]
            p10 = target.iloc[4, 2]
            p11 = target.iloc[3, 2]
            p12 = target.iloc[2, 2]
            p13 = target.iloc[1, 2]
            p14 = target.iloc[0, 2]
            p15 = target.iloc[0, 5]

        elif len(target['time']) == 7 and target.iloc[0, 1] == 1530:
            p9 = target.iloc[6, 2]
            p10 = target.iloc[5, 2]
            p11 = target.iloc[4, 2]
            p12 = target.iloc[3, 2]
            p13 = target.iloc[1, 2]
            p14 = target.iloc[0, 2]
            p15 = target.iloc[0, 5]

        elif len(target['time']) == 7 and target.iloc[0, 1] == 1630:
            p9 = target.iloc[6, 2]
            p10 = target.iloc[5, 2]
            p11 = target.iloc[4, 2]
            p12 = target.iloc[3, 2]
            p13 = target.iloc[1, 2]
            p14 = target.iloc[0, 2]
            p15 = target.iloc[0, 5]

        elif len(target['time']) == 6 and target.iloc[0, 1] == 1530:
            p9 = target.iloc[5, 2]
            p10 = target.iloc[5, 2]
            p11 = target.iloc[4, 2]
            p12 = target.iloc[3, 2]
            p13 = target.iloc[1, 2]
            p14 = target.iloc[0, 2]
            p15 = target.iloc[0, 5]

        elif len(target['time']) == 5:
            p9 = target.iloc[4, 2]
            p10 = target.iloc[4, 2]
            p11 = target.iloc[3, 2]
            p12 = target.iloc[2, 2]
            p13 = target.iloc[1, 2]
            p14 = target.iloc[0, 2]
            p15 = target.iloc[0, 5]

        df = pd.DataFrame([[date, p9, p10, p11, p12, p13, p14, p15]], columns=['date', 'p9', 'p10', 'p11', 'p12', 'p13', 'p14', 'p15'])
        final = pd.concat([final, df])

    print(final)
    final.sort_values(by=['date'], ascending=True, inplace=True)
    final.to_csv(savepath + file, index=False)
