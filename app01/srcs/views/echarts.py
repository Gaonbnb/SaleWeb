from django.shortcuts import render
from pyecharts import options as opts
from pyecharts.charts import Bar

def bar_chart(req):
    # 使用pyecharts生成图表
    x_data = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    y_data = [820, 932, 901, 934, 1290, 1330, 1320]
    c = (
        Bar()
        .add_xaxis(x_data)
        .add_yaxis("sales", y_data)
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar Chart"))
    )
    # 将图表数据传递给前端页面
    chart_data = c.dump_options_with_quotes()
    
    return render(req, 'echart.html', {'chart_options': chart_data})