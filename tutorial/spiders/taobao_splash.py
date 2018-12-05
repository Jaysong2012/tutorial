# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class TaobaoSplashSpider(scrapy.Spider):
    name = 'taobao_splash'
    allowed_domains = ['www.taobao.com']
    start_urls = ['https://s.taobao.com/search?q=iphone']

    def start_requests(self):
        for url in self.start_urls:
            # 通过SplashRequest请求等待1秒
            yield SplashRequest(url, self.parse, args={'wait': 2})

    def parse(self, response):
        titele = response.xpath('//div[@class="row row-2 title"]/a/text()').extract()
        print('这是标题：', titele)
