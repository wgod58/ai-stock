data = [
    [
        1502928000000,
        "4261.48000000",
        "4485.39000000",
        "4200.74000000",
        "4285.08000000",
        "795.15037700",
        1503014399999,
        "3454770.05073206",
        3427,
        "616.24854100",
        "2678216.40060401",
        "0",
    ],
    [
        1503014400000,
        "4285.08000000",
        "4371.52000000",
        "3938.77000000",
        "4108.37000000",
        "1199.88826400",
        1503100799999,
        "5086958.30617151",
        5233,
        "972.86871000",
        "4129123.31651808",
        "0",
    ],
    # Add more rows as needed...
]

# Modify each row to contain only the first three items
modified_data = [[row[i] for i in range(6)] for row in data]

print(modified_data)



import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv("./data/BTCUSDT_1h_train_pattern.csv")

print(df.head())  # Print the first few rows of the DataFrame
