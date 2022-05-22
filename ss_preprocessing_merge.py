import pandas as pd
import os

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# 합칠 종목
code = '090430'

# 저장할 경로
savepath = 'D:/project/rltrader-master/data/c/'

# 파일 불러오기
path1 = 'D:/project/rltrader-master/data/raw/ohlcv/ohlcv_{}.csv'.format(code)            # 시고저종
file1 = pd.read_csv(path1)

path2 = 'D:/project/rltrader-master/data/raw/priceperhour_pre/pph_{}.csv'.format(code)   # 시간별가격
file2 = pd.read_csv(path2)

path3 = 'D:/project/rltrader-master/data/raw/investor/inv_{}.csv'.format(code)           # 투자주체
file3 = pd.read_csv(path3, encoding='cp949')

path4 = 'D:/project/rltrader-master/data/raw/GSO.csv'                                    # 금은원유가격
file4 = pd.read_csv(path4)

# 전처리 : 중복컬럼 제거 및 컬럼명 변경
file1 = file1[file1.columns.difference(['time'])]
file3 = file3[file3.columns.difference(['close'])]
file3 = file3.rename({'개인':'individual',
                      '외국인':'foreign',
                      '국가,지자체':'government',
                      '금융투자':'financial',
                      '기관계':'institutional',
                      '기타금융':'otherFinancial',
                      '기타법인':'legal',
                      '기타외인':'otherForeign',
                      '보험':'insurance',
                      '연기금':'pensionFund',
                      '은행':'bank',
                      '투신':'investment'}, axis='columns')

# 파일 합치기
final = pd.merge(file1, file2, how='inner', on='date')
final = pd.merge(final, file3, how='inner', on='date')
final = pd.merge(final, file4, how='inner', on='date')

# 정렬 및 저장
final.sort_values(by=['date'], ascending=True, inplace=True)
final = final[['date', 'open', 'high', 'low', 'close', 'volume',
               'p9', 'p10', 'p11', 'p12', 'p13', 'p14', 'p15',
               'individual', 'foreign', 'institutional', 'financial', 'insurance', 'investment', 'bank', 'otherFinancial', 'pensionFund', 'government', 'legal', 'otherForeign',
               'Gold', 'Silver', 'Oil']]
final.to_csv(savepath + '{}.csv'.format(code), index=False, encoding='cp949')
print(final)
