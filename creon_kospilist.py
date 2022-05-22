import win32com.client
import pandas as pd

instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
codeList = instCpCodeMgr.GetStockListByMarket(1)

kospi = pd.DataFrame(columns=['code', 'secondCode', 'name'])

for i, code in enumerate(codeList):
    secondCode = instCpCodeMgr.GetStockSectionKind(code)
    name = instCpCodeMgr.CodeToName(code)
    df = pd.DataFrame([[code, secondCode, name]], columns=['code', 'secondCode', 'name'])
    kospi = kospi.append(df)

print(kospi)
# kospi.to_csv('./data/kospi.csv', index=False, encoding='euc-kr')
