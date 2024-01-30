import subprocess
import sys

try:
    import selenium
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", "selenium"])

try:
    import bs4
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", "beautifulsoup4"])

try:
    import pandas
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", "pandas"])
    import pandas as pd

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime

# Get today's date in the same format as your JSON data
today = datetime.now().strftime("%Y%m%d")

results = []

# Set up the WebDriver
driver_path = "other/chromedriver.exe"  # Replace with your path to chromedriver
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

url = "https://guba.eastmoney.com/rank/"
driver.get(url)
driver.implicitly_wait(10)  # Wait for the page to fully load

for i in range(2):
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")
    a_tags = soup.find_all('a', attrs={'data-strdata': True})
    data_strdata_values = [tag['data-strdata'] for tag in a_tags]

    for data_str in data_strdata_values:
        data_list = json.loads(data_str)
        for item in data_list:
            if 'CALCTIME' in item and today in item['CALCTIME']:
                rank = item.get('RANK')
                srcsecuritycode = item.get('SRCSECURITYCODE', 'N/A')
                results.append({'CALCTIME': item['CALCTIME'], 'RANK': rank, 'SRCSECURITYCODE': srcsecuritycode})

    if i < 1:  # Only click 'Next Page' if not on the last iteration
        try:
            next_button = driver.find_element(By.XPATH, "//a[contains(text(),'下一页')]")
            next_button.click()
            time.sleep(5)  # Wait for the next page to load
        except NoSuchElementException:
            print("No more pages to navigate.")
            break

res_df = pd.DataFrame(results)

import os

# Folder name
folder_name = 'hotones'

# Check if the folder exists
if not os.path.exists(folder_name):
    # Create the folder
    os.makedirs(folder_name)

csv_file_path = f"{folder_name}/hotones_{today}.csv"
res_df.to_csv(csv_file_path, index=False)
