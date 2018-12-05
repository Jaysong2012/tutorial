#! /usr/bin/env python3
# -*- coding:utf-8 -*-
from backend.libs.Util import Util

class DLDL(object):
    index = 'dldl'

    @classmethod
    def get_hot_keyword(cls):
        es = Util.get_es()
        body = {
            "aggs": {
                "hot_keyword" : {
                    "terms" : {
                        "field" : "content",
                        "size": 500
                    }
                }
            },
            "size": 0
        }

        try:
            res = es.search(index=cls.index, doc_type=cls.index, body=body)
        except Exception as e:
            print('查询失败 ' , str(e))
            res = None
        return res


