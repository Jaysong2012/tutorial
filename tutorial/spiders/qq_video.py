# -*- coding: utf-8 -*-
import scrapy
import json

from scrapy import Request
from tutorial.items import QQVideoCommentItem


class QqVideoSpider(scrapy.Spider):
    name = 'qq_video'
    allowed_domains = ['v.qq.com','coral.qq.com']
    start_urls = ['http://coral.qq.com/article/1641090003/comment?commentid={}&reqnum={}']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0].format(0,10), callback=self.parse)

    def parse(self, response):
        dict_rsp = json.loads(response.text)
        if 0 != dict_rsp.get('errCode',-1):
            return

        for comment in dict_rsp['data']['commentid']:
            item = QQVideoCommentItem()
            item['comment'] = comment  # 提取评论
            yield item

        #加载更多
        if dict_rsp['data']['hasnext']:
            yield Request(self.start_urls[0].format(dict_rsp['data']['last'],20), self.parse)

