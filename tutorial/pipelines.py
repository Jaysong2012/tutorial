# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import elasticsearch
from backend.libs.Util import Util
from backend.models.es.CSDN2018BlogStar import CSDN2018BlogStar

def get_es():
    return elasticsearch.Elasticsearch(['192.168.199.133:9200'])

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

class BaiDuSearchPipeline(object):
    def process_item(self, item, spider):
        print('BaiDuSearchPipeline',item)
        return item

class QQVideoCommentPipeline(object):
    count = 0
    index = 'dldl'
    def process_item(self, item, spider):
        print(json.dumps(item['comment']))
        get_es().index(index=__class__.index,doc_type=__class__.index,body=item['comment'])
        __class__.count += 1
        print(__class__.count)
        return item

class ProxyPipeline(object):
    def process_item(self, item, spider):
        if item['type'].find('高匿') > -1:
            Util.record_proxy(item['ip']+':'+item['port']+'\n')
        return item

class CSDN2018BlogStarPipeline(object):
    count = 0
    def process_item(self, item, spider):
        CSDN2018BlogStar.index_doc(json.dumps(dict(item), ensure_ascii=False))
        __class__.count += 1
        print(__class__.count)
        return item
