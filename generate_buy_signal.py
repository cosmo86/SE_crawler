import argparse
import subprocess
import sys
from datetime import datetime
import os

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


# Create the parser
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--size', type=str, help='Size parameter')
args = parser.parse_args()
if args.size:
    print(f"市值档位是: {args.size}")
else:
    print("必须填写市值信息.")
    exit()



today = datetime.now().strftime("%Y%m%d")

try:
    all_A = pd.read_csv(f"ALL_A/全部A股{today}" , encoding="GBK")

except:
    print("[全部A股] 文件不存在，请检查文件名或者日期")

try:
    yrtd_limup = pd.read_csv(f"昨日涨停{today}.csv" , encoding="GBK")
except:
    print("[昨日涨停] 文件不存在，请检查文件名或者日期")

try:
    hotones = pd.read_csv(f"hotones_{today}.csv" )
except:
    print("[东方财富人气榜前30名] 文件不存在，请检查文件名或者日期")

###################### Helper function ######################
def convert_market_cap(x):
    if '亿' in x:
        # Remove '亿' and convert to float, then multiply by a billion
        return float(x.replace('亿', '')) 
    elif x == 'nan':
        # Convert 'nan' string to actual NaN
        return np.nan
###################### Helper function ###################### 


all_A.rename(columns={'涨幅%': 'fluc_today'}, inplace=True)
all_A['fluc_today']= pd.to_numeric(all_A['fluc_today'], errors='coerce')
top_100 = all_A.sort_values(by='fluc_today', ascending=False).head(100)

hotones.rename(columns={'SRCSECURITYCODE': '代码'}, inplace=True)
hotones["代码"] = hotones["代码"].apply(lambda x: x[2:])
hotones = hotones.query("RANK <= 30")

combined_before_filter = pd.concat([ hotones[["代码"]] , top_100[["代码"]], yrtd_limup[["代码"]]  ])


combined_before_filter =combined_before_filter.merge(all_A, how="left", left_on="代码", right_on="代码")
combined_filtered = combined_before_filter[~combined_before_filter['名称'].str.contains( 'ST|\*ST|N' ,na=False)]
combined_filtered_84 = combined_filtered[~combined_filtered['代码'].str.startswith('8') |  combined_filtered['代码'].str.startswith('4')]

combined_filtered_84.rename(columns={'10日涨幅%': 'fluc_10day', '20日涨幅%': 'fluc_20day'}, inplace=True)
combined_filtered_84["fluc_10day"] = combined_filtered_84["fluc_10day"].apply(lambda x: float(x))
combined_filtered_84["fluc_20day"] = combined_filtered_84["fluc_20day"].apply(lambda x: float(x))

combined_filtered_84 = combined_filtered_84.drop_duplicates()


####### Results #######
res_market_cap_35 = combined_filtered_84.query('fluc_10day<70 and fluc_20day<70 and 流通市值Z<35')
res_market_cap_35_100 = combined_filtered_84.query(' 流通市值Z>35 and 流通市值Z<100')
res_market_cap_100 = combined_filtered_84.query('  流通市值Z>100')

res_market_cap_35 = res_market_cap_35[['代码','名称','fluc_today','流通市值Z','fluc_10day','fluc_20day','细分行业']]
res_market_cap_35_100 = res_market_cap_35_100[['代码','名称','fluc_today','流通市值Z','fluc_10day','fluc_20day','细分行业']]
res_market_cap_100 = res_market_cap_100[['代码','名称','fluc_today','流通市值Z','fluc_10day','fluc_20day','细分行业']]


import os

# Folder name
folder_name = 'Out'

# Check if the folder exists
if not os.path.exists(folder_name):
    # Create the folder
    os.makedirs(folder_name)

res_market_cap_35.to_csv(f"{folder_name}/res_market_cap_35_{today}.csv")
res_market_cap_35_100.to_csv(f"{folder_name}/res_market_cap_35_100_{today}.csv")
res_market_cap_100.to_csv(f"{folder_name}/res_market_cap_100_{today}.csv")


######### Generate buy signal ###############
folder_name = '白名单'
# Check if the folder exists
if not os.path.exists(folder_name):
    # Create the folder
    os.makedirs(folder_name)

buy_templete = pd.read_csv("templetes/buy_templete.csv",encoding="GBK")

if args.size == "small":
    temp_templete = buy_templete.head(len(res_market_cap_35))
    temp_templete['SecurityId'] = res_market_cap_35['代码'].apply(lambda x: 's-'+x).values
    temp_templete['SecurityName'] = res_market_cap_35['名称'].values
    new_order = ['SecurityId', 'SecurityName','Accounts', 'BuyPriceType', 'BuyPrice', 'BuyPriceFactor', 'BuyVolume',
       'SellPriceType', 'SellPrice', 'SellPriceFactor', 'SellVolume', 'Tag_A',
       'Tag_B']
    temp_templete = temp_templete[new_order]
    for i in range(3):
        temp_templete.to_csv(f"{folder_name}/BuyGZ{i+1}.csv")
elif args.size == "med":
    temp_templete = buy_templete.head(len(res_market_cap_35_100))
    temp_templete['SecurityId'] = res_market_cap_35_100['代码'].apply(lambda x: 's-'+x).values
    temp_templete['SecurityName'] = res_market_cap_35_100['名称'].values
    new_order = ['SecurityId', 'SecurityName','Accounts', 'BuyPriceType', 'BuyPrice', 'BuyPriceFactor', 'BuyVolume',
       'SellPriceType', 'SellPrice', 'SellPriceFactor', 'SellVolume', 'Tag_A',
       'Tag_B']
    temp_templete = temp_templete[new_order]
    for i in range(3):
        temp_templete.to_csv(f"{folder_name}/BuyGZ{i+1}.csv")
    
else:
    temp_templete = buy_templete.head(len(res_market_cap_100))
    temp_templete['SecurityId'] = res_market_cap_100['代码'].apply(lambda x: 's-'+x).values
    temp_templete['SecurityName'] = res_market_cap_100['名称'].values
    new_order = ['SecurityId', 'SecurityName','Accounts', 'BuyPriceType', 'BuyPrice', 'BuyPriceFactor', 'BuyVolume',
       'SellPriceType', 'SellPrice', 'SellPriceFactor', 'SellVolume', 'Tag_A',
       'Tag_B']
    temp_templete = temp_templete[new_order]
    for i in range(3):
        temp_templete.to_csv(f"{folder_name}/BuyGZ{i+1}.csv")