import time
import win32com.client
import pandas as pd
import ctypes


class Creon:
    def __init__(self):
        self.obj_CpCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
        self.obj_CpCybos = win32com.client.Dispatch('CpUtil.CpCybos')
        self.obj_StockChart = win32com.client.Dispatch('CpSysDib.StockChart')

    def connectCheck(self):
        # 관리자 권한 여부 체크
        if ctypes.windll.shell32.IsUserAnAdmin():
            print('정상: 관리자권한으로 실행된 프로세스입니다.')
        else:
            print('오류: 일반권한으로 실행됨. 관리자 권한으로 실행해 주세요')
            return False

    def creon_7400_주식차트조회(self, code, date_from, date_to):
        # 연결 여부 체크
        if (self.obj_CpCybos.IsConnect == 0):
            print("연결 실패")
            return False

        list_field_key = [0, 1, 2, 3, 4, 5, 8]
        list_field_name = ['date', 'time', 'open', 'high', 'low', 'close', 'volume']
        dict_chart = {name: [] for name in list_field_name}

        self.obj_StockChart.SetInputValue(0, code)
        self.obj_StockChart.SetInputValue(1, ord('1'))  # 0: 개수, 1: 기간
        self.obj_StockChart.SetInputValue(2, date_to)  # 종료일
        self.obj_StockChart.SetInputValue(3, date_from)  # 시작일
        self.obj_StockChart.SetInputValue(5, list_field_key)  # 필드
        self.obj_StockChart.SetInputValue(6, ord('m'))  # 'D', 'W', 'M', 'm', 'T'
        self.obj_StockChart.SetInputValue(9, ord('1'))  # 수정주가 사용
        self.obj_StockChart.BlockRequest()

        # remainCount = self.obj_CpCybos.GetLimitRemainCount(1)  # 1 시세 제한
        # if remainCount <= 0:
        #     print('시세 연속 조회 제한 회피를 위해 sleep', self.obj_CpCybos.LimitRequestRemainTime)
        #     time.sleep(self.obj_CpCybos.LimitRequestRemainTime / 1000)

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

        print("차트: {} {}".format(cnt, dict_chart))
        return pd.DataFrame(dict_chart, columns=list_field_name)




if __name__ == '__main__':
    creon = Creon()

    # codeList = creon.obj_CpCodeMgr.GetStockListByMarket(1)  # 거래소
    codeList = ['A005930', 'A005380', 'A035420', 'A051910', 'A068270']
    codeList2 = creon.obj_CpCodeMgr.GetStockListByMarket(2)  # 코스닥

    start = '20180101'
    end = '20191231'

    print(creon.connectCheck())


    df = creon.creon_7400_주식차트조회(codeList[1], start, end)
    # df.to_csv("./data/COSPI/{}.csv".format(codeList[1][1:]), index=False)
    print(df)

    # for i, code in enumerate(codeList):
    #     df = creon.creon_7400_주식차트조회(code, start, end)
    #     df.to_csv("./data/COSPI/{}.csv".format(code[1:]), index=False)
    #     print(codeList)



# 추가:
# 1. ohlcv 외 데이터프레임을 구성할 다른 변수 고민(지표계산? 주체별 거래량 같은거 없나?)
# 2. 코스닥/코스피 구분하고 전종목 코드 가져오기
# 3. 반복문 이용해 전체 종목에 대한 데이터 가져오도록 코드 수정
