parser.add_argument('--threshold',
                    default = 0.8,
                    type = float,
                    help='the percentage of which the missing values should be deleted')

parser.add_argument('--fill_nan_method',
                    default = 'mean',
                    type = str,
                    help='how you would like to fill the missing values')

parser.add_argument('--column_to_change',
                    default = [],
                    type = list,
                    help='choose the column name that you want to change')

parser.add_argument('--new_column_name',
                    default = [],
                    type = list,
                    help='the corresponding column name of each changed column')

parser.add_argument('--new_column_type',
                    default = [],
                    type = list,
                    help='the corresponding data type of each changed column')

parser.add_argument('--date_column_name',
                    default = 'date',
                    type = str,
                    help='the column name which represents datetime')
column_to_change = []
new_column_type = []
new_column_name = []
date_column_name = 'DATE'
threshold = 0.8
fill_nan_method = 'mean'
#扫描各特征的数据类型
def data_scan_type(df):
    return pd.DataFrame(df.dtypes)



#改变列的数据类型
def change_data_type(df, column=column_to_change, type=new_column_type):
    for i in range(len(column)):
        df[column[i]].astype(type[i])
    return df



#重新命名列名
def data_rename_column(df, column=column_to_change,new_name=new_column_name):
    for i in range(len(column)):
        df.rename(columns={column[i]: new_name[i]})
    return df



#功能是按阈值筛选掉缺失值大于多少的列，并返回剩余的数据
def detect_nan_by_column(df, threshold):
    feature = []
    row_num = df.shape[0]
    dic = df.isnull().sum().to_dict()
    for i in dic:
        if (dic[i] / row_num) > threshold:
            feature.append(i)
    new_data = df.drop(feature, axis=1)
    return new_data



#按阈值筛选掉缺失值大于多少的行，并返回剩余的数据
def detect_nan_by_row(df, threshold=threshold):
    new_data = pd.DataFrame()
    if threshold == 0:
        new_data = df.dropna()
    else:
        nan_len=0
        col_name = df.columns.tolist()
        for row_index, row in df.iterrows():
            for col in col_name:
                tmp = df.loc[row_index, col]
                if tmp != tmp:
                    nan_len += 1
            ratio = nan_len / len(col_name)
            if ratio < threshold:
                new_data = pd.concat([new_data, df.iloc[row_index,:]])
    return new_data



def fill_nan_data(df, criteria=fill_nan_method):
    col = df.columns[df.isnull().sum() > 0]
    for i in col:
        if criteria=='mean':
            val = df[i].mean()
        elif criteria=='median':
            val = df[i].median()
        elif criteria=='mode':
            val = df[i].mode()[0]
        df[i].fillna(val, inplace=True)
    return df



def check_data_by_date(df, date_column_name=date_column_name):
    df['new_date'] = ""
    df['new_index'] = 0
    multi_df = []
    for row_index, row in df.iterrows():
        df.loc[row_index, 'new_date'] = parser.parse(str(df.loc[row_index,date_column_name]))
    df.index = pd.to_datetime(df.new_date)
    df['new_index'] = df.index.isocalendar().week
    col = df['new_index'].tolist()
    df_ = df.reset_index(drop=True)
    for i in col:
        new = df_[df_['new_index']==i]
        new1 = new.reset_index(drop=True)
        new2 = new1.drop(['new_date', 'new_index'], axis=1)
        multi_df.append(new2)
    return multi_df