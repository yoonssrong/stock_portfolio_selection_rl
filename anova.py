# import scipy.stats as stats
import scipy.stats
# import scikit_posthocs as sp

import pandas as pd
import numpy as np
import urllib
import pingouin as pg

from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.sandbox.stats.multicomp import MultiComparison
from statsmodels.stats.multicomp import pairwise_tukeyhsd

import matplotlib.pyplot as plt
import seaborn as sns


df_buy = pd.read_csv('D:/project/rltrader-master/output/ANOVA/df_for_anova_buy.csv')
df_sell = pd.read_csv('D:/project/rltrader-master/output/ANOVA/df_for_anova_sell.csv')
df_return = pd.read_csv('D:/project/rltrader-master/output/ANOVA/df_for_anova_return.csv')

group1_buy = df_buy['dqn']
group2_buy = df_buy['a2c']
group3_buy = df_buy['a3c']

group1_sell = df_sell['dqn']
group2_sell = df_sell['a2c']
group3_sell = df_sell['a3c']

group1_return = df_return['dqn']
group2_return = df_return['a2c']
group3_return = df_return['a3c']


# # 정규성 검정
# print("매수 횟수 정규성 검정")
# print(scipy.stats.shapiro(group1_buy))
# print(scipy.stats.shapiro(group2_buy))
# print(scipy.stats.shapiro(group3_buy))
# print("")
# print("매도 횟수 정규성 검정")
# print(scipy.stats.shapiro(group1_sell))
# print(scipy.stats.shapiro(group2_sell))
# print(scipy.stats.shapiro(group3_sell))
# print("")
print("수익률 횟수 정규성 검정")
print(scipy.stats.shapiro(group1_return))
print(scipy.stats.shapiro(group2_return))
print(scipy.stats.shapiro(group3_return))
print("")
#
# # 등분산 검정
# print("매수 등분산 검정")
# # print(scipy.stats.bartlett(group1, group2, group3), scipy.stats.fligner(group1, group2, group3), scipy.stats.levene(group1, group2, group3), sep="\n")
# print(scipy.stats.levene(group1_buy, group2_buy, group3_buy))
# print("")
# print("매도 등분산 검정")
# print(scipy.stats.levene(group1_sell, group2_sell, group3_sell))
# print("")
print("수익률 등분산 검정")
print(scipy.stats.levene(group1_return, group2_return, group3_return))
print("")
# # bartlett(k-squared) : 비정규성에 민감하기 때문에 정규성을 따를 때만 사용해야하는 검정 방법.
# # fligner(chi-squared)
# # levene : 정규분포와 관계없이 연속적인 분포로부터 데이터를 구했을 때 사용하는 검정 방법.


# # # # t-test
# # # print(stats.ttest_ind(group1, group2, equal_var=False))
# #
# #
# ANOVA
# print(stats.f_oneway(group1, group2, group3))

# print("ANOVA(kruskal) : 매수")
# print(scipy.stats.kruskal(group1_buy, group2_buy, group3_buy))
# print("")
# print("ANOVA(kruskal) : 매도")
# print(scipy.stats.kruskal(group1_sell, group2_sell, group3_sell))
# print("")

# F_statistic, pVal = stats.f_oneway(group1, group2, group3)
#
# print('데이터의 일원분산분석 결과 : F={0:.1f}, p={1:.5f}'.format(F_statistic, pVal))
# if pVal < 0.05:
#     print('P-value 값이 충분히 작음으로 인해 그룹의 평균값이 통계적으로 유의미하게 차이납니다.')
#
# print(pVal)
#
# # 사후분석
# # 비모수검정(non-parametric test)인 크루스칼 왈리스 검정(Kruskal Wallis test)에서 유의한 차이가 나타난 경우의 사후검정으로는
# # Bonferroni correction/Bonferroni test(본페로니 교정/본페로니 검정 등)이 사용됩니다.
#
# group1_df = pd.DataFrame({'value':group1, 'group':'dqn'})
# group2_df = pd.DataFrame({'value':group2, 'group':'a2c'})
# group3_df = pd.DataFrame({'value':group3, 'group':'a3c'})
#
# df_for_post_hoc = pd.concat([group1_df, group2_df, group3_df])
# df_for_post_hoc.reset_index(drop=True, inplace=True)
#
# # df_for_post_hoc.to_csv('buy_for_hoc.csv', index=False, encoding='utf-8')
#
# # comp = MultiComparison(df_for_post_hoc.value, df_for_post_hoc.group)
# # result = comp.allpairtest(scipy.stats.ttest_ind, method='bonf')
# # print(result[0])
# # print("")
# # hsd = pairwise_tukeyhsd(df_for_post_hoc['value'], df_for_post_hoc['group'], alpha=0.05)
# # print(hsd.summary())
#
# # data = np.array([group1, group2, group3])
#
# #perform Nemenyi post-hoc test
# # print(sp.posthoc_nemenyi_friedman(data.T))
#
# # # 사후분석 : games-howell
# # print(pg.pairwise_gameshowell(data=df_for_post_hoc, dv='value', between='group').round(3))


from scipy.stats import linregress
x = [0, 2944.45]
y = [123, 3296.68]
slope, intercept, r_value, p_value, std_err = linregress(x, y)
print(slope)



# train_x = (0, 2026.16)
# train_y = (981, 2873.47)
# test_x = (0, 2944.45)
# test_y = (123, 3296.68)