# Date：2018-06-07
# Author：财报妹 https://weibo.com/marsfactory
# Description：2018 年第 1 季度各省离结率
#

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from operator import itemgetter
from collections import OrderedDict
import os
import json


def get_data():
    os.chdir(os.getcwd())
    url = r'http://www.mca.gov.cn/article/sj/tjjb/sjsj/2018/201806041612.html'  # 民政部公布的 2018 年第 1 季度数据
    tables = pd.read_html(url)
    data = tables[0]
    all_provinces = {}
    for i in range(9, 40):
        province = data[0][i]
        province_marry = data[42][3]
        province_divorce = data[44][3]
        province_data = {}
        province_data[province_marry] = int(data[48][i])
        province_data[province_divorce] = int(data[50][i])
        province_dmr = '离结率'  # 离结率 = 离婚对数/结婚对数
        province_data[province_dmr] = "{:.2%}".format(data[50][i] / data[48][i])
        all_provinces[province] = province_data

    fp = open('data.json','w', encoding='utf-8')
    fp.write(json.dumps(all_provinces, ensure_ascii=False, indent=4)) # 把所有数据写入到 data.json
    fp.close()
    return all_provinces


def plot_plot():
    os.chdir(os.getcwd())
    zhfont = matplotlib.font_manager.FontProperties(fname='Hiragino Sans GB W3.ttf')
    all_provinces = get_data()
    provinces = []
    married_number = []
    divorced_number = []
    province_dmr = []
    province_dmr_dict = {}
    for item in all_provinces:
        provinces.append(item)
        married_number.append(all_provinces[item]['结婚登记'])
        divorced_number.append(all_provinces[item]['离婚登记'])
        province_dmr.append(all_provinces[item]['离婚登记'] / all_provinces[item]['结婚登记'])
        province_dmr_dict[item] = all_provinces[item]['离婚登记'] / all_provinces[item]['结婚登记']

    sorted_x = OrderedDict(sorted(province_dmr_dict.items(), key=itemgetter(1)))  # reverse=True 就逆序啦
    D = dict(sorted_x)
    provinces_sorted = []
    province_dmr_sorted = []
    for item in D:
        provinces_sorted.append(item)
        province_dmr_sorted.append(D[item])

    provinces = provinces_sorted
    provinces_dmr = province_dmr_sorted
    fig, ax = plt.subplots(figsize=(10, 20), dpi=300)
    b = ax.barh(range(len(provinces)), provinces_dmr, color='crimson')
    for rect in b:
        w = rect.get_width()
        ax.text(w, rect.get_y() + rect.get_height() / 2, "{:.2%}".format(w), ha='left', va='center')
    ax.set_yticks(range(len(provinces)))
    ax.set_yticklabels(provinces, fontproperties=zhfont)
    plt.savefig("2018 年第 1 季度各省离结率.jpg") # 将图片保存
    plt.title(r'2018 年第 1 季度各省离结率', fontproperties=zhfont)


if __name__ == "__main__":
    print(os.getcwd())
    os.chdir(os.getcwd())
    plot_plot()
    print('Well done! 太棒了')
