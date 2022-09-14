from pyecharts.charts import Line, Bar, Scatter
from pyecharts import options as opts
from pyecharts.faker import Faker
import numpy as np

def echarts_mybar(df, x, y):
    df = df.iloc[:30, :]
    x_axis = np.array(df[x]).tolist()
    y_axis = np.array(df[y]).tolist()
    x_axis, y_axis = zip(*sorted(zip(x_axis, y_axis)))
    bar = (
        Bar()
        .add_xaxis(x_axis)
        .add_yaxis("纵坐标名字",y_axis)
        .set_global_opts(title_opts=opts.TitleOpts(title="主标题", subtitle="副标题"),
                         toolbox_opts=opts.ToolboxOpts(),
                         datazoom_opts=opts.DataZoomOpts(is_show=True,
                         range_start=0,  # 显示区域的开始位置，默认是20
                         range_end=80,  # 显示区域的结束位置，默认是80
                         orient='horizontal'  ##缩放区域空值条所放的位置
                         )

        )
        .set_series_opts(label_opts=opts.LabelOpts(position='insideTop', color='white', font_size=12, is_show=False))
    )
    return bar

def echarts_myscatter(df, x, y):
    df = df.iloc[:30, :]
    x_axis = np.array(df[x]).tolist()
    y_axis = np.array(df[y]).tolist()
    x_axis, y_axis = zip(*sorted(zip(x_axis, y_axis)))
    x_axis = [str(i) for i in x_axis]
    # y_axis = [int(i) for i in y_axis]
    print('===========',type(x_axis), type(y_axis),type(x_axis[0]), type(y_axis[0]),'===============')
    scatter = (
        # 散点图
        # 初始化
        Scatter(init_opts=opts.InitOpts(width="900px", height="600px"))
        .add_xaxis(xaxis_data=x_axis)
        .add_yaxis(
            series_name="",
            y_axis=y_axis,
            # 标记的大小
            symbol_size=8,
            # 标记的图形
            symbol=None,
            # 是否选中图例
            is_selected=True,
            # 系列 label 颜色
            # color='#00CCFF',
            label_opts=opts.LabelOpts(is_show=True),  # 不显示标签
        )
        # 系统配置项
        .set_series_opts()
        # 全局配置项
        .set_global_opts(
        #     # x轴配置
        #     xaxis_opts=opts.AxisOpts(
        #         name='x轴',
        #         name_location='center',
        #         name_gap=15,
        #         # 坐标轴类型 'value': 数值轴
        #         type_="value",
        #         # 分割线配置项
        #         splitline_opts=opts.SplitLineOpts(is_show=True)  # 显示分割线
        #     ),
        #     # y轴配置
        #     yaxis_opts=opts.AxisOpts(
        #         name='y轴',
        #         # 坐标轴类型 'value': 数值轴
        #         # type_="value",
        #         # 坐标轴刻度配置项
        #         axistick_opts=opts.AxisTickOpts(is_show=True),  # 显示刻度
        #         # 分割线配置项
        #         splitline_opts=opts.SplitLineOpts(is_show=True),  # 显示分割线
        #     ),
        #     # 提示框配置项
            toolbox_opts=opts.ToolboxOpts()
        )
    )
    return scatter

def echarts_myline(df, x, y):
    df = df.iloc[:30, :]
    x_axis = np.array(df[x]).tolist()
    y_axis = np.array(df[y]).tolist()
    x_axis, y_axis = zip(*sorted(zip(x_axis, y_axis)))
    x_axis, y_axis=list(x_axis), list(y_axis)
    x_axis = [str(i) for i in x_axis]
    # y_axis = [int(i) for i in y_axis]
    line = (
        Line()
        .set_global_opts(
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
        .add_xaxis(x_axis)
        .add_yaxis(
            series_name="基本折线图",
            y_axis=y_axis,
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=True),
        )
    )
    return line


def echarts_stackbar(df,  # 传入数据df，应该是一个行索引为date的时间序列面板数据
             df_gr=None,  # 传入同比增长率df，可以没有
             datatype='ABS',  # 主Y轴形式是绝对值，增长率还是份额，用来确定一些标签格式，默认为绝对值
             line_name=None,
             ) -> Bar:
    axislabel_format = '{value}'  # 主Y轴默认格式
    max = df[df>0].sum(axis=1).max()  # 主Y轴默认最大值
    min = df[df<=0].sum(axis=1).min()  # 主Y轴默认最小值
    if datatype in ['SHARE', 'GR']:  # 如果主数据不是绝对值形式而是份额或增长率如何处理
        df = df.multiply(100).round(2)
        axislabel_format = '{value}%'
        max = 100
        min = 0
    if df_gr is not None:
        df_gr = df_gr.multiply(100).round(2) # 如果有同比增长率，原始数*100呈现

    if df.empty is False:
        stackbar = (
            Bar()
            .add_xaxis(df.index.tolist())
        )
        for i, item in enumerate(df.columns): # 预留的枚举，这个方法以后可以根据输入对象不同从单一柱状图变成堆积柱状图
            stackbar.add_yaxis(item,
                          df[item].values.tolist(),
                          stack='总量',
                          label_opts=opts.LabelOpts(is_show=False),
                          z_level=1,  # 指定渲染图层，低版本pyecharts可能因为没有该参数报错
                          )
        if df_gr is not None:  # 如果有同比增长率数据则加入次Y轴
            stackbar.extend_axis(
                yaxis=opts.AxisOpts(
                    name=line_name,
                    type_="value",
                    axislabel_opts=opts.LabelOpts(formatter="{value}%"),
                )
            )
        stackbar.set_global_opts(
            legend_opts=opts.LegendOpts(pos_top='5%', pos_left='10%', pos_right='60%'),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            tooltip_opts=opts.TooltipOpts(trigger='axis',
                                          axis_pointer_type='cross',
                                          ),
            xaxis_opts=opts.AxisOpts(type_='category',
                                     boundary_gap=True,
                                     axislabel_opts=opts.LabelOpts(rotate=90), # x轴标签方向rotate有时能解决拥挤显示不全的问题
                                     splitline_opts=opts.SplitLineOpts(is_show=False,
                                                                       linestyle_opts=opts.LineStyleOpts(
                                                                           type_='dotted',
                                                                           opacity=0.5,
                                                                       )
                                                                       )
                                     ),
            yaxis_opts=opts.AxisOpts(max_=max,
                                     min_=min,
                                     type_="value",
                                     axislabel_opts=opts.LabelOpts(formatter=axislabel_format),
                                     # axistick_opts=opts.AxisTickOpts(is_show=True),
                                     splitline_opts=opts.SplitLineOpts(is_show=True,
                                                                       linestyle_opts=opts.LineStyleOpts(
                                                                           type_='dotted',
                                                                           opacity=0.5,
                                                                       )
                                                                       )
                                     ),
        )
        if df_gr is not None:
            line = (
                Line()
                    .add_xaxis(xaxis_data=df_gr.index.tolist())
                    .add_yaxis(
                    series_name=line_name,
                    yaxis_index=1,
                    y_axis=df_gr.values.tolist(),
                    label_opts=opts.LabelOpts(is_show=False),
                    linestyle_opts=opts.LineStyleOpts(width=3),
                    symbol_size=8,
                    itemstyle_opts=opts.ItemStyleOpts(border_width=1, border_color='', border_color0='white'),
                    z_level=2  # 渲染图层大于柱状图，保证线图在上方，低版本pyecharts可能因为没有该参数报错
               )
            )
    else:
        stackbar = (Bar())
    if df_gr is not None:
        return stackbar.overlap(line) # 如果有次坐标轴最后要用overlap方法组合
    else:
        return stackbar




