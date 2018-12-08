#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import elasticsearch
import time
import random


USER_AGENT_LIST=[
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


class Util(object):

    @staticmethod
    def get_es():
        return elasticsearch.Elasticsearch(['192.168.199.133:9200'])

    @staticmethod
    def get_cellid_header(timestamp=int(time.time()), host='www.cellid.cn',ip=None):
        if ip is None:
            ip = str(random.choice(list(range(255)))) + '.' + str(random.choice(list(range(255)))) + '.' + str(
                random.choice(list(range(255)))) + '.' + str(random.choice(list(range(255))))
        return {
            'Host': host,
            'User-Agent': random.choice(USER_AGENT_LIST),
            'server-addr': '',
            'remote_user': '',
            'X-Client-IP': ip,
            'X-Remote-IP': ip,
            'X-Remote-Addr': ip,
            'X-Originating-IP': ip,
            'x-forwarded-for': ip,
            'Origin': 'http:/' + host,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "http://" + host + "/",
            'Content-Length': '0',
            "Connection": "keep-alive",
            'Cookie': 'Hm_lvt_6e76d1bd846f1ef996da8b905e7c5b09=1542787567; Hm_lpvt_6e76d1bd846f1ef996da8b905e7c5b09=' + str(
                timestamp)
        }

    @staticmethod
    def get_header(host='www.baidu.com',ip=None):
        if ip is None:
            ip = str(random.choice(list(range(255)))) + '.' + str(random.choice(list(range(255)))) + '.' + str(
                random.choice(list(range(255)))) + '.' + str(random.choice(list(range(255))))
        return {
            'Host': host,
            'User-Agent': random.choice(USER_AGENT_LIST),
            'server-addr': '',
            'remote_user': '',
            'X-Client-IP': ip,
            'X-Remote-IP': ip,
            'X-Remote-Addr': ip,
            'X-Originating-IP': ip,
            'x-forwarded-for': ip,
            'Origin': 'http:/' + host,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "http://" + host + "/",
            'Content-Length': '0',
            "Connection": "keep-alive"
        }

    @staticmethod
    def get_header_list(host='www.baidu.com',ip=None):
        if ip is None:
            ip = str(random.choice(list(range(255)))) + '.' + str(random.choice(list(range(255)))) + '.' + str(
                random.choice(list(range(255)))) + '.' + str(random.choice(list(range(255))))
        return [
            {'Host': host},
            {'User-Agent': random.choice(USER_AGENT_LIST)},
            {'server-addr': ''},
            {'remote_user': ''},
            {'X-Client-IP': ip},
            {'X-Remote-IP': ip},
            {'X-Remote-Addr': ip},
            {'X-Originating-IP': ip},
            {'x-forwarded-for': ip},
            {'Origin': 'http:/' + host},
            {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
            {"Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.5,en;q=0.3"},
            {"Accept-Encoding": "gzip, deflate"},
            {"Referer": "http://" + host + "/"},
            {'Content-Length': '0'},
            {"Connection": "keep-alive"},
        ]

    @staticmethod
    def record_proxy(content):
        with open('proxy_pool.txt','a+') as f:
            f.write(content)

