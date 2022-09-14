import pandas as pd
import numpy as py
import time
import os
import sys

df = pd.read_csv('./test_date.csv')

print(df.info(memory_usage='deep'), '\n', df.memory_usage(deep=True), '\n', df.memory_usage(deep=False))
print(df.memory_usage().sum()/(1024**2))
print(sys.getsizeof(df.append(df))/(1024**2))


# storage thresholds (MB), 1024: 1GB
thresholds = [10, 100, 1024, 1024 * 2, 1024 * 5, 1024 * 10]
print(thresholds)

def append_data(df, threshold):

    temp_df = df
    since = time.time()
    while temp_df.memory_usage().sum()/(1024**2) < threshold:
        temp_df = temp_df.append(temp_df)
    print('it costs: ', time.time() - since, 's')
    print(temp_df.memory_usage().sum()/(1024**2), 'MB')
    # print(temp_df.reset_index(drop=True))


    temp_df.to_csv('./%s.csv' % threshold, index = False)

    return None

for threshold in thresholds:
    append_data(df, threshold)