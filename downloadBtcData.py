import requests
import pandas as pd
import datetime
import os

# 创建数据目录
data_dir = "./data/"
os.makedirs(data_dir, exist_ok=True)

# 初始化两个空的DataFrame来存储所有数据
all_data_train = pd.DataFrame()
all_data_test = pd.DataFrame()

# 定义时间间隔和日期范围
symbol = "BTCUSDT"
# interval 15m 1h 4h 1d
interval = "4h"

# 遍历每一年，从2014年到2024年
for year in range(2017, 2025):
    for month in range(1, 13):  # Python的range函数默认从0开始，所以这里是1到12
        start_date = datetime.datetime(year, month, 1)
        # end_date
        if month == 12:
            end_date = datetime.datetime(year + 1, 1, 1)
        else:
            end_date = datetime.datetime(year, month + 1, 1)

        # end_month = month + 1 if month < 12 else 1  # 修正end_month的计算
        # end_date = datetime.datetime(year, end_month, 1) - datetime.timedelta(
        #     days=1
        # )  # 获取该月的最后一天

        start_timestamp = int(start_date.timestamp() * 1000)
        end_timestamp = int(end_date.timestamp() * 1000)

        print(start_date)
        print(end_date)

        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&startTime={start_timestamp}&endTime={end_timestamp}"

        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to retrieve data for {symbol} at {start_date} to {end_date}")
            continue

        # Gmt time,Open,High,Low,Close,Volume

        data = response.json()

        data = [[row[i] for i in range(6)] for row in data]

        # print(data)

        df = pd.DataFrame(
            data,
            columns=[
                "Gmt time",
                "Open",
                "High",
                "Low",
                "Close",
                "Volume",
            ],
        )
        df["Gmt time"] = pd.to_datetime(df["Gmt time"], unit="ms")

        # 判断数据归属年份，追加到相应的DataFrame中
        if year >= 2017 and year <= 2020:
            all_data_train = pd.concat([all_data_train, df], ignore_index=True)
        elif year >= 2021 and year <= 2024:
            all_data_test = pd.concat([all_data_test, df], ignore_index=True)

# 按照年份保存到CSV文件中
# 保存2014年至2018年的数据
filename_train = f"{symbol}_{interval}_train.csv"
all_data_train.to_csv(os.path.join(data_dir, filename_train), index=False)
print(f"Training data for years 2017-2018 saved to {filename_train}")

# 保存2019年至2024年的数据
filename_test = f"{symbol}_{interval}_test.csv"
all_data_test.to_csv(os.path.join(data_dir, filename_test), index=False)
print(f"Testing data for years 2019-2024 saved to {filename_test}")
