def columns2dictionary(df):
    """
    该字典key为前端准备显示的所有多选字段名, value为数据库对应的字段名
    从DataFrame里读取生成, key即是value, 所见即所得

    """
    dictionary = {col: col for col in df.columns}

    # print(dictionary)

    return dictionary
import pandas as pd
aa = 1
mselect_dict = {}

df = pd.read_excel('C:/Users/sas053/Desktop/feature_importance.xlsx')  # 将sql语句结果读取至Pandas Dataframe


dct = columns2dictionary(df)
# D_MULTI_SELECT
for key, value in dct.items():
    mselect_dict[key] = {}
    mselect_dict[key]['select'] = value
print(mselect_dict)