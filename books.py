from itertools import count

import pandas as pd
import statistics
import numpy as np

pd.set_option('display.max_columns', 16)

# df = pd.read_csv('bank_transactions_data_2.csv')
# df.sort_values(["CustomerAge"], axis=0, ascending=False, inplace=True)

# print("\nAfter sorting:")
df = pd.read_csv('roulette_1000_rounds.csv')

arr = np.array(df["Winning Number"])
x = count(arr == 0)
for x in range(1000):
    if x in x == [0]:
        print(x)

#Trying to find the number of zeros per 1000







# cols = [10]
# df = df[df.columns[cols]]

# arr = np.array(df)

# print(arr[2])