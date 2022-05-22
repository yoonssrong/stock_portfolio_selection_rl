import pandas as pd
import os
import re


PATH = 'D:/project/rltrader-master/output/p_a3c_test_모음/'

folders = os.listdir(PATH)

output = pd.read_csv('D:/project/rltrader-master/output/a3c_ticker.csv')

for folder in folders:
    print(folder)
    files = os.listdir(PATH+folder)
    log_file = [file for file in files if file.endswith(".log")]
    f = open(PATH+folder+f"/{log_file[0]}", 'r', encoding='utf-8')
    lines = f.readlines()

    target = [s for s in lines if "Epsilon" in s]

    target = pd.DataFrame(target)

    target['ticker'] = target[0].str.split(' ').str[0]
    target[f'{folder}'] = target[0].str.split(' ').str[8]
    target = target[['ticker', f'{folder}']]

    target['ticker'] = [i.replace('[', 'A') for i in target['ticker']]
    target['ticker'] = [i.replace(']AEpoch', '') for i in target['ticker']]
    target[f'{folder}'] = [i.replace('PV:', '') for i in target[f'{folder}']]

    output = pd.merge(output, target, how='left', on='ticker')

    f.close()

output.to_csv('./output/p_a3c_test_모음결과.csv', index=False, encoding='euc-kr')