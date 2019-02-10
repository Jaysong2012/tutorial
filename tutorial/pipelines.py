# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import elasticsearch
from backend.libs.Util import Util
from backend.models.es.CSDN2018BlogStar import CSDN2018BlogStar
from backend.models.es.BlogStar2018 import BlogStar2018
from backend.models.es.DLDL import DLDL


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

class BaiDuSearchPipeline(object):
    def process_item(self, item, spider):
        print('BaiDuSearchPipeline',item)
        return item

class QQVideoCommentPipeline(object):
    count = 0
    def process_item(self, item, spider):
        print(json.dumps(item['comment']))
        item['comment']['up'] = int(item['comment']['up'])
        DLDL.index_doc(item['comment'])
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

class BlogStar2018Pipeline(object):
    def process_item(self, item, spider):
        BlogStar2018.index_doc(json.dumps(dict(item), ensure_ascii=False))
        return item
