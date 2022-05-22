import pandas as pd
import pandas_datareader as pdr

api_key = '4uyBm_E4CG_K_1HxCUgz'

# 국제 금 가격(런던 금시장)
# df_gold = pdr.DataReader('GOLDAMGBD228NLBM', 'fred', start='2015-01-01')
df_gold = pdr.DataReader('LBMA/GOLD', 'quandl', start='2015-01-01', api_key=api_key)
df_gold = df_gold.iloc[:, 0:1]

# 국제 은 가격
df_silver = pdr.DataReader('LBMA/SILVER', 'quandl', start='2015-01-01', api_key=api_key)
df_silver = df_silver.iloc[:, 0:1]

# 국제 원유 가격(WTI 선물)
df_oil = pdr.DataReader('CHRIS/CME_CL1', 'quandl', start='2015-01-01', api_key=api_key)
df_oil = df_oil.iloc[:, [5]]

result = pd.concat([df_gold, df_silver, df_oil], axis=1)
result = result.rename({'USDAM':'Gold', 'USD':'Silver', 'Settle':'Oil'}, axis='columns')

result.to_csv("./data/raw/GSO.csv", index=True)
