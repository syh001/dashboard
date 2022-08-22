from django.shortcuts import render
from django.http import HttpResponse
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
# Create your views here.

# is sql important?
# how WD manage data/dataset?
# which data format is most often used?

def index(request):
    # 标准sql语句，此处为测试返回数据库data表的数据条目n，之后可以用python处理字符串的方式动态扩展
    # sql = "Select count(*) from data" 
    df = pd.read_excel('C:/Users/sas053/Desktop/jmp_feature_importance.xlsx') #将sql语句结果读取至Pandas Dataframe
    
    df = df.iloc[0:3]
    # certain_one.columns = [''] * len(certain_one.columns)
    # certain_one = pd.DataFrame(certain_one.iloc[0:2,1], header = None)
    print(type(pd.DataFrame(df.iloc[0,1:3])), '\n', df)
    # certain_one = np.mean(certain_one)
    # print(type(certain_one.keys()))
    # certain_one = certain_one.columns
    context = {'data': df}
    
    return render(request, 'visual/display.html', context)
    # return HttpResponse(df.to_html(max_cols=10,show_dimensions=True)) #渲染，这里暂时渲染为最简单的HttpResponse，以后可以扩展
