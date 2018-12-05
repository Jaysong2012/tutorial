#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import elasticsearch
class Util(object):

    @staticmethod
    def get_es():
        return elasticsearch.Elasticsearch(['192.168.199.133:9200'])