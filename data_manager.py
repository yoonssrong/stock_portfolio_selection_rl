import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, RobustScaler


# COLUMNS_CHART_DATA = ['date', 'open', 'high', 'low', 'close', 'volume']
COLUMNS_CHART_DATA = ['날짜', '시가', '고가', '저가', '종가', '거래량']

COLUMNS_TRAINING_DATA_V1 = [
    'BANDb', 'BANDWidth', 'CCI', 'CO', 'DMI', 'EOM', 'MACD_OSC', 'MI', 'Momentum', 'NCO', 'PO', 'ROC', 'RSI', 'SMI',
    'Fast Stochastic', 'TRIX', 'VO', 'VROC', 'Williams', 'ZScore'
]

COLUMNS_TRAINING_DATA_V1_RICH = [
    'open_lastclose_ratio', 'high_close_ratio', 'low_close_ratio',
    'close_lastclose_ratio', 'volume_lastvolume_ratio',
    'close_ma5_ratio', 'volume_ma5_ratio',
    'close_ma10_ratio', 'volume_ma10_ratio',
    'close_ma20_ratio', 'volume_ma20_ratio',
    'close_ma60_ratio', 'volume_ma60_ratio',
    'close_ma120_ratio', 'volume_ma120_ratio',
    'inst_lastinst_ratio', 'frgn_lastfrgn_ratio',
    'inst_ma5_ratio', 'frgn_ma5_ratio',
    'inst_ma10_ratio', 'frgn_ma10_ratio',
    'inst_ma20_ratio', 'frgn_ma20_ratio',
    'inst_ma60_ratio', 'frgn_ma60_ratio',
    'inst_ma120_ratio', 'frgn_ma120_ratio',
]

COLUMNS_TRAINING_DATA_V2 = [
    'per', 'pbr', 'roe',
    'open_lastclose_ratio', 'high_close_ratio', 'low_close_ratio',
    'close_lastclose_ratio', 'volume_lastvolume_ratio',
    'close_ma5_ratio', 'volume_ma5_ratio',
    'close_ma10_ratio', 'volume_ma10_ratio',
    'close_ma20_ratio', 'volume_ma20_ratio',
    'close_ma60_ratio', 'volume_ma60_ratio',
    'close_ma120_ratio', 'volume_ma120_ratio',
    'market_kospi_ma5_ratio', 'market_kospi_ma20_ratio', 
    'market_kospi_ma60_ratio', 'market_kospi_ma120_ratio', 
    'bond_k3y_ma5_ratio', 'bond_k3y_ma20_ratio', 
    'bond_k3y_ma60_ratio', 'bond_k3y_ma120_ratio'
]

COLUMNS_TRAINING_DATA_C = [
    'PER', 'PBR',
    'sma5', 'sma20', 'sma100', 'sma200', 'ema5', 'ema20', 'ema100', 'ema200', 'wma5', 'wma20', 'wma100', 'wma200',
    'MACD', 'MACD_Signal', 'MACD_OSC', 'RSI', 'RSI Signal', 'bol_mid', 'bol_upper', 'fast_k', 'slow_k', 'slow_d'
]

COLUMNS_TRAINING_DATA_P = [
    'BPS', 'PER', 'PBR', 'EPS', 'DIV', 'DPS',
    'sma5', 'sma20', 'sma100', 'sma200', 'ema5', 'ema20', 'ema100', 'ema200', 'wma5', 'wma20', 'wma100', 'wma200',
    'MACD', 'MACD_Signal', 'MACD_OSC', 'RSI', 'RSI Signal', 'bol_mid', 'bol_upper', 'bol_down', 'bol_down', 'bol_b', 'bol_w',
    'fast_k', 'slow_k', 'slow_d'
]


def load_data(fpath, date_from, date_to, ver='c'):
    header = 0
    data = pd.read_csv(fpath, thousands=',', header=header, encoding="utf-8",
                       converters={'날짜': lambda x: str(x)})

    # 기간 필터링
    data['날짜'] = data['날짜'].str.replace('-', '')
    data = data[(data['날짜'] >= date_from) & (data['날짜'] <= date_to)]
    # data = data.dropna()
    data = data.fillna(0)

    # 차트 데이터 분리
    chart_data = data[COLUMNS_CHART_DATA]

    # 학습 데이터 분리
    training_data = None
    if ver == 'v1':
        training_data = data[COLUMNS_TRAINING_DATA_V1].copy()
        training_data.loc[:, ['BANDb', 'BANDWidth', 'CCI', 'CO', 'DMI',
                              'EOM', 'MACD_OSC', 'MI', 'Momentum', 'NCO',
                              'PO', 'ROC', 'RSI', 'SMI', 'Fast Stochastic',
                              'TRIX', 'VO', 'VROC', 'Williams', 'ZScore']] = \
            training_data[['BANDb', 'BANDWidth', 'CCI', 'CO', 'DMI',
                           'EOM', 'MACD_OSC', 'MI', 'Momentum', 'NCO',
                           'PO', 'ROC', 'RSI', 'SMI', 'Fast Stochastic',
                           'TRIX', 'VO', 'VROC', 'Williams', 'ZScore']].apply(lambda x: np.log2(x))
    elif ver == 'v1.rich':
        training_data = data[COLUMNS_TRAINING_DATA_V1_RICH]
    elif ver == 'v2':
        data.loc[:, ['per', 'pbr', 'roe']] = \
            data[['per', 'pbr', 'roe']].apply(lambda x: x / 100)
        training_data = data[COLUMNS_TRAINING_DATA_V2]
        training_data = training_data.apply(np.tanh)
    elif ver == 'c':
        data.loc[:, ['PER', 'PBR']] = \
            data[['PER', 'PBR']].apply(lambda x: x / 100)
        training_data = data[COLUMNS_TRAINING_DATA_C]
        min_max_scaler = MinMaxScaler()
        training_data.loc[:, ['sma5', 'sma20', 'sma100', 'sma200', 'ema5', 'ema20', 'ema100', 'ema200', 'wma5', 'wma20', 'wma100', 'wma200',
                              'MACD', 'MACD_Signal', 'MACD_OSC', 'RSI', 'RSI Signal', 'bol_mid', 'bol_upper', 'bol_down', 'fast_k', 'slow_k', 'slow_d']] = min_max_scaler.fit_transform(
            training_data.loc[:, ['sma5', 'sma20', 'sma100', 'sma200', 'ema5', 'ema20', 'ema100', 'ema200', 'wma5', 'wma20', 'wma100', 'wma200',
                                  'MACD', 'MACD_Signal', 'MACD_OSC', 'RSI', 'RSI Signal', 'bol_mid', 'bol_upper', 'bol_down', 'fast_k', 'slow_k', 'slow_d']])
    elif ver == 'p':
        data.loc[:, ['DPS']] = \
            data[['DPS']].apply(lambda x: x / 100)
        data.loc[:, ['BPS', 'EPS', 'EPS']] = \
            data[['BPS', 'EPS', 'EPS']].apply(lambda x: np.log(x))
        training_data = data[COLUMNS_TRAINING_DATA_P].copy()
        robustScaler = RobustScaler()
        training_data.loc[:, ['RSI', 'RSI Signal', 'fast_k', 'slow_k', 'slow_d']] = \
            training_data[['RSI', 'RSI Signal', 'fast_k', 'slow_k', 'slow_d']].apply(lambda x: x / 100)
        training_data.loc[:,
        ['sma5', 'sma20', 'sma100', 'sma200', 'ema5', 'ema20', 'ema100', 'ema200',
         'wma5', 'wma20', 'wma100', 'wma200', 'bol_mid', 'bol_upper', 'bol_down']] = \
            training_data[
                ['sma5', 'sma20', 'sma100', 'sma200', 'ema5', 'ema20', 'ema100', 'ema200',
                 'wma5', 'wma20', 'wma100', 'wma200', 'bol_mid', 'bol_upper', 'bol_down']].apply(lambda x: np.log2(x))
        training_data.loc[:, ['MACD', 'MACD_Signal', 'MACD_OSC']] = robustScaler.fit_transform(
            training_data.loc[:, ['MACD', 'MACD_Signal', 'MACD_OSC']])

    else:
        raise Exception('Invalid version.')
    
    return chart_data, training_data
