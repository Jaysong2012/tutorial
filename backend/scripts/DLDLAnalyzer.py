#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
sys.path.append('../..')
from backend.models.es.DLDL import DLDL

from pyecharts import Bar, Grid ,Timeline,WordCloud,Pie,Map

white_key_word_list = ['我','你','的','了',]

def total_render(buckets):
    grid = Grid(width=1300, height=900)
    bar = Bar("斗罗大陆热词分析", "热词柱形图")
    key_list = []
    count_list = []
    keyword_count = 1;
    for bucket in buckets:
        if bucket['key'] in white_key_word_list :
            continue
        keyword_count +=1
        if keyword_count <=100:
            key_list.append(bucket['key'])
            count_list.append(bucket['doc_count'])

    bar.add('热词', key_list, count_list, is_datazoom_show=True, xaxis_interval=0, xaxis_rotate=30)
    # 把 bar 加入到 grid 中，并适当调整 grid_bottom 参数，使 bar 图整体上移
    grid.add(bar, grid_bottom="25%")
    # 生成本地 HTML 文件
    grid.render(path='render.html')

def top_20_key_word_render(buckets):
    bar = Bar("斗罗大陆热词分析", "热词柱形图")
    key_list = []
    count_list = []
    keyword_count = 1;
    for bucket in buckets:
        if bucket['key'] in white_key_word_list or len(bucket['key']) == 1:
            continue

        keyword_count +=1
        if keyword_count <=20:
            key_list.append(bucket['key'])
            count_list.append(bucket['doc_count'])

    bar.add('热词', key_list, count_list)
    bar.render(path='top10.html')

def range_bar(buckets,start,stop):
    bar = Bar("斗罗大陆热词分析", str(start)+'~'+str(stop)+"热词")
    key_list = []
    count_list = []
    for i ,bucket in enumerate(buckets):
        if i in range(start,stop) :
            key_list.append(bucket['key'])
            count_list.append(bucket['doc_count'])

    bar.add(str(start)+'~'+str(stop)+"热词", key_list, count_list)
    return bar

def word_cloud(buckets,path,top_keyword):
    wordcloud = WordCloud(width=1300, height=900)
    name = []
    value = []
    for i,bucket in enumerate(buckets):
        if bucket['key'] in white_key_word_list or i >top_keyword:
            continue
        name.append(bucket['key'])
        value.append(bucket['doc_count'])

    wordcloud.add("", name, value, word_size_range=[30, 120])
    wordcloud.render(path)

def gender_map():
    print('gender | 人数')
    print('------|-----')
    for bucket in DLDL.gender_aggs()['aggregations']['terms_gender']['buckets']:
        print(bucket['key'], '|', bucket['doc_count'])

    attr = ["男", "女",]
    v1 = [133,27]
    pie = Pie("性别分布")
    pie.add("", attr, v1, is_label_show=True)
    pie.render()

def up_5_comment_keyword():
    print('评论总数目',DLDL.count_doc())
    print('点赞 | 评论')
    print('------|-----')
    for hit in DLDL.up_5_comment()['hits']['hits']:
        print(hit['_source']['up'],'|',hit['_source']['content'])

    word_cloud(DLDL.up_5_comment_hot_keyword()['aggregations']['hot_keyword']['buckets'], 'up_5_cmt_100_word.html', 100)

def city_map():
    city_list = []
    count_list = []
    china_city_list = []
    with open('/data/code/python/venv/venv_Scrapy/tutorial/1.txt') as f:
        lines = f.readlines()

    for line in lines:
        china_city_list.append(line.replace('省','').replace('\n','').replace('特别行政区',''))

    china_city_list.append('内蒙古')
    china_city_list.append('广西')
    china_city_list.append('西藏')
    china_city_list.append('宁夏')
    china_city_list.append('新疆')

    print(china_city_list)

    for bucket in DLDL.region_agg()['aggregations']['terms_region']['buckets']:
        if bucket['key'] in china_city_list:
            city_list.append(bucket['key'])
            count_list.append(int(bucket['doc_count']))

    # pie = Pie("", width=1200, height=600)
    # pie.add("", city_list, count_list, is_label_show=True)
    # pie.render()

    map = Map("评论观众VisualMap ", width=1200, height=600)
    map.add(
        "",
        city_list,
        count_list,
        maptype="china",
        is_visualmap=True,
        visual_text_color="#000",
    )
    map.render()

if __name__ == '__main__':
    word_cloud(DLDL.get_hot_keyword()['aggregations']['hot_keyword']['buckets'],'top100.html',100)
    #up_5_comment_keyword()
    #word_cloud(DLDL.get_hot_keyword()['aggregations']['hot_keyword']['buckets'], 'top200.html', 200)
    #total_render(buckets)

    #gender_map()

    #city_map()









