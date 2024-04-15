from pyecharts.charts import Bar
from pyecharts import options as opts

# 准备数据
x_data = ["shirt", "cardign", "chiffon shirt", "pants", "heels", "socks"]
y_data = [5, 20, 36, 10, 75, 90]

# 创建柱状图对象
bar = (
    Bar()
    .add_xaxis(x_data)
    .add_yaxis("商家A", y_data)
    .set_global_opts(title_opts=opts.TitleOpts(title="主标题", subtitle="副标题"))
)

# 渲染图表到 HTML 文件中，保存为当前目录下的 bar.html
bar.render("bar.html")

