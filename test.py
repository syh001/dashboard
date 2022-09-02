def get_kpi(df, column, axis=0):
    df = df.loc[:, [column]]

    print(df)
    print(df.mean(axis))
    try:
        df_mean = df.mean(axis)[0]
        df_std = df.std(axis)[0]
        df_median = df.median(axis)[0]

    except:
        df_mean = 'N/A'
        df_std = 'N/A'
        df_median = 'N/A'

    return {
        "df_mean": df_mean,
        "df_std": df_std,
        "df_median": df_median,
    }
import pandas as pd
DF = pd.read_csv('./test.csv')
print(get_kpi(DF, 'TOOL'))