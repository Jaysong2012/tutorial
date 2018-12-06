# -*- coding: utf-8 -*-
import scrapy

class Ip138Spider(scrapy.Spider):
    name = 'ip138'
    allowed_domains = ['www.ip138.com','2018.ip138.com']
    start_urls = ['http://2018.ip138.com/ic.asp']

    # custom_settings = {
    #     'DEFAULT_REQUEST_HEADERS' : {
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #         "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.5,en;q=0.3",
    #         "Accept-Encoding": "gzip, deflate",
    #         'Content-Length': '0',
    #         "Connection": "keep-alive"
    #     }
    # }

    # headers = {
    #     'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #     "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.5,en;q=0.3",
    #     "Accept-Encoding": "gzip, deflate",
    #     'Content-Length': '0',
    #     "Connection": "keep-alive"
    # }
    #
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={'proxy':'http://116.62.134.173:9999'} ,callback=self.parse)

    def parse(self, response):
        print("*" * 40)
        print("response text: %s" % response.text)
        print("response headers: %s" % response.headers)
        print("response meta: %s" % response.meta)
        print("request headers: %s" % response.request.headers)
        print("request cookies: %s" % response.request.cookies)
        print("request meta: %s" % response.request.meta)

