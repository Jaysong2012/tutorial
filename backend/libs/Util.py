#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import elasticsearch
import time
import random
from tutorial.settings import USER_AGENT_LIST

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

