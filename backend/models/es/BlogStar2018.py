#! /usr/bin/env python3
# -*- coding:utf-8 -*-
import elasticsearch

class BlogStar2018(object):
    index = 'blogstar2018'
    es = elasticsearch.Elasticsearch(['sc.es.com:80'])

    @classmethod
    def index_doc(cls,body):
        cls.es.index(index=cls.index, doc_type=cls.index, body=body)

    @classmethod
    def match_all(cls):
        body = {
          "query": {
            "match_all": {}
          },
          "size": 1000
        }
        try:
            res = cls.es.search(index=cls.index, doc_type=cls.index, body=body)
        except Exception as e:
            print('查询失败 ', str(e))
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
    def stats_aggs(cls,field):
        body = {
          "size": 0,
          "aggs": {
            "stats_"+field: {
              "stats": {
                "field": field
              }
            }
          }
        }
        try:
            res = cls.es.search(index=cls.index, doc_type=cls.index, body=body)
        except Exception as e:
            print('查询失败 ', str(e))
            res = None
        return res

    @classmethod
    def term_aggs(cls,field,size=10):
        body = {
          "size": 0,
          "aggs": {
            "term_"+field: {
              "terms": {
                "field": field,
                "size": size,
                "order": {
                  "_key": "desc"
                }
              }
            }
          }
        }
        try:
            res = cls.es.search(index=cls.index, doc_type=cls.index, body=body)
        except Exception as e:
            print('查询失败 ', str(e))
            res = None
        return res

    @classmethod
    def term_query(cls,field,value):
        body = {
          "query": {
            "bool": {
              "filter": {
                "term": {
                  field: value
                }
              }
            }
          }
        }

        try:
            res = cls.es.search(index=cls.index, doc_type=cls.index, body=body)
        except Exception as e:
            print('查询失败 ', str(e))
            res = None
        return res

    @classmethod
    def username_term_query(cls,field,value):
        body = {
          "query": {
            "bool": {
              "filter": {
                "term": {
                  field: value
                }
              }
            }
          },
          "_source": ["blogstar_vote.user_name"]
        }

        try:
            res = cls.es.search(index=cls.index, doc_type=cls.index, body=body)
        except Exception as e:
            print('查询失败 ', str(e))
            res = None
        return res

    @classmethod
    def stat_colunm_name(cls):
        body = {
            "aggs": {
                "colunms": {
                    "nested": {
                        "path": "colunms"
                    },
                    "aggs": {
                        "colunm_name": {
                            "terms": {
                                "field": "colunms.colunm_name",
                                "size": 1000
                            }
                        }
                    }
                }
            }
        }
        try:
            res = cls.es.search(index=cls.index, doc_type=cls.index, body=body)
        except Exception as e:
            print('查询失败 ', str(e))
            res = None
        return res