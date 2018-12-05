# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import elasticsearch

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
