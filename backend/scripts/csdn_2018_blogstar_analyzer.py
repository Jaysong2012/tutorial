#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
sys.path.append('../..')
from backend.models.es.CSDN2018BlogStar import CSDN2018BlogStar
import json
import re
from pyecharts import Bar,WordCloud

def hot_key_word_cloud():
    white_hotkey_list = ['分布式','算法','嵌入式','前端','机器学习','公众号','微信公众号','数据库','计算机','人工智能','后端','框架','数据结构','程序','大数据',
                   '程序设计','计算机网络','网络','视觉','数据','图像','小程序','图像分析','操作系统','架构','安卓','微服务','爬虫','设计模式']

    wordcloud = WordCloud(width=1300, height=900)
    name = []
    value = []
    for i,bucket in enumerate(CSDN2018BlogStar.hot_key()['aggregations']['term_comment']['buckets']):
        if re.compile(u'[\u4e00-\u9fa5]').search(bucket['key']) :
            if bucket['key'] in white_hotkey_list:
                name.append(bucket['key'])
                value.append(bucket['doc_count'])
        elif re.findall('[a-zA-Z]+', bucket['key']) :
            if bucket['key'].find('http') == -1 and bucket['key'].find('csdn') == -1 and 'details'!=bucket['key'] and '1&orderby'!=bucket['key']:
                name.append(bucket['key'])
                value.append(bucket['doc_count'])


    wordcloud.add("", name, value, word_size_range=[30, 120])
    wordcloud.render('csdn_blogstar_hotkey.html')

if __name__ == '__main__':

    userName = 'testcs_dn'

    print('报名总人数:',CSDN2018BlogStar.count_doc())
    field_dict = {'original':'原创','fans':'粉丝','star':'喜欢','comment':'评论','level':'等级','visit':'访问','score':'积分','rank':'排名',}
    for field in field_dict.keys():
        rank_res = CSDN2018BlogStar.order_field(field,'asc' if field == 'rank' else 'desc')
        for i,hit in enumerate(rank_res['hits']['hits']):
            #print(hit['_source']['blogstar_comment']['UserName'])
            if hit['_source']['blogstar_comment']['UserName'] == userName:
                print(field_dict[field],'指标排名', i+1)

    # field_stats_dict = {}
    # for field in field_dict.keys():
    #     res = CSDN2018BlogStar.stats_aggs(field)
    #     if res:
    #         field_stats_dict[field] = {
    #             'max': int(res['aggregations']['stats_'+field]['max']),
    #             'min': int(res['aggregations']['stats_'+field]['min']),
    #             'avg': int(res['aggregations']['stats_'+field]['avg']),
    #             'sum': int(res['aggregations']['stats_'+field]['sum'])
    #         }
    # print('指标','|','最大值','|','最小值','|','平均值','|','总计','|','最佳用户列表')
    # print('|:------:|:---------:|:---------:|:---------:|:---------:|:-----------:|')
    # for field in field_dict.keys():
    #     print(field_dict[field],'|',field_stats_dict[field]['max'],'|',field_stats_dict[field]['min'],
    #           '|', field_stats_dict[field]['avg'],'|',field_stats_dict[field]['sum'],
    #           '|',[hit['_source']['blogstar_comment']['UserName'] for hit in CSDN2018BlogStar.username_term_query(field, field_stats_dict[field]['min' if 'rank' == field else 'max'])['hits']['hits']])
    #
    # level_aggs_res = CSDN2018BlogStar.term_aggs('level')
    # print('等级','|','人数')
    # print('------|-----')
    # if level_aggs_res :
    #     for bucket in level_aggs_res['aggregations']['term_level']['buckets']:
    #         print(bucket['key'],'|',bucket['doc_count'])
    #
    # print('勋章','|','人数')
    # print('------|-----')
    # medal_aggs_res = CSDN2018BlogStar.term_aggs('medal')
    # if medal_aggs_res:
    #     for bucket in medal_aggs_res['aggregations']['term_medal']['buckets']:
    #         print(bucket['key'],'|',bucket['doc_count'])
    #
    # year_2018_stats_agg_res = CSDN2018BlogStar.stats_agg_year_2018()
    # if year_2018_stats_agg_res:
    #     print('2018年度写的文章 | 篇')
    #     print('-----------------|------')
    #     print('最大|',int(year_2018_stats_agg_res['aggregations']['stats_year_2018']['max']))
    #     print('最小|',int(year_2018_stats_agg_res['aggregations']['stats_year_2018']['min']))
    #     print('平均|',int(year_2018_stats_agg_res['aggregations']['stats_year_2018']['avg']))
    #     print('总计|',int(year_2018_stats_agg_res['aggregations']['stats_year_2018']['sum']))
    #
    # print('2018年度文章写的最多的数量',int(year_2018_stats_agg_res['aggregations']['stats_year_2018']['max']),
    #       '用户',[bucket['key'] for bucket in year_2018_stats_agg_res['aggregations']['term_username']['buckets'] if bucket['year_2018']['prefix_yesr']['sum_article_num']['value'] == int(year_2018_stats_agg_res['aggregations']['stats_year_2018']['max'])],
    #       '平均每月文章数',int(year_2018_stats_agg_res['aggregations']['stats_year_2018']['max']/12))
    #
    # hot_key_word_cloud()




