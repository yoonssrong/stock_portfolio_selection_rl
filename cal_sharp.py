import pandas as pd
import os


PATH = "D:/project/rltrader-master/output/p_a3c_test_best/"

# jackup_list = ['003670', '068270', '081660', '009420', '011790', '028670', '071050', '006400', '004800', '003850', '042660', '001680', '010620', '009150', '105560', '018880', '035420', '010950', '047040', '004000', '017800', '004990', '028260', '005300', '185750', '051910', '006800', '000990', '005180', '097950', '192400', '029780', '009540', '032640', '006260', '096770', '138930', '003230', '069260', '192080', '024110', '006360', '055550', '001740', '051600']
# jackup_list = list(map(lambda x: 'epoch_summary_'+x, jackup_list))

jackup_list = os.listdir(PATH)

output = pd.DataFrame({'pvs':pd.Series(0, index=list(range(123)))})

for folder in jackup_list:
    df = pd.read_csv(os.path.join(PATH, folder) + '/epoch_summary_1.csv')
    pvs = df['pvs']
    output['pvs'] += pvs

output['pvs'] = output['pvs'] / len(jackup_list)

output.to_csv('./output/cal_sharp_a3c.csv')
