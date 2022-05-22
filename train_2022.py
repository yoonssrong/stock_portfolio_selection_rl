import os
import sys
import logging
import pandas as pd
import openpyxl
import gc

import settings
import utils
import data_manager


# 학습 기간
period = [
    ('20110915', '20111208'),
    ('20111209', '20120308'),
    ('20120309', '20120614'),
    ('20120615', '20120913'),
    ('20120914', '20121213'),
    ('20121214', '20130314'),
    ('20130315', '20130613'),
    ('20130614', '20130912'),
    ('20130913', '20131212'),
    ('20131213', '20140313'),
    ('20140314', '20140612'),
    ('20140613', '20140911'),
    ('20140912', '20141211'),
    ('20141212', '20150312'),
    ('20150313', '20150611'),
    ('20150612', '20150910'),
    ('20150911', '20151210'),
    ('20151211', '20160310'),
    ('20160311', '20160609'),
    ('20160610', '20160908'),
    ('20160909', '20161208'),
    ('20161209', '20170309'),
    ('20170310', '20170608'),
    ('20170609', '20170914'),
    ('20170915', '20171214'),
    ('20171215', '20180308'),
    ('20180309', '20180614'),
    ('20180615', '20180913'),
    ('20180914', '20181213'),
    ('20181214', '20190314'),
    ('20190315', '20190613'),
    ('20190614', '20190911'),
    ('20190916', '20191212'),
    ('20191213', '20200312'),
    ('20200313', '20200611'),
    ('20200612', '20200910'),
    ('20200911', '20201210')
]

# kospi200 종목 리스트 경로
PATH = './data/kospi200/'

# set options
ver = 'v1'
rl_method = 'a2c'  # choices=['dqn', 'pg', 'ac', 'a2c', 'a3c']
net = 'lstm'  # choices=['dnn', 'lstm', 'cnn']
num_steps = 5
lr = 0.0001
discount_factor = 0
start_epsilon = 0.5
balance = 10000000
num_epoches = 10
delayed_reward_threshold = 0.05
value_network_name = None
policy_network_name = None
reuse_models = False
learning = True

setList = os.listdir(PATH)

os.environ['KERAS_BACKEND'] = 'tensorflow'

for i, set in enumerate(setList):

    gc.collect()

    start_date, end_date = period[i]

    file = openpyxl.load_workbook(os.path.join(PATH, set))
    file = file['Sheet1']
    data = file.values
    columns = next(data)[0:]
    df = pd.DataFrame(data, columns=columns)

    tickers = df['종목코드']

    # 학습 재시작시 중복체크
    utils.mkDIRc.mkDIRd(f'./output/3m/{set}_{rl_method}/')
    ex_list = os.listdir(f'./output/3m/{set}_{rl_method}/')
    tickers = [x for x in tickers if x not in ex_list]

    for targetcode in tickers:

        gc.collect()

        list_targetcode = [targetcode]

        # 출력 경로 설정
        output_path = os.path.join(settings.BASE_DIR,
                                   f'output/3m/{set}/{targetcode}')
        utils.mkDIRc.mkDIRd(output_path)

        # 종목별 로그 개별 저장을 위해 루트 로그 초기화
        log = logging.getLogger()
        for hdlr in log.handlers[:]:
            log.removeHandler(hdlr)

        # 로그 기록 설정
        file_handler = logging.FileHandler(filename=os.path.join(
            output_path, f"{targetcode}.log"), encoding='utf-8')
        stream_handler = logging.StreamHandler(sys.stdout)
        file_handler.setLevel(logging.DEBUG)
        stream_handler.setLevel(logging.INFO)
        logging.basicConfig(format="%(message)s", handlers=[file_handler, stream_handler], level=logging.DEBUG)

        # 로그, Keras Backend 설정을 먼저하고 RLTrader 모듈들을 이후에 임포트해야 함
        from learners import DQNLearner, PolicyGradientLearner, \
            ActorCriticLearner, A2CLearner, A3CLearner

        # 모델 경로 준비
        value_network_path = ''
        policy_network_path = ''
        if value_network_name is not None:
            value_network_path = os.path.join(settings.BASE_DIR,
                                              f'models/{value_network_name}.h5')
        else:
            value_network_path = os.path.join(
                output_path, f'{rl_method}_{net}_value_{start_date}_{end_date}_{targetcode}.h5')
        if policy_network_name is not None:
            policy_network_path = os.path.join(settings.BASE_DIR,
                                               f'models/{policy_network_name}.h5')
        else:
            policy_network_path = os.path.join(
                output_path, f'{rl_method}_{net}_policy_{start_date}_{end_date}_{targetcode}.h5')

        common_params = {}
        list_stock_code = []
        list_chart_data = []
        list_training_data = []
        list_min_trading_unit = []
        list_max_trading_unit = []

        for stock_code in list_targetcode:
            # 차트 데이터, 학습 데이터 준비
            chart_data, training_data = data_manager.load_data(
                os.path.join(settings.BASE_DIR,
                             f'data/{ver}/{stock_code}.csv'),
                start_date, end_date, ver=ver)

            # 최소/최대 투자 단위 설정
            min_trading_unit = max(int(100000 / chart_data.iloc[-1]['종가']), 1)
            max_trading_unit = max(int(1000000 / chart_data.iloc[-1]['종가']), 1)

            # 공통 파라미터 설정
            common_params = {'rl_method': rl_method,
                             'delayed_reward_threshold': delayed_reward_threshold,
                             'net': net, 'num_steps': num_steps, 'lr': lr,
                             'output_path': output_path, 'reuse_models': reuse_models}

            # 강화학습 시작
            learner = None
            if rl_method != 'a3c':
                common_params.update({'stock_code': stock_code,
                                      'chart_data': chart_data,
                                      'training_data': training_data,
                                      'min_trading_unit': min_trading_unit,
                                      'max_trading_unit': max_trading_unit})
                if rl_method == 'dqn':
                    learner = DQNLearner(**{**common_params,
                                            'value_network_path': value_network_path})
                elif rl_method == 'pg':
                    learner = PolicyGradientLearner(**{**common_params,
                                                       'policy_network_path': policy_network_path})
                elif rl_method == 'ac':
                    learner = ActorCriticLearner(**{**common_params,
                                                    'value_network_path': value_network_path,
                                                    'policy_network_path': policy_network_path})
                elif rl_method == 'a2c':
                    learner = A2CLearner(**{**common_params,
                                            'value_network_path': value_network_path,
                                            'policy_network_path': policy_network_path})
                if learner is not None:
                    learner.run(balance=balance,
                                num_epoches=num_epoches,
                                discount_factor=discount_factor,
                                start_epsilon=start_epsilon,
                                learning=learning)
                    learner.save_models()
            else:
                list_stock_code.append(stock_code)
                list_chart_data.append(chart_data)
                list_training_data.append(training_data)
                list_min_trading_unit.append(min_trading_unit)
                list_max_trading_unit.append(max_trading_unit)

        if rl_method == 'a3c':
            learner = A3CLearner(**{
                **common_params,
                'list_stock_code': list_stock_code,
                'list_chart_data': list_chart_data,
                'list_training_data': list_training_data,
                'list_min_trading_unit': list_min_trading_unit,
                'list_max_trading_unit': list_max_trading_unit,
                'value_network_path': value_network_path,
                'policy_network_path': policy_network_path})

            learner.run(balance=balance, num_epoches=num_epoches,
                        discount_factor=discount_factor,
                        start_epsilon=start_epsilon,
                        learning=learning)
            learner.save_models()

        # out of memory
        import tensorflow as tf
        with tf.Graph().as_default():
            gpu_options = tf.compat.v1.GPUOptions(allow_growth=True)