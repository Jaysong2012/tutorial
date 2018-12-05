#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
sys.path.append('../..')
from backend.models.es.DLDL import DLDL

from pyecharts import Bar, Grid ,Timeline,WordCloud

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

if __name__ == '__main__':
    buckets = DLDL.get_hot_keyword()['aggregations']['hot_keyword']['buckets']
    # timeline = Timeline(is_auto_play=True, timeline_bottom=0)
    # for i in list(range(len(buckets)))[::10]:
    #     timeline.add(range_bar(buckets,i,i+9),str(i)+'~'+str(i+9)+"热词")
    # timeline.render()
    # word_cloud(buckets,'top100.html',100)
    # word_cloud(buckets, 'top200.html', 200)
    total_render(buckets)








