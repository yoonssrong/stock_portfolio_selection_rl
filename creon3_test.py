import time
import win32com.client
import pandas as pd


class Creon:
    def __init__(self):
        self.obj_CpCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
        self.obj_CpCybos = win32com.client.Dispatch('CpUtil.CpCybos')
        self.obj_StockChart = win32com.client.Dispatch('CpSysDib.StockChart')

    def creon_7400_주식차트조회(self, code, date_from, date_to):
        b_connected = self.obj_CpCybos.IsConnect
        if b_connected == 0:
            print("연결 실패")
            return None

        list_field_key = [0, 1, 2, 3, 4, 5, 8] # 요청항목 - 날짜,시간,시가,고가,저가,종가,거래량
        list_field_name = ['date', 'time', 'open', 'high', 'low', 'close', 'volume']
        dict_chart = {name: [] for name in list_field_name}

        self.obj_StockChart.SetInputValue(0, 'A'+code) # 종목코드
        self.obj_StockChart.SetInputValue(1, ord('1'))  # 0: 개수, 1: 기간
        self.obj_StockChart.SetInputValue(2, date_to)  # 종료일
        self.obj_StockChart.SetInputValue(3, date_from)  # 시작일
        self.obj_StockChart.SetInputValue(4, 500)  # 조회 개수
        self.obj_StockChart.SetInputValue(5, list_field_key)  # 필드
        self.obj_StockChart.SetInputValue(6, ord('m'))  # 'D', 'W', 'M', 'm', 'T'
        self.obj_StockChart.SetInputValue(7, 30)  # 분틱차트 주기
        self.obj_StockChart.SetInputValue(9, ord('1'))  # 수정주가 사용
        self.obj_StockChart.BlockRequest()

        status = self.obj_StockChart.GetDibStatus()
        msg = self.obj_StockChart.GetDibMsg1()
        print("통신상태: {} {}".format(status, msg))
        if status != 0:
            return None

        cnt = self.obj_StockChart.GetHeaderValue(3)  # 수신개수
        for i in range(cnt):
            dict_item = (
                {name: self.obj_StockChart.GetDataValue(pos, i)
                for pos, name in zip(range(len(list_field_name)), list_field_name)}
            )
            for k, v in dict_item.items():
                dict_chart[k].append(v)

        return pd.DataFrame(dict_chart, columns=list_field_name)


if __name__ == '__main__':
    creon = Creon()
    code = '005380'

    # years = list(range(2015, 2016))
    #
    # for year in years:
    #     startdate = str(year) + '0101'
    #     enddate = str(year) + '1231'
    #     df = creon.creon_7400_주식차트조회(code, startdate, enddate)
    #     print(df)
    #     df.to_csv("./data/raw/priceperhour/pph_{}_{}.csv".format(code, year), index=False)

    startdate = '20190101'
    enddate = '20201231'
    df = creon.creon_7400_주식차트조회(code, startdate, enddate)
    print(df)
    # df.to_csv("./data/raw/priceperhour/pph_{}.csv".format(code), index=False)
