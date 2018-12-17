#! /usr/bin/env python3
# -*- coding:utf-8 -*-
from backend.libs.Util import Util

class DLDL(object):
    index = 'dldl'
    es = Util.get_es()

    @classmethod
    def get_hot_keyword(cls):
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
            res = cls.es.search(index=cls.index, doc_type=cls.index, body=body)
        except Exception as e:
            print('查询失败 ' , str(e))
            res = None
        return res

    @classmethod
    def index_doc(cls,body):
        cls.es.index(index=cls.index, doc_type=cls.index, body=body)

    @classmethod
    def up_5_comment(cls):
        body = {
            "query": {
                "bool": {
                    "filter": {
                        "range": {
                            "up": {
                                "gte": 5
                            }
                        }
                    }
                }
            },
            "size": 100,
            "sort": [
                {
                    "up": {
                        "order": "desc"
                    }
                }
            ]
        }

        try:
            res = cls.es.search(index=cls.index, doc_type=cls.index, body=body)
        except Exception as e:
            print('查询失败 ' , str(e))
            res = None
        return res

    @classmethod
    def count_doc(cls):
        try:
            res = cls.es.count(index=cls.index, doc_type=cls.index,)
        except Exception as e:
            print('查询失败 ', str(e))
            return 0
        return res['count']

    @classmethod
    def up_5_comment_hot_keyword(cls):
        body = {
          "query": {
            "bool": {
              "filter": {
                "range": {
                  "up": {
                    "gte": 5
                  }
                }
              }
            }
          },
          "size": 0,
          "aggs": {
            "hot_keyword" : {
              "terms" : {
                "field" : "content",
                "size": 100
              }
            }
          }
        }
        try:
            res = cls.es.search(index=cls.index, doc_type=cls.index, body=body)
        except Exception as e:
            print('查询失败 ' , str(e))
            res = None
        return res

    @classmethod
    def gender_aggs(cls):
        body = {
            "size": 0,
            "aggs": {
                "terms_gender": {
                    "terms": {
                        "field": "userinfo.gender",
                        "size": 10
                    }
                }
            }
        }

        try:
            res = cls.es.search(index=cls.index, doc_type=cls.index, body=body)
        except Exception as e:
            print('查询失败 ' , str(e))
            res = None
        return res


    @classmethod
    def region_agg(cls):
        body = {
            "size": 0,
            "aggs": {
                "terms_region": {
                    "terms": {
                        "field": "userinfo.region",
                        "size": 1000
                    }
                }
            }
        }

        try:
            res = cls.es.search(index=cls.index, doc_type=cls.index, body=body)
        except Exception as e:
            print('查询失败 ' , str(e))
            res = None
        return res


