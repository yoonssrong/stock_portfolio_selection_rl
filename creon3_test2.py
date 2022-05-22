### 30분봉 차트 다운로드 테스트

import sys
from PyQt5.QtWidgets import *
import win32com.client
from pandas import Series, DataFrame
import pandas as pd
import os, time

g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
g_objCpStatus = win32com.client.Dispatch('CpUtil.CpCybos')

class CpStockChart:
    def __init__(self):
        self.objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

    # 차트 요청 - 분간, 틱 차트
    def RequestMT(self, code, caller):
        # 연결 여부 체크
        bConnect = g_objCpStatus.IsConnect
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")
            return False

        self.objStockChart.SetInputValue(0, code)  # 종목코드
        self.objStockChart.SetInputValue(1, ord('0'))  # 0: 개수, 1: 기간
        # self.objStockChart.SetInputValue(2, '20191231')  # 종료일
        # self.objStockChart.SetInputValue(3, '20180101')  # 시작일
        self.objStockChart.SetInputValue(4, 500)  # 조회 개수
        self.objStockChart.SetInputValue(5, [0, 1, 2, 3, 4, 5, 8])  # 요청항목 - 날짜, 시간,시가,고가,저가,종가,거래량
        self.objStockChart.SetInputValue(6, ord('m'))  # '차트 주기 - 분/틱
        self.objStockChart.SetInputValue(7, 30)  # 분틱차트 주기
        self.objStockChart.SetInputValue(9, ord('1'))  # 수정주가 사용

        sumcnt = 0
        caller.datachart = None
        caller.datachart = pd.DataFrame(columns=('date', 'time', 'open', 'high', 'low', 'close', 'volume'))

        while True:
            remainCount = g_objCpStatus.GetLimitRemainCount(1)  # 1 시세 제한
            if remainCount <= 0:
                print('시세 연속 조회 제한 회피를 위해 sleep', g_objCpStatus.LimitRequestRemainTime)
                time.sleep(g_objCpStatus.LimitRequestRemainTime / 1000)

            self.objStockChart.BlockRequest()

            # 현재가 통신 및 통신 에러 처리
            rqStatus = self.objStockChart.GetDibStatus()
            rqRet = self.objStockChart.GetDibMsg1()
            print("통신상태", rqStatus, rqRet)
            if rqStatus != 0:
                return False

            cnt = self.objStockChart.GetHeaderValue(3)
            sumcnt += cnt

            for i in range(cnt):
                item = {}
                item['date'] = self.objStockChart.GetDataValue(0, i)
                item['time'] = self.objStockChart.GetDataValue(1, i)
                item['open'] = self.objStockChart.GetDataValue(2, i)
                item['high'] = self.objStockChart.GetDataValue(3, i)
                item['low'] = self.objStockChart.GetDataValue(4, i)
                item['close'] = self.objStockChart.GetDataValue(5, i)
                item['volume'] = self.objStockChart.GetDataValue(6, i)

                caller.datachart.loc[len(caller.datachart)] = item

            # 1000 개 정도만 처리
            if sumcnt > 30000:
                break;
            # 연속 처리
            if self.objStockChart.Continue != True:
                break

        caller.datachart = caller.datachart.set_index('date')
        # 인덱스 이름 제거
        caller.datachart.index.name = None
        print(caller.datachart)
        return True


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PLUS API TEST')
        self.setGeometry(300, 300, 300, 290)
        self.isSB = False
        self.objCur = []

        self.datachart = DataFrame()
        self.objChart = CpStockChart()

        self.codeEdit = QLineEdit("", self)
        self.codeEdit.move(20, 20)
        self.codeEdit.textChanged.connect(self.codeEditChanged)
        self.codeEdit.setText('코드')
        self.label = QLabel('종목코드', self)
        self.label.move(140, 20)

        btchart3 = QPushButton("분차트 요청", self)
        btchart3.move(20, 120)
        btchart3.clicked.connect(self.btchart3_clicked)

        btchart7 = QPushButton("엑셀로 저장", self)
        btchart7.move(20, 170)
        btchart7.clicked.connect(self.btchart7_clicked)

        btnExit = QPushButton("종료", self)
        btnExit.move(20, 220)
        btnExit.clicked.connect(self.btnExit_clicked)

        self.setCode('000660')

    # 분차트 받기
    def btchart3_clicked(self):
        if self.objChart.RequestMT(self.code, self) == False:
            exit()


    def btchart7_clicked(self):
        code = self.code[1:]
        charfile = './data/raw/ohlcv_30m/{}.csv'.format(code)
        print(len(self.datachart.index))
        self.datachart.to_csv(charfile, encoding="euc-kr", index=True)
        return

    def codeEditChanged(self):
        code = self.codeEdit.text()
        self.setCode(code)

    def setCode(self, code):
        if len(code) < 6:
            return

        print(code)
        if not (code[0] == "A"):
            code = "A" + code

        name = g_objCodeMgr.CodeToName(code)
        if len(name) == 0:
            print("종목코드 확인")
            return

        self.label.setText(name)
        self.code = code

    def btnExit_clicked(self):
        exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()

    codeList = ['005930', '000660']

    for code in codeList:
        # 종목 설정
        myWindow.setCode(code)
        # 차트 불러오기
        myWindow.btchart3_clicked()
        # 차트 저장
        myWindow.btchart7_clicked()

    # 윈도우 종료
    myWindow.btnExit_clicked()

    app.exec_()