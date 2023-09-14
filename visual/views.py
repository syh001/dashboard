import re
import datetime
from ydata_profiling import ProfileReport
import csaps
from django.http import HttpResponse
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import os
from django.shortcuts import render, redirect
import json
from .charts import *
try:
    import six
except ImportError:
    from django.utils import six
import time
import json
from random import randrange
from django.http import HttpResponse
from django.template.defaulttags import register
# from rest_framework.views import APIView
root_path = './'
source_path = 'C:/Users/1000300246/Desktop/test_folder/'
target_path = 'C:/Users/sas053/Desktop/dataset'


global DF
DF = pd.read_csv('C:/Users/1000300246/Desktop/test_folder/HDD_Magnetic.csv')
# DF.sort_values(by=['new_Date'], ascending=True, inplace=True)
@register.filter
def get_range(value):
    return range(len(value))

def test_read_speed():
    since = time.time()
    print('it costs: ', time.time() - since, 's to load the file')
    print(DF.memory_usage().sum() / (1024 ** 2), 'MB')
    since = time.time()
    df_col = DF.iloc[:, 7]
    print('it costs: ', time.time() - since, 's to load the column')


def read_data(source_path, target_path, file_name, file_name_save):
    source_file = source_path + file_name
    target_file = target_path + file_name_save
    if source_file.endswith('.sas7bdat'):
        df = pd.read_sas(source_file)
    # elif source_file.endswith('.jmp'):
    #     jmp = Dispatch("JMP.Application")
    #     doc = jmp.OpenDocument(source_file)
    #     # temporarily add csv file
    #     doc.SaveAs(target_file)
    #     df = pd.read_csv(target_file)
    #     # Delete the extraly generated csv file 
    #     # to ensure that the data warehouse has not changed
    #     os.remove(target_path + file_name_save)
    else:
        df = pd.read_csv(source_file)
    return df


def get_kpi(df, column, axis=0):
    df = df.loc[:, [column]]

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


# 该字典key为前端准备显示的所有多选字段名, value为数据库对应的字段名
D_MULTI_SELECT = {
    'YC': ['Yield', 'EC'],
    'Magnetic': ['ACC', 'MCW', 'Roller SER'],
    'Reader HI': ['1k-BEM(Rd)NT', '1k-BEM(Rd)HT', 'Bi-state XTI Profile (writer induced HI)', '172c'],
    'PE': ['PE NT (Degauss on)', 'PE HT (Degauss off/on)'],
    'XTI': ['XTI NT', 'XTI HT'],
    'XTI Degradation': ['Delta XTI', 'Delta OWC'],
    'Writer instability': ['1K-BEM (WrRd) HT', 'RV_Range', 'B_Allband'],
    'Writer degradation': ['Delta MCW', 'Delta SER', 'Delta OW'],
    'Write-short': ['UEC (S5W, Func, SRST, Fin & Featuring)'],
}
ALERT_PARAMETER = {
    'Write-Short': ['F61F_DPPM', 'F623_DPPM(PCM)'],
    'Reader HI': ['Bi_state', 'hi_idd_sig_P99_rd_HT_2R', 'i_rd_172c_cnt_p99'],
    'PE': ['R_delta_PE_p99', 'R_delSER_Max_P99_HT_Track0', 'R_delSER_Max_P99_NT_Track0'],
    'XTI': ['R_delSER_Max_P99_HT_F_FTI', 'R_delSER_Max_P99_HT_N_FTI', 'R_delSER_Max_P99_HT_NTI', 'R_delSER_Max_P99_HT_Track23', 'R_delSER_Max_P99_HT_Trackminus1', 'R_delSER_Max_P99_HT_Trackplus1', 'nmax50byband_6600_min_P1'],
    'XTI Degradation': ['dNTI_FR', 'OWC_delta_min_P1'],
    'Writer Instability': ['hi_idd_sig_P99_wr_HT_trim', 'hi_idd_sig_P99_wr_HT_nontrim', 'RV_Rng_P99', 'B_byallband_P1'],
    'Writer Degradation': ['Final_SER_delta_P99', 'MCW_MD_delta_P99', 'OWP_delta_min_P1']
}
def index(request):
    mselect_dict = {}
    dic = {}
    form_dict = dict(six.iterlists(request.GET))
    # print('arrive index!', form_dict)
    df = DF
    dct = columns2dictionary(df)
    for key, value in dct.items():
        mselect_dict[key] = {}
        mselect_dict[key]['select'] = value
        mselect_dict[key]['options'] = get_distinct_list(df, value)  # 以后可以后端通过列表为每个多选控件传递备选项
        dic[key] = list(set(get_distinct_list(df, value).tolist()))
    # print('mselect_dict', mselect_dict)
    context = {
        'mselect_dict': mselect_dict,
        'D_MULTI_SELECT': D_MULTI_SELECT,
        'ALERT_PARAMETER': ALERT_PARAMETER,
        'Product': dic['PRODUCT'],
        'Model': dic['HDD_Model'],
        'option_list': list(ALERT_PARAMETER.keys())
    }
    # 下面一定要返回子模板，否则的话是block与endblock失效的原因！！！
    return render(request, 'visual/plot.html', context)

def find_category(string):
  for key, value in ALERT_PARAMETER.items():
    for v in value:
      if v in string:
        return key

def alert(request):
    dic1 = {'a':[{'wafer':110,'feature':'dvnj'},{'wafer':110,'feature':'dvnj'},{'wafer':110,'feature':'dvnj'}],
            'b':[{'wafer':111,'feature':'dfve'},{'wafer':110,'feature':'dvnj'}]}
    form_dict = dict(six.iterlists(request.GET))
    new_dict = {key: ALERT_PARAMETER[key] for key in ALERT_PARAMETER}
    for i in new_dict:
        new_dict[i] = []
    df = pd.read_csv(source_path + 'wafer_table.csv')
    for i in range(len(df)):
        tmp = {}
        tmp['wafernum'] = df.iloc[i]['wafernum']
        tmp['feature'] = df.iloc[i]['feature']
        tmp['value'] = df.iloc[i]['value']
        tmp['hdd_model'] = df.iloc[i]['hdd_model']
        category = find_category(df.iloc[i]['feature'])
        new_dict[category].append(tmp)
    # alert_df = df[df['outlier'] == 1][['Product', 'HDD_Model', 'Head_Site', 'Disk', 'wafernum', 'parameter_name']]
    # dat = []
    # for i, j in alert_df.iterrows():
    #     j = dict(j)
    #     j['raw_index'] = i
    #     dat.append(j)
    context = {
        'data': new_dict
    }
    # for i in new_dict:
    #     print(i)
    #     for j in new_dict[i]:
    #         print(j['wafernum'], j['feature'], j['value'], j['hdd_model'])
    #     print('--------------')


    return render(request, 'alert/alert.html', context)


def columns2dictionary(df):
    """
    该字典key为前端准备显示的所有多选字段名, value为数据库对应的字段名
    从DataFrame里读取生成, key即是value, 所见即所得
    """
    dictionary = {col: col for col in df.columns}

    return dictionary


def get_distinct_list(df, column):
    """
    获取一个feature下的不同的值，通过unique()函数
    改list返回可作为画图中的legend
    """
    # print(df[column].unique())
    l = df[column].unique()
    return l


def search(request, column, kw, df):
    try:
        df = df
        l = df.values.flatten().tolist()
        results_list = []
        for element in l:
            option_dict = {'name': element,
                           'value': element,
                           }
            results_list.append(option_dict)
        res = {
            "success": True,
            "results": results_list,
            "code": 200,
        }
    except Exception as e:
        res = {
            "success": False,
            "errMsg": e,
            "code": 0,
        }
    return HttpResponse(json.dumps(res, ensure_ascii=False),
                        content_type="application/json charset=utf-8")  # 返回结果必须是json格式


def choose_file(request):
    file_list_dict = dict(six.iterlists(request.GET))
    file_list = os.path()
    return file_list


def showdata(request, df=DF):
    # data = dict(six.iterlists(request.GET))
    con = {
        'alldata': df.to_html(),
    }
    return HttpResponse(json.dumps(con, ensure_ascii=False),
                        content_type="application/json charset=utf-8")


def query(request, data=DF):
    form_dict = dict(six.iterlists(request.GET))
    print('query', form_dict)
    df = data
    # box = []
    if form_dict:
        global x_feature, y_feature, box
        x_feature = form_dict['Feature1'][0]
        y_feature = form_dict['Feature2'][0]
        box = [x_feature, y_feature]
        multi_con = form_dict['Feature_opt[]']
        for i in multi_con:
            box.append(i)
        kpi = get_kpi(df, x_feature)
        df = df.loc[:, box]
    box_df = pd.DataFrame(df)
    print('aaaaaaa', x_feature, y_feature, kpi)
    context = {
        "df_mean": kpi["df_mean"],
        "df_std": kpi["df_std"],
        "df_median": kpi["df_median"],
        'data': df.to_html(),
        'data_': box_df.to_html(),
    }
    return HttpResponse(json.dumps(context, ensure_ascii=False),
                        content_type="application/json charset=utf-8")  # 返回结果必须是json格式


def query1(request, data=DF):
    form_dict = dict(six.iterlists(request.GET))
    print('query1', form_dict)
    if form_dict:
        global process_choose, query1_data
        process_choose = str(form_dict['process_choose[]'][0])
        print('process_choose', process_choose)
        query1_data = DF[DF['Process'] == process_choose]
    context = {
        "process_choose": 1,
        "query1_data": query1_data.to_json(),
    }
    return HttpResponse(json.dumps(context, ensure_ascii=False),
                        content_type="application/json charset=utf-8")  # 返回结果必须是json格式


def plot(request):
    type = list(dict(six.iterlists(request.GET)).keys())[0]
    # item = dict(six.iterlists(request.GET)).keys()
    print('===============', type, '==================')

    if type == 'Combine':
        chart = echarts_barline(DF, x_feature, y_feature, box)
    elif type == 'Line':
        chart = echarts_myline(DF, x_feature, y_feature, box)
    elif type == 'Stack':
        chart = echarts_stackbar(DF, x_feature, y_feature, box)

    elif type == 'Plot':
        chart = page_simple_layout()
        # chart = echarts_two_test(query1_data, process_choose)

    chart = chart.dump_options()

    total_trend = json.loads(chart)
    # print('total_trend', type(total_trend))
    context = {
        'total_trend': total_trend,
    }
    return HttpResponse(json.dumps(context, ensure_ascii=False),
                        content_type="application/json charset=utf-8")


def blog(request):
    mselect_dict = {}
    form_dict = dict(six.iterlists(request.GET))
    df = DF.iloc[0:50]
    dct = columns2dictionary(df)
    for key, value in dct.items():
        mselect_dict[key] = {}
        mselect_dict[key]['select'] = value
        mselect_dict[key]['options'] = get_distinct_list(df, value)  # 以后可以后端通过列表为每个多选控件传递备选项
    context = {
        'mselect_dict': mselect_dict,
    }
    return render(request, 'visual/blog_main_display.html', context)

def overview(request):
    form_dict = dict(six.iterlists(request.GET))
    source_path = 'C:/Users/1000300246/Desktop/test_folder/'
    df = pd.read_csv(source_path + 'all3prod_hddsumec_2023wk35.csv')
    # profile = ProfileReport(df, title="Profiling Report")
    # profile.to_file("C:/Users/1000300246/Desktop/test_folder/your_report.html")
    context = {
        'mselect_dict': df,
    }
    return render(request, 'visual/your_report.html')

def choose_path_file():
    import os
    current_address = os.path.dirname(os.path.abspath(__file__))
    for parent, dirnames, filenames in os.walk(current_address):
        # Case1: traversal the directories
        for dirname in dirnames:
            print("Parent folder:", parent)
            print("Dirname:", dirname)
        # Case2: traversal the files
        for filename in filenames:
            print("Parent folder:", parent)
            print("Filename:", filename)

def generate_plot_data(df, by, para_value):
    # 所有数据点 散点
    scatter_data = []
    fit_data = {}
    # fit出来的那条线的数据
    fit_aver_data = []
    df_ = df.dropna(subset=[para_value])
    if by == 'Date':
        for i, it in df_.iterrows():
            x = df_.loc[i, by]
            y = df_.loc[i, para_value]
            scatter_data.append([x, y])
            if x not in fit_data:
                fit_data[x] = []
            fit_data[x].append(y)
        for i in fit_data:
            tmp = [i]
            if len(fit_data[i]) > 1:
                tmp.append(np.mean(fit_data[i]))
            else:
                tmp.append(fit_data[i][0])
            fit_aver_data.append(tmp)
    elif by == 'Wafernum':
        x = df_[by].tolist()
        y = df_[para_value].tolist()
        df_['x_index'] = df_['Wafernum']
        df_['x_index'] = pd.factorize(df_['x_index'])[0].astype(int)
        df_['x_index'] = df_['x_index'].add(1)
        sp = csaps.UnivariateCubicSmoothingSpline(df_['x_index'].tolist(), y, smooth=0.8)  # 1e-16
        y_fit = sp(df_['x_index'].tolist())
        for i in range(len(x)):
            tmp_fit = [x[i], y_fit[i]]
            tmp_scatter = [x[i], y[i]]
            fit_aver_data.append(tmp_fit)
            scatter_data.append(tmp_scatter)
    print('fit_aver_data', fit_aver_data)
    print('scatter_data', scatter_data)
    return fit_aver_data, scatter_data

def get_process_name(request):
    file_dir = 'C:/Users/1000300246/Desktop/test_folder/'
    group_ls = []
    file = ''
    flag = ''
    dict = {}
    #接收参数
    independent = request.POST.get("independent")
    parameter = request.POST.get("dependent")
    by = request.POST.get("by")
    product = request.POST.get("product")
    hddmodel = request.POST.get("hddmodel")
    wec = request.POST.get("wec")
    hsite = request.POST.get("hsite")
    disk = request.POST.get("disk")
    # grade = request.POST.get("grade")

    # print('-------------', product, hddmodel, wec)
    # print('by---------', by, independent,parameter )
    #按什么分组
    # if independent == 'Magnetic':
    #     group_ls = ['PRODUCT', 'HDD_Model', 'WAFER_EC', 'HEAD_SITE', 'DISK_SITE', 'DISK', 'GRADE']
    #     flag = 'Magnetic'
    # elif independent == 'YC':
    #     group_ls = ['PRODUCT', 'HDD_Model', 'WAFER_EC', 'HEAD_SITE', 'DISK_SITE', 'DISK', 'GRADE']
    #     flag = 'Test'
    # elif independent == 'XTI Degradation':
    #     group_ls = ['PRODUCT', 'HDD_Model', 'WAFER_EC', 'HEAD_SITE', 'DISK_SITE', 'DISK', 'GRADE']
    #     flag = 'XTI Degradation'
    # else:
    #     flag = 'Test'

    #确认文件
    # df=''
    # para_value=''
    # for f in os.listdir(file_dir):
    #     obj = re.search(independent, f)
    #     if obj:
    #         file = obj.string
    #         break
    # print('文件时', file)
    # if file != '':
    #     file_name = file_dir + '/' + file
    #     df = pd.read_csv(file_name)


    df = pd.read_csv(file_dir + 'all3prod_hddsumec_2023wk35.csv')
    # 确认参数
    para_value = ''
    for col in df.columns:
        if parameter in col:
            para_value = col
            break
    print('参数是', para_value)

    #去掉date或者wafer中为空值的部分
    df = df.dropna(subset=[by])

    #origin df
    df = df[(df['Product'] == product) & (df['hdd_model'] == hddmodel) & (df['Wafer_EC'] == wec) & (df['Head_site'] == hsite) & (df['disk'] == disk)]
    scatter_data = generate_plot_data(df,by, para_value)[0]
    fit_aver_data = generate_plot_data(df,by, para_value)[1]
    pho_df = df[(df['Product'] == product) & (df['hdd_model'] == hddmodel) & (df['Wafer_EC'] == wec) & (df['Head_site'] == 'PHO')]
    pho_dic = {}
    disk_ls = set(df['disk'].tolist())
    for i in disk_ls:
        pho_dic[i] = {}
        pho_df_ = pho_df.copy()
        pho_df_ = pho_df_[(pho_df_['disk'] == i)]
        pho_dic[i]['scatter_data'] = generate_plot_data(pho_df_, by, para_value)[0]
        pho_dic[i]['fit_aver_data'] = generate_plot_data(pho_df_, by, para_value)[1]


    # df_ = df.copy()
    # if by=='Date':
    #     df_['new_date'] = 0
    #     for i, it in df_.iterrows():
    #         obj = df_.loc[i, 'Date']
    #         obj_ = datetime.datetime.strptime(str(obj), "%m/%d/%Y")
    #         df_.loc[i, 'new_date'] = (obj_ - datetime.datetime(1970, 1, 1)).total_seconds()
    #     df_.sort_values(by=['new_date'], ascending=True, inplace=True)
    # print("数据是", df_)




    # x = df_[by].tolist()
    # y = df_[para_value].tolist()
    # dic_try = {"x": df_[by].tolist(), "y": df_[para_value].tolist(), "by":by, "para":para_value}

    #     if para_value != '':
    #         # by date 分组
    #         df_list = []
    #         for group in group_ls:
    #             transposed_df = df.pivot_table(index=by, columns=group, values=para_value, aggfunc='mean')
    #             transposed_df.reset_index(inplace=True)
    #             df_list.append(transposed_df)
    #         all = df_list[0]
    #         for i in range(1, len(df_list)):
    #             all = pd.merge(all, df_list[i], left_on=by, right_on=by)
    #         all.replace({np.nan: '-'}, inplace=True)
    #         if by == 'Date':
    #             # 按照时间排序，确保画图时的时间轴是正确的
    #             all['new_date'] = 0
    #             for i, it in all.iterrows():
    #                 obj = all.loc[i, 'Date']
    #                 obj_ = datetime.datetime.strptime(obj, "%m/%d/%Y")
    #                 all.loc[i, 'new_date'] = (obj_ - datetime.datetime(1970, 1, 1)).total_seconds()
    #             all.sort_values(by=['new_date'], ascending=True, inplace=True)
    #         #将所有分组以字典的形式传到前端画图
    #         for i in all.columns:
    #             dict[i] = np.array(all[i]).tolist()
    #     else:
    #         flag = 'Test_no_para'
    # df_pho = DF[(DF['PRODUCT'] == product_choose) & (DF['HDD_Model'] == model_choose) & (DF['HEAD_SITE'] == 'PHO')]
    # df_pho = df_pho.dropna()
    # df_tho = DF[(DF['PRODUCT'] == product_choose) & (DF['HDD_Model'] == model_choose) & (DF['HEAD_SITE'] == 'THO')]
    # df_tho = df_tho.dropna()
    # pho_qty = [np.array(df_pho['QTY_6400']).tolist(), np.array(df_pho['MCW_MD']).tolist(),
    #            np.array(df_pho['Resi_pACC']).tolist()]
    # pho_line = [np.array(df_pho['Resi_OWP_MD_Post']).tolist(), np.array(df_pho['Resi_FinalSER']).tolist()]
    # tho_qty = [np.array(df_tho['QTY_6400']).tolist(), np.array(df_tho['MCW_MD']).tolist(),
    #            np.array(df_tho['Resi_pACC']).tolist()]
    # tho_line = [np.array(df_tho['Resi_OWP_MD_Post']).tolist(), np.array(df_tho['Resi_FinalSER']).tolist()]
    # col_name = ['QTY_6400', 'MCW_MD', 'Resi_pACC', 'Resi_OWP_MD_Post', 'Resi_FinalSER']
    # print(dict)
    # print('filename', file_name)
    # print('para', para_value)
    lis1 = ['a', 'b', 'c', 'd', 'Fri', 'Sat', 'Sun']
    lis2 = [150, 230, 224, 218, 135, 147, 260]
    trans_dict = {"by":by, "parameter": para_value, "scatter_data":scatter_data, "fit_aver_data": fit_aver_data}
    return render(request, './visual/plot.html', {
        # "pho_qty": pho_qty,
        # "pho_line": pho_line,
        # "tho_qty": tho_qty,
        # "tho_line": tho_line,
        # "col_name": col_name,
        # "pho_date": np.array(df_pho['Date']).tolist(),
        # "tho_date": np.array(df_tho['Date']).tolist(),
        "lis1": lis1,
        "lis2": lis2,
        "scatter_data":scatter_data,
        "fit_aver_data": fit_aver_data,
        "product":product,
        "hddmodel":hddmodel,
        "wec":wec,
        "hsite":hsite,
        "disk":disk,
        # "grade":grade,
        "pho_dic": pho_dic,
        "independent": independent,
        "parameter": para_value,
        "dict" : dict,
        "flag" : 'scatter_fit',
        "trans_dict" : trans_dict,
        "by_":by
    })
