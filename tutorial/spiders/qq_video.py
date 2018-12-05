# -*- coding: utf-8 -*-
import scrapy
import json

from scrapy import Request
from tutorial.items import QQVideoCommentItem


class QqVideoSpider(scrapy.Spider):
    name = 'qq_video'
    allowed_domains = ['v.qq.com','coral.qq.com']
    start_urls = ['http://coral.qq.com/article/1641090003/comment']
    base_url = start_urls[0]

    def parse(self, response):
        dict_rsp = json.loads(response.text)
        if 0 != dict_rsp.get('errCode',-1):
            return
        first_comment_id = dict_rsp['data']['first']
        last_comment_id = dict_rsp['data']['last']

        total_comment_num = dict_rsp['data']['total']

        yield Request(self.base_url+'?commentid='+first_comment_id+'&reqnum=50', self.parse_next)


    def parse_next(self, response):
        dict_rsp = json.loads(response.text)
        if 0 != dict_rsp.get('errCode',-1):
            return

        for comment in dict_rsp['data']['commentid']:
            item = QQVideoCommentItem()
            item['comment'] = comment  # 提取评论
            yield item

        #最后一条了
        if not dict_rsp['data']['hasnext']:
            return
        else:
            print(dict_rsp['data']['first'])
            yield Request(self.base_url+'?commentid='+dict_rsp['data']['first']+'&reqnum=50', self.parse_next)
