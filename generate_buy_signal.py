import argparse
import subprocess
import sys
from datetime import datetime
import os
import warnings

try:
    import pandas
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", "pandas"])
    import pandas as pd

try:
    import numpy
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", "numpy"])
    import numpy as np


import pandas as pd
import numpy as np
# Suppresswarning
from pandas.core.common import SettingWithCopyWarning

from SE_config.SE_config import MID_CONFIG, LARGE_CONFIG, ROW_TEMPLETE

# Ignore SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

# Create the parser
parser = argparse.ArgumentParser(description='Process some string.')
parser.add_argument('--low_lim', type=str, help='Size parameter')
parser.add_argument('--high_lim', type=str, help='Size parameter')
args = parser.parse_args()
if (args.low_lim and args.high_lim):
    print(f"市值档位是: 小 {args.low_lim} 亿元 - 大 {args.high_lim} 亿元")
else:
    print("必须填写市值信息.")
    exit()



today = datetime.now().strftime("%Y%m%d")

try:
    all_A = pd.read_csv(f"每日源文件/全部Ａ股{today}.csv" , encoding="GBK")

except:
    print("[全部A股] 文件不存在，请检查文件名或者日期")

try:
    yrtd_limup = pd.read_csv(f"每日源文件/昨日涨停{today}.csv" , encoding="GBK")
except:
    print("[昨日涨停] 文件不存在，请检查文件名或者日期")

try:
    hotones = pd.read_csv(f"每日源文件/人气榜{today}.csv" , encoding="GBK")
    user_provided_hotones = True
except FileNotFoundError:
    print("[东方财富人气榜前30名] 文件不存在，请检查文件名或者日期")
except Exception as e:
    print(f"错误发生！！！ 请联系管理员: {e}")

###################### Helper function ######################
def convert_market_cap(x):
    if isinstance(x, str):
        if '亿' in x:
            # Remove '亿' and convert to float, then multiply by a billion
            return float(x.replace('亿', '')) 
    else:
        if x == 'nan' or x==np.nan:
            # Convert 'nan' string to actual NaN
            return np.nan
###################### Helper function ###################### 


all_A.rename(columns={'涨幅%': 'fluc_today'}, inplace=True)
all_A['fluc_today']= pd.to_numeric(all_A['fluc_today'], errors='coerce')
top_100 = all_A.sort_values(by='fluc_today', ascending=False).head(100)

if user_provided_hotones:
    print("用户正在使用用户自己提供的 人气榜排名, 不再对排名做更多处理")
else:
    hotones.rename(columns={'SRCSECURITYCODE': '代码'}, inplace=True)
    hotones["代码"] = hotones["代码"].apply(lambda x: x[2:])
    #hotones = hotones.query("RANK <= 30")

combined_before_filter = pd.concat([ hotones[["代码"]] , top_100[["代码"]], yrtd_limup[["代码"]]  ])


combined_before_filter =combined_before_filter.merge(all_A, how="left", left_on="代码", right_on="代码")
combined_filtered = combined_before_filter[~combined_before_filter['名称'].str.contains( 'ST|\*ST|N' ,na=False)]
combined_filtered_84 = combined_filtered[~combined_filtered['代码'].str.startswith('8') |  combined_filtered['代码'].str.startswith('4')]


combined_filtered_84["流通市值Z"] = combined_filtered_84["流通市值Z"].apply(convert_market_cap)
combined_filtered_84.rename(columns={'10日涨幅%': 'fluc_10day', '20日涨幅%': 'fluc_20day'}, inplace=True)
combined_filtered_84["fluc_10day"] = combined_filtered_84["fluc_10day"].apply(lambda x: float(x))
combined_filtered_84["fluc_20day"] = combined_filtered_84["fluc_20day"].apply(lambda x: float(x))

combined_filtered_84 = combined_filtered_84.drop_duplicates()


####### Results #######

res_market_cap_filtered = combined_filtered_84.query(f"流通市值Z>{args.low_lim} and 流通市值Z<{args.high_lim}")
#res_market_cap_35 = combined_filtered_84.query('fluc_10day<70 and fluc_20day<70 and 流通市值Z<35')
#res_market_cap_35_100 = combined_filtered_84.query(' 流通市值Z>35 and 流通市值Z<100')
#res_market_cap_100 = combined_filtered_84.query('  流通市值Z>100')

#res_market_cap_35 = res_market_cap_35[['代码','名称','fluc_today','流通市值Z','fluc_10day','fluc_20day','细分行业']]
#res_market_cap_35_100 = res_market_cap_35_100[['代码','名称','fluc_today','流通市值Z','fluc_10day','fluc_20day','细分行业']]
#res_market_cap_100 = res_market_cap_100[['代码','名称','fluc_today','流通市值Z','fluc_10day','fluc_20day','细分行业']]
res_market_cap_filtered = res_market_cap_filtered[['代码','名称','fluc_today','流通市值Z','fluc_10day','fluc_20day','细分行业']]

import os

# Folder name
folder_name = 'Out'
SE_path = os.path.join(folder_name,"SE_path")
# Check if the folder exists
if not os.path.exists(SE_path):
    # Create the folder
    os.makedirs(SE_path)

#res_market_cap_35.to_csv(f"{folder_name}/res_market_cap_35_{today}.csv")
#res_market_cap_35_100.to_csv(f"{folder_name}/res_market_cap_35_100_{today}.csv")
#res_market_cap_100.to_csv(f"{folder_name}/res_market_cap_100_{today}.csv")
res_market_cap_filtered['代码'] = res_market_cap_filtered['代码'].astype(str)
res_market_cap_filtered.to_csv(f"{folder_name}/res_market_cap_{args.low_lim}_{args.high_lim}_{today}.csv")

########################################## SE Engine ##########################################
SE_engine_df = res_market_cap_filtered.copy()
res_list = []
for i in range(len(SE_engine_df)):

    temp_config = MID_CONFIG if SE_engine_df.iloc[i]['流通市值Z']<100 else LARGE_CONFIG
    #print(temp_config)
    for j in range(3):
        
        temp_res_row = ROW_TEMPLETE
        temp_res_row['SecurityID'] = SE_engine_df.iloc[i]['代码']
        temp_res_row['ExchangeID'] = '1' if temp_res_row['SecurityID'].startswith('6') else '2'
        
        temp_res_row['BuyTriggerVolume'] = temp_config[f"TRIGGER_{j+1}"]
        temp_res_row['CancelVolume'] = temp_config[f"CANCEL_{j+1}"]
        
        #temp_res_row['Position'] = temp_config[]
        #temp_res_row['MaxTriggerTimes'] = temp_config[f"TRIGGER_{j}"]
        #temp_res_row['LowerTimeLimit'] = temp_config[f"TRIGGER_{j}"]
        
        temp_res_row['ScoutBuyTriggerCashLim'] = temp_config[f"SCOUT_TRIGGER_{j+1}"]
        
        #temp_res_row['ScoutMonitorDuration'] = temp_config[f"TRIGGER_{j}"]
        #temp_res_row['Cond2Percent'] = temp_config[f"TRIGGER_{j}"]
        #temp_res_row['Cond2HighTime'] = temp_config[f"TRIGGER_{j}"]
        #temp_res_row['Cond2TrackDuration'] = temp_config[f"TRIGGER_{j}"]
        temp_res_row['CancelTriggerVolumeLarge'] = temp_config[f"CANCEL_LARGE_{j+1}"]
        #temp_res_row['Cond4LowTime'] = temp_config[f"TRIGGER_{j}"]
        #temp_res_row['Cond4HighTime'] = temp_config[f"TRIGGER_{j}"]
        res_list.append(temp_res_row.copy())

res_SE_df = pd.DataFrame(res_list)
res_SE_df.to_csv(f"{SE_path}/SE_daily_pool_{today}",index=False)
print("SE pool generated!")

########################################## SE Engine End ##########################################

################### Divide SH and SZ ###################
#res_market_cap_35_sh = res_market_cap_35[res_market_cap_35['代码'].str.startswith('6') ]
#res_market_cap_35_sz = res_market_cap_35[res_market_cap_35['代码'].str.startswith('3') | res_market_cap_35['代码'].str.startswith('0') ]

#res_market_cap_35_100_sh = res_market_cap_35_100[res_market_cap_35_100['代码'].str.startswith('6') ]
#res_market_cap_35_100_sz = res_market_cap_35_100[res_market_cap_35_100['代码'].str.startswith('3') | res_market_cap_35_100['代码'].str.startswith('0') ]

#res_market_cap_100_sh = res_market_cap_100[res_market_cap_100['代码'].str.startswith('6') ]
#res_market_cap_100_sz = res_market_cap_100[res_market_cap_100['代码'].str.startswith('3') | res_market_cap_100['代码'].str.startswith('0') ]
res_market_cap_filtered_sh = res_market_cap_filtered[res_market_cap_filtered['代码'].str.startswith('6') ]
res_market_cap_filtered_sz = res_market_cap_filtered[res_market_cap_filtered['代码'].str.startswith('3') | res_market_cap_filtered['代码'].str.startswith('0')
                                                     
                                                      ]
######### Generate buy signal ###############
# Parent directory name
parent_dir = '白名单'
# Child directory names
child_dir_sh = '上海'
child_dir_sz = '深圳'
# Construct paths for the child directories
path_sh = os.path.join(parent_dir, f"{args.low_lim}_{args.high_lim}", child_dir_sh)
path_sz = os.path.join(parent_dir, f"{args.low_lim}_{args.high_lim}",child_dir_sz)

# Check if the parent folder doesn't exist
if not os.path.exists(path_sh):
    # Create the directories
    os.makedirs(path_sh, exist_ok=True)
    os.makedirs(path_sz, exist_ok=True)

## Populate temp_templete with dummy variables
buy_templete = pd.read_csv("templetes/buy_templete.csv",encoding="GBK")
buy_templete = buy_templete[['Accounts', 'BuyPriceType', 'BuyPrice',
       'BuyPriceFactor', 'BuyVolume', 'SellPriceType', 'SellPrice',
       'SellPriceFactor', 'SellVolume', 'Tag_A', 'Tag_B']]
for i in range(5): # 47(lenth of templete) * 2**5, which should hold 1500 stocks
    buy_templete = pd.concat([buy_templete,buy_templete])




# SH
temp_templete = buy_templete.head(len(res_market_cap_filtered_sh))
temp_templete['SecurityId'] = res_market_cap_filtered_sh['代码'].apply(lambda x: 's-'+x).values
temp_templete['SecurityName'] = res_market_cap_filtered_sh['名称'].values
new_order = ['SecurityId', 'SecurityName','Accounts', 'BuyPriceType', 'BuyPrice', 'BuyPriceFactor', 'BuyVolume',
    'SellPriceType', 'SellPrice', 'SellPriceFactor', 'SellVolume', 'Tag_A',
    'Tag_B']
temp_templete = temp_templete[new_order]
for i in range(3):
    temp_templete.to_csv(f"{path_sh}/BuyGZ{i+1}.csv", index=False, encoding="GBK")

#SZ
temp_templete = buy_templete.head(len(res_market_cap_filtered_sz))
temp_templete['SecurityId'] = res_market_cap_filtered_sz['代码'].apply(lambda x: 's-'+x).values
temp_templete['SecurityName'] = res_market_cap_filtered_sz['名称'].values
new_order = ['SecurityId', 'SecurityName','Accounts', 'BuyPriceType', 'BuyPrice', 'BuyPriceFactor', 'BuyVolume',
    'SellPriceType', 'SellPrice', 'SellPriceFactor', 'SellVolume', 'Tag_A',
    'Tag_B']
temp_templete = temp_templete[new_order]
for i in range(3):
    temp_templete.to_csv(f"{path_sz}/BuyGZ{i+1}.csv", index=False, encoding="GBK")


print("处理完成！")