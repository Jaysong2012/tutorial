# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import re

from tutorial.items import BaiDuSearchItem


class BaiduSplashSpider(scrapy.Spider):
    name = 'baidu_splash'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/s?wd=elasticsearch%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0%20%E7%81%B5%E5%8A%A8%E7%9A%84%E8%89%BA%E6%9C%AF']

    def start_requests(self):
        for url in self.start_urls:
            # 通过SplashRequest请求等待1秒
            yield SplashRequest(url, self.parse, args={'wait': 1})

    def parse(self, response):

        #print(response.text)
        head_scripts = response.xpath('//head/div/script[@id="head_script"]')
        print(head_scripts)

        # for a in response.xpath('//div[@id="wrapper_wrapper"]'):
        #     print(a.xpath('./script[@id="head_script"]/text()').extract())

        head_script = response.xpath('//div[@id="wrapper_wrapper"]/script[@id="head_script"]/text()').extract()
        #result = re.findall(".*bds.comm.eqid = \"(.+?)\";.*", str(head_script))

        eqid = str(re.findall(r"bds.comm.eqid = \"(.+?)\";", str(head_script))[0])

        print(eqid)

        for head_script in head_scripts:
            print(head_script.xpath('./text()').extract())
        # for a in response.xpath('//div[@class="result c-container "]/h3/a'):
        #     print(type(a))
        #     ems = a.xpath('./em/text()')
        #     for em in ems:
        #         if em.extract().find('') > -1:
        #             item = BaiDuSearchItem()
        #             item['visit_url'] = a.xpath('@href').extract()  # 提取链接
        #             yield item
