import os
import pandas as pd


PATH = 'D:/project/rltrader-master/data/c/'

tickers = pd.read_csv('D:/project/rltrader-master/output/c/port_A3C.csv')

tickers = list(tickers['ticker'])
tickers = list(map(lambda x: x[1:], tickers))

output = pd.DataFrame(columns=['ticker', '수익률'])

for ticker in tickers:
    df = pd.read_csv(PATH + ticker + '.csv', index_col=0)
    buy = df.loc['2016-01-04', 'close']
    close = df.loc['2019-12-30', 'close']

    ret = (close - buy) / buy * 100     # 수익률

    name = 'A'+ticker

    tmp = pd.DataFrame([[name, ret]], columns=['ticker', '수익률'])
    output = pd.concat([output, tmp])

output.to_csv('D:/project/rltrader-master/output/buy_and_hold_trainPeriod.csv', index=False, encoding='cp949')