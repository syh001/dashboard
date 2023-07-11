from pyecharts.charts import Line, Bar, Scatter, Pie, Timeline, Grid, Page, Tab
from pyecharts import options as opts
from pyecharts.faker import Faker
import numpy as np
from pyecharts.globals import ThemeType


def echarts_stackbar(df, x, y, box) -> Bar:
    print('x:', x)
    print('y', y)
    print('box', box)
    bar = Bar(init_opts=opts.InitOpts())
    bar.add_xaxis(df[x].tolist())
    bar.add_yaxis(y, df[y].tolist())
    for i in range(len(box)):
        bar.add_yaxis(box[i], df[box[i]].tolist(), stack="stack")
    bar.set_global_opts(title_opts=opts.TitleOpts(title="stackbar-chart"),
                         toolbox_opts=opts.ToolboxOpts(),
                         datazoom_opts=opts.DataZoomOpts(is_show=True,
                         range_start=0,  # 显示区域的开始位置，默认是20
                         range_end=80,  # 显示区域的结束位置，默认是80
                         orient='horizontal'  ##缩放区域空值条所放的位置
                        )

        ).set_series_opts(label_opts=opts.LabelOpts(position='insideTop', color='white', font_size=12, is_show=False))
    bar1 = bar.dump_options()
    print('bar', type(bar))
    print('bar1', type(bar1))
    return bar

def echarts_myline(df, x, y, box):
    line = Line(init_opts=opts.InitOpts())
    line.add_xaxis(df[x].tolist())
    line.add_yaxis(y, df[y].tolist())
    for i in range(len(box)):
        line.add_yaxis(box[i], df[box[i]].tolist(), stack="stack")
    line.set_global_opts(title_opts=opts.TitleOpts(title="line-chart"),
                         toolbox_opts=opts.ToolboxOpts(),
                         datazoom_opts=opts.DataZoomOpts(is_show=True,
                         range_start=0,  # 显示区域的开始位置，默认是20
                         range_end=80,  # 显示区域的结束位置，默认是80
                         orient='horizontal'  ##缩放区域空值条所放的位置
                        )

        ).set_series_opts(label_opts=opts.LabelOpts(position='insideTop', color='white', font_size=12, is_show=False))
    return line


def echarts_barline(df, x, y, box):
    #规定box中辅助维度后两维画折线图，其余的画柱状图
    from pyecharts import options as opts
    from pyecharts.charts import Bar, Grid, Line

    # x_data = ["{}月".format(i) for i in range(1, 13)]
    x_data = np.array(df[x]).tolist()
    bar = (
        Bar()
        .add_xaxis(x_data)
        .add_yaxis(
            y,
            np.array(df[y]).tolist(),
            yaxis_index=0,
            color="#d14a61",
        )
        .add_yaxis(
            box[-2],
            np.array(df[box[-2]]).tolist(),
            yaxis_index=1,
            color="#5793f3",
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                name=y,
                type_="value",
                min_=0,
                max_=100,
                position="right",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#d14a61")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
            )
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value",
                name=box[-1],
                min_=0,
                max_=1,
                position="left",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#675bba")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} %"),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            )
        )
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                name=box[-2],
                min_=0,
                max_=100,
                position="right",
                offset=80,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#5793f3")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
            ),
            title_opts=opts.TitleOpts(title="Grid-多 Y 轴示例"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            toolbox_opts=opts.ToolboxOpts(),
            datazoom_opts=opts.DataZoomOpts(is_show=True,
                                            range_start=0,
                                            range_end=80,
                                            orient='horizontal')

        )
    )

    line = (
        Line()
        .add_xaxis(x_data)
        .add_yaxis(
            box[-1],
            np.array(df[box[-1]]).tolist(),
            yaxis_index=2,
            color="#675bba",
            label_opts=opts.LabelOpts(is_show=False),
        )
    )

    bar.overlap(line)
    grid = Grid()
    grid.add(bar, opts.GridOpts(pos_left="5%", pos_right="20%"), is_control_axis_index=True)

    return grid

def test1():

    bar = (
        Bar()
        .add_xaxis(["{}月".format(i) for i in range(1, 13)])
        .add_yaxis(
            "蒸发量", [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3],
            yaxis_index=0,
            color="#d14a61",
        )
        .add_yaxis(
            "降水量", [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3],
            yaxis_index=1,
            color="#5793f3",
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="蒸发量", type_="value", min_=0, max_=250,
                position="right",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#d14a61")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
            )
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value", name="温度", min_=0, max_=25,
                position="left",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#675bba")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            )
        )
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                name="降水量", min_=0, max_=250,
                position="right",
                offset=80,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#5793f3")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
            ),
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False, type_="inside", xaxis_index=[0, 0], range_end=100),
                opts.DataZoomOpts(
                    is_show=True, xaxis_index=[0, 1], pos_top="97%", range_end=100),
            ],
            title_opts=opts.TitleOpts(title="Grid-Overlap-多 X/Y 轴示例"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(pos_left="25%"),
            # toolbox_opts=opts.ToolboxOpts(),
            # datazoom_opts=opts.DataZoomOpts(
            #                                 is_show=True,
            #                                 range_start=0,
            #                                 range_end=80,
            #                                 orient='horizontal')
        )
    )

    line = (
        Line()
        .add_xaxis(["{}月".format(i) for i in range(1, 13)])
        .add_yaxis(
            "平均温度", [2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2],
            yaxis_index=2,
            color="#675bba",
            label_opts=opts.LabelOpts(is_show=False),
        )
    )

    bar1 = (
        Bar()
        .add_xaxis(["{}月".format(i) for i in range(1, 13)])
        .add_yaxis(
            "蒸发量 1", [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3],
            color="#d14a61",
            xaxis_index=1,
            yaxis_index=3,
        )
        .add_yaxis(
            "降水量 2", [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3],
            color="#5793f3",
            xaxis_index=1,
            yaxis_index=4,
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="蒸发量", type_="value", min_=0, max_=250,
                position="right",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#d14a61")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
            )
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value", name="温度", min_=0, max_=25,
                position="left",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#675bba")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            )
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(grid_index=1),
            yaxis_opts=opts.AxisOpts(
                name="降水量", min_=0, max_=250,
                position="right",
                offset=80,
                grid_index=1,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#5793f3")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(pos_left="65%"),
            # toolbox_opts=opts.ToolboxOpts(),
            # datazoom_opts=opts.DataZoomOpts(
            #                                 is_show=True,
            #                                 range_start=0,
            #                                 range_end=80,
            #                                 orient='horizontal')
        )
    )

    line1 = (
        Line()
        .add_xaxis(["{}月".format(i) for i in range(1, 13)])
        .add_yaxis(
            "平均温度 1", [2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2],
            color="#675bba",
            label_opts=opts.LabelOpts(is_show=False),
            xaxis_index=1,
            yaxis_index=5,
        )
    )

    overlap_1 = bar.overlap(line)
    overlap_2 = bar1.overlap(line1)

    grid = (
        Grid(init_opts=opts.InitOpts(width="1200px", height="800px"))
        .add(
            overlap_1, grid_opts=opts.GridOpts(pos_right="58%"),
            is_control_axis_index=True
        )
        .add(
            overlap_2, grid_opts=opts.GridOpts(pos_left="58%"),
            is_control_axis_index=True)
    )
    print('567', type(grid))
    return grid

def test():
    bar = (
        Bar()
        .add_xaxis(["{}月".format(i) for i in range(1, 13)])
        .add_yaxis(
            "蒸发量", [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3],
            yaxis_index=0,
            color="#d14a61",
            stack='stack',
        )
        .add_yaxis(
            "降水量", [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3],
            yaxis_index=0,
            color="#5793f3",
            stack='stack',
        )
        # .extend_axis(
        #     yaxis=opts.AxisOpts(
        #         name="蒸发量", type_="value", min_=0, max_=250,
        #         position="right",
        #         axisline_opts=opts.AxisLineOpts(
        #             linestyle_opts=opts.LineStyleOpts(color="#d14a61")
        #         ),
        #         axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
        #     )
        # )
        .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value", name="温度", min_=0, max_=25,
                position="left",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#675bba")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            )
        )
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                name="降水量", min_=0, max_=500,
                position="right",
                # offset=80,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#5793f3")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
            ),
            title_opts=opts.TitleOpts(title="Grid-Overlap-多 X/Y 轴示例"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(pos_left="25%"),
            # toolbox_opts=opts.ToolboxOpts(),
            # datazoom_opts=opts.DataZoomOpts(
            #                                 xaxis_index=0,
            #                                 # is_show=True,
            #                                 # range_start=0,
            #                                 # range_end=80,
            #                                 orient='horizontal',pos_bottom='50%'
            # )
        )
    )

    line = (
        Line()
        .add_xaxis(["{}月".format(i) for i in range(1, 13)])
        .add_yaxis(
            "平均温度", [2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2],
            yaxis_index=1,
            color="#675bba",

            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            "平均温度2", [5.0, 2.8, 1.3, 4.5, 6.3, 10.2, 18, 23.4, 2, 9, 10, 7],
            yaxis_index=1,
            color="#675bbb",
            label_opts=opts.LabelOpts(is_show=False),
        )

    )

    bar1 = (
        Bar()
        .add_xaxis(["{}月".format(i) for i in range(1, 13)])
        .add_yaxis(
            "蒸发量 1", [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3],
            color="#d14a61",
            xaxis_index=1,
            yaxis_index=2,
            stack='stack1',
        )
        .add_yaxis(
            "降水量 2", [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3],
            color="#5793f3",
            xaxis_index=1,
            yaxis_index=2,
            stack='stack1',
        )
        # .extend_axis(
        #     yaxis=opts.AxisOpts(
        #         name="蒸发量", type_="value", min_=0, max_=250,
        #         position="right",
        #         axisline_opts=opts.AxisLineOpts(
        #             linestyle_opts=opts.LineStyleOpts(color="#d14a61")
        #         ),
        #         axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
        #     )
        # )
        .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value", name="温度", min_=0, max_=25,
                position="left",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#675bba")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            )
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(grid_index=1),
            yaxis_opts=opts.AxisOpts(
                name="降水量", min_=0, max_=500,
                position="right",
                # offset=80,
                grid_index=1,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#5793f3")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(pos_left="25%", pos_top="50%"),
            # toolbox_opts=opts.ToolboxOpts(),
            datazoom_opts=opts.DataZoomOpts(
                xaxis_index=1,
                #                             is_show=True,
                #                             range_start=0,
                #                             range_end=80,
                                            orient='horizontal',
                pos_bottom='20%'
            )
        )
    )

    line1 = (
        Line()
        .add_xaxis(["{}月".format(i) for i in range(1, 13)])
        .add_yaxis(
            "平均温度 1", [2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2],
            color="#675bba",
            label_opts=opts.LabelOpts(is_show=False),
            xaxis_index=1,
            yaxis_index=3,
        )
    )

    overlap_1 = bar.overlap(line)
    overlap_2 = bar1.overlap(line1)

    grid = (
        Grid(init_opts=opts.InitOpts(width="1200px", height="800px"))
        .add(
            overlap_1, grid_opts=opts.GridOpts(pos_bottom="60%"),
            is_control_axis_index=True
        )
        .add(
            overlap_2, grid_opts=opts.GridOpts(pos_top="60%"),
            is_control_axis_index=True)

    )
    return grid

def echarts_two_test(df, process_choose):
    process = process_choose
    df_PHO = df[df['Site'] == 'PHO']
    
    x_PHO = np.array(df_PHO['Date']).tolist()
    qty_nor = np.array(df_PHO['QTY Nor_OWc']).tolist()
    qty_low = np.array(df_PHO['QTY Low_OWc']).tolist()
    qty_high = np.array(df_PHO['QTY High_OWc']).tolist()
    qty_all = np.array(df_PHO['QTY All data']).tolist()
    acc_nor = np.array(df_PHO['Nor_OWc']).tolist()
    acc_low = np.array(df_PHO['Low_OWc']).tolist()
    acc_high = np.array(df_PHO['High_OWc']).tolist()
    acc_all = np.array(df_PHO['All data']).tolist()

    df_THO = df[df['Site'] == 'THO']
    x_THO = np.array(df_THO['Date']).tolist()
    qty_nor_tho = np.array(df_THO['QTY Nor_OWc']).tolist()
    qty_low_tho = np.array(df_THO['QTY Low_OWc']).tolist()
    qty_high_tho = np.array(df_THO['QTY High_OWc']).tolist()
    qty_all_tho = np.array(df_THO['QTY All data']).tolist()
    acc_nor_tho = np.array(df_THO['Nor_OWc']).tolist()
    acc_low_tho = np.array(df_THO['Low_OWc']).tolist()
    acc_high_tho = np.array(df_THO['High_OWc']).tolist()
    acc_all_tho = np.array(df_THO['All data']).tolist()
    
    # bar1 = (
    #     Bar()
    #     .add_xaxis(x_PHO)
    #     .add_yaxis(
    #         series_name='qty_nor_pho',
    #         y_axis=qty_nor,
    #         stack="stack1"
    #     ).add_yaxis(
    #         series_name='qty_low_pho',
    #         y_axis=qty_low,
    #         stack="stack1"
    #     ).add_yaxis(
    #         series_name='qty_high_pho',
    #         y_axis=qty_high,
    #         stack="stack1"
    #     ).add_yaxis(
    #         series_name='qty_all_pho',
    #         y_axis=qty_all,
    #         stack="stack1"
    #     )
    #     .extend_axis(
    #         yaxis=opts.AxisOpts(
    #             name='line',position='left',min_=101,max_=105,
    #         )
    #     )
    #     .set_global_opts(yaxis_opts=opts.AxisOpts(position='right',
    #                                              min_=0,
    #                                              max_=500,
    #                                              name='qty'
    #
    #                                              ),
    #                      title_opts=opts.TitleOpts(title="Grid-Bar"))
    # )
    # line1 = (
    #     Line()
    #     .add_xaxis(x_PHO)
    #     .add_yaxis(
    #         series_name='acc_low',
    #         y_axis=acc_low,
    #         yaxis_index=1,
    #         is_connect_nones=True,
    #         # stack="stack3"
    #     ).add_yaxis(
    #         series_name='acc_high',
    #         y_axis=acc_high,
    #         yaxis_index=1,
    #         is_connect_nones=True,
    #         # stack="stack3"
    #     ).add_yaxis(
    #         series_name='acc_all',
    #         y_axis=acc_all,
    #         yaxis_index=1,
    #         is_connect_nones=True,
    #         # stack="stack3"
    #     )
    # )
    # bar2 = (
    #     Bar()
    #     .add_xaxis(x_THO)
    #     .add_yaxis(
    #         series_name='qty_nor_tho',
    #         y_axis=qty_nor_tho,
    #         # yaxis_index=2,
    #         stack="stack2"
    #     ).add_yaxis(
    #         series_name='qty_low_tho',
    #         y_axis=qty_low_tho,
    #         # yaxis_index=2,
    #         stack="stack2"
    #     ).add_yaxis(
    #         series_name='qty_high_tho',
    #         y_axis=qty_high_tho,
    #         # yaxis_index=2,
    #         stack="stack2"
    #     ).add_yaxis(
    #         series_name='qty_all_tho',
    #         y_axis=qty_all_tho,
    #         # yaxis_index=2,
    #         stack="stack2"
    #     ).set_global_opts(
    #         # xaxis_opts=opts.AxisOpts(grid_index=1),
    #         # yaxis_opts=opts.AxisOpts(
    #         #     grid_index=1,
    #         # ),
    #         title_opts=opts.TitleOpts(title="Grid-Line", pos_top="48%"),
    #         legend_opts=opts.LegendOpts(pos_top="48%"),
    #     )
    # )
    # p1 = bar1.overlap(line1)
    # grid = (
    #     Grid()
    #     .add(p1, grid_opts=opts.GridOpts(pos_bottom="60%"))
    #     .add(bar2, grid_opts=opts.GridOpts(pos_top="60%"))
    # )
    # return grid

    bar = Bar()
    bar.add_xaxis(xaxis_data=x_PHO)
    bar.add_yaxis(
        series_name='qty_nor_pho',
        y_axis=qty_nor,
        yaxis_index=0,
        stack="stack"
    ).add_yaxis(
        series_name='qty_low_pho',
        y_axis=qty_low,
        yaxis_index=0,
        stack="stack"# 使用的y轴的index，在单个图表实例中存在多个y轴的时候有用
    ).add_yaxis(
        series_name='qty_high_pho',
        y_axis=qty_high,
        yaxis_index=0,
        stack="stack"
    ).add_yaxis(
        series_name='qty_all_pho',
        y_axis=qty_all,
        yaxis_index=0,
        stack="stack"
    )
    bar.extend_axis(
        yaxis=opts.AxisOpts(
            type_='value',
            name='lineacc',
            position='left',
            min_=80,
            max_=110,
            axisline_opts=opts.AxisLineOpts(
                is_show=False,

            ),

        )
    )
    bar.set_global_opts(yaxis_opts=opts.AxisOpts(position='right',
                                                 min_=0,
                                                 max_=500,
                                                 name='qty'

                                                 ),
                        legend_opts=opts.LegendOpts(
                            pos_left='left',
                            pos_top='middle',
                            orient='vertical',
                            align='auto',
                        ),
                        title_opts=opts.TitleOpts(title=process+" pACC Trend by "+process+" Date PHO", pos_top='top'),
                        toolbox_opts=opts.ToolboxOpts(),
                        datazoom_opts=opts.DataZoomOpts(is_show=True,
                                                        range_start=0,  # 显示区域的开始位置，默认是20
                                                        range_end=80,  # 显示区域的结束位置，默认是80
                                                        orient='horizontal'  ##缩放区域空值条所放的位置
                                                        )

                        ).set_series_opts(
        label_opts=opts.LabelOpts(position='insideRight', color='white', font_size=12, is_show=False))
    line = Line()
    line.add_xaxis(x_PHO)
    line.add_yaxis(
        series_name='acc_nor',
        y_axis=acc_nor,
        yaxis_index=1,
        is_connect_nones=True,
        # stack="stack"
    ).add_yaxis(
        series_name='acc_low',
        y_axis=acc_low,
        yaxis_index=1,
        is_connect_nones=True,
        # stack="stack"  # 使用的y轴的index，在单个图表实例中存在多个y轴的时候有用
    ).add_yaxis(
        series_name='acc_high',
        y_axis=acc_high,
        yaxis_index=1,
        is_connect_nones=True,
        # stack="stack"
    ).add_yaxis(
        series_name='acc_all',
        y_axis=acc_all,
        yaxis_index=1,
        is_connect_nones=True,
        # stack="stack"
    )
    line.set_global_opts(title_opts=opts.TitleOpts(title="line-chart"),
                         toolbox_opts=opts.ToolboxOpts(),
                         legend_opts=opts.LegendOpts(
                             pos_left='left',
                             pos_top='middle',
                             orient='vertical',
                             align='auto',
                         ),
                         datazoom_opts=opts.DataZoomOpts(is_show=True,
                                                         range_start=0,  # 显示区域的开始位置，默认是20
                                                         range_end=80,  # 显示区域的结束位置，默认是80
                                                         orient='horizontal'  ##缩放区域空值条所放的位置
                                                         )

                         ).set_series_opts(
        label_opts=opts.LabelOpts(position='insideRight', color='white', font_size=12, is_show=False))


    bar1 = Bar()
    bar1.add_xaxis(xaxis_data=x_THO)
    bar1.add_yaxis(
        series_name='qty_nor_tho',
        y_axis=qty_nor_tho,
        yaxis_index=1,
        stack="stack"
    ).add_yaxis(
        series_name='qty_low_tho',
        y_axis=qty_low_tho,
        yaxis_index=1,
        stack="stack"  # 使用的y轴的index，在单个图表实例中存在多个y轴的时候有用
    ).add_yaxis(
        series_name='qty_high_tho',
        y_axis=qty_high_tho,
        yaxis_index=1,
        stack="stack"
    ).add_yaxis(
        series_name='qty_all_tho',
        y_axis=qty_all_tho,
        yaxis_index=1,
        stack="stack"
    )
    bar1.extend_axis(
        yaxis=opts.AxisOpts(
            type_='value',
            name='lineacc',
            position='left',
            min_=80,
            max_=110,
            axisline_opts=opts.AxisLineOpts(
                is_show=False,

            ),

        )
    )
    bar1.set_global_opts(
                        xaxis_opts=opts.AxisOpts(grid_index=1),
                        yaxis_opts=opts.AxisOpts(position='right',
                                                 min_=0,
                                                 max_=500,
                                                 name='qty',
                                                 # grid_index=1,

                                                 ),
                        legend_opts=opts.LegendOpts(
                            pos_left='left',
                            pos_top='middle%',
                            orient='vertical',
                            align='auto',
                        ),
                        title_opts=opts.TitleOpts(title=process + " pACC Trend by " + process + " Date THO",
                                                  pos_top='top'),
                        toolbox_opts=opts.ToolboxOpts(),
                        datazoom_opts=opts.DataZoomOpts(is_show=True,
                                                        range_start=0,  # 显示区域的开始位置，默认是20
                                                        range_end=80,  # 显示区域的结束位置，默认是80
                                                        orient='horizontal'  ##缩放区域空值条所放的位置
                                                        )

                        ).set_series_opts(
        label_opts=opts.LabelOpts(position='insideRight', color='white', font_size=12, is_show=False))
    line1 = Line()
    line1.add_xaxis(x_THO)
    line1.add_yaxis(
        series_name='acc_nor',
        y_axis=acc_nor_tho,
        xaxis_index=1,
        yaxis_index=3,
        is_connect_nones=True,
        # stack="stack"
    ).add_yaxis(
        series_name='acc_low',
        y_axis=acc_low_tho,
        xaxis_index=1,
        yaxis_index=3,
        is_connect_nones=True,
        # stack="stack"  # 使用的y轴的index，在单个图表实例中存在多个y轴的时候有用
    ).add_yaxis(
        series_name='acc_high',
        y_axis=acc_high_tho,
        xaxis_index=1,
        yaxis_index=3,
        is_connect_nones=True,
        # stack="stack"
    ).add_yaxis(
        series_name='acc_all',
        y_axis=acc_all_tho,
        xaxis_index=1,
        yaxis_index=3,
        is_connect_nones=True,
        # stack="stack"
    )
    line1.set_global_opts(
        xaxis_opts=opts.AxisOpts(grid_index=1),
        title_opts=opts.TitleOpts(title="line-chart"),
                         toolbox_opts=opts.ToolboxOpts(),
                         legend_opts=opts.LegendOpts(
                             pos_left='right',
                             pos_top='48%',
                             orient='vertical',
                             align='auto',
                         ),
                         datazoom_opts=opts.DataZoomOpts(is_show=True,
                                                         range_start=0,  # 显示区域的开始位置，默认是20
                                                         range_end=80,  # 显示区域的结束位置，默认是80
                                                         orient='horizontal'  ##缩放区域空值条所放的位置
                                                         )

                         ).set_series_opts(
        label_opts=opts.LabelOpts(position='insideRight', color='white', font_size=12, is_show=False))
    pic1 = bar.overlap(line)
    pic2 = bar1.overlap(line1)
    grid = Grid()
    grid.add(pic1, opts.GridOpts(pos_left="5%", pos_right="20%", pos_bottom="60%"), is_control_axis_index=True)
    grid.add(pic2, opts.GridOpts(pos_left="5%", pos_right="20%", pos_top="60%"), is_control_axis_index=True)

    return grid

    # bar1 = (
    #     Bar()
    #     .add_xaxis(Faker.choose())
    #     .add_yaxis("商家A", Faker.values(), stack="stack1")
    #     .add_yaxis("商家B", Faker.values(), stack="stack1")
    #     .set_global_opts(title_opts=opts.TitleOpts(title="Grid-Bar"))
    # )
    # bar2 = (
    #     Bar()
    #     .add_xaxis(Faker.choose())
    #     .add_yaxis("商家C", Faker.values(), stack="stack2")
    #     .add_yaxis("商家D", Faker.values(), stack="stack2")
    #     .set_global_opts(
    #         title_opts=opts.TitleOpts(title="Grid-Line", pos_top="48%"),
    #         legend_opts=opts.LegendOpts(pos_top="48%"),
    #     )
    # )


# 导入要使用的模块
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Liquid, Page, Pie
from pyecharts.commons.utils import JsCode
from pyecharts.components import Table
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType


# 将每个图 封装到 函数

# 1.条形图
def bar_datazoom_slider() -> Bar:
    c1 = (

        Bar(init_opts=opts.InitOpts(theme=ThemeType.MACARONS))
        .add_xaxis(Faker.days_attrs)
        .add_yaxis("商家A", Faker.days_values)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Bar-DataZoom（slider-水平）"),
            datazoom_opts=[opts.DataZoomOpts()],
        )
    )
    return c1


# 2.带标记点的折线图
def line_markpoint() -> Line:
    c2 = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.MACARONS))

        .add_xaxis(Faker.choose())
        .add_yaxis(
            "商家A",
            Faker.values(),
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="min")]),
        )
        .add_yaxis(
            "商家B",
            Faker.values(),
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Line-MarkPoint"))
    )
    return c2


# 3.玫瑰型饼图
def pie_rosetype() -> Pie:
    v = Faker.choose()
    c = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.MACARONS))

        .add(
            "",
            [list(z) for z in zip(v, Faker.values())],
            radius=["30%", "75%"],
            center=["25%", "50%"],
            rosetype="radius",
            label_opts=opts.LabelOpts(is_show=False),
        )

        .add(
            "",
            [list(z) for z in zip(v, Faker.values())],
            radius=["30%", "75%"],
            center=["75%", "50%"],
            rosetype="area",
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Pie-玫瑰图示例"))
    )
    return c





def page_simple_layout():
    # page = Page(layout=Page.SimplePageLayout)  # 简单布局
    # # 将上面定义好的图添加到 page
    # page.add(
    #     bar_datazoom_slider(),
    #     line_markpoint(),
    #     pie_rosetype(),
    # )
    tab = Tab()
    tab.add(bar_datazoom_slider(), 'tab1')
    tab.add(line_markpoint(), 'tab2')
    # tab.add(pie_rosetype(), "pie-example")
    tab.render('./templates/tab.html')
    # return tab


























