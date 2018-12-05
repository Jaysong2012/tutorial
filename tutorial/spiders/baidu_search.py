# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import BaiDuSearchItem

class BaiduSearchSpider(scrapy.Spider):
    name = 'baidu_search'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/s?wd=灵动的艺术']

    def parse(self, response):
        # 拿到当前页码
        current_page = int(response.xpath('//div[@id="page"]/strong/span[@class="pc"]/text()').extract_first())

        #当前页面查找内容
        for i,a in enumerate(response.xpath('//div[@class="result c-container "]/h3/a')):
            #拿到标题文本
            title = ''.join(a.xpath('./em/text() | ./text()').extract())
            # 精确找到自己
            if title.find('灵动的艺术的博客') > -1:
                item = BaiDuSearchItem()
                item['visit_url'] = a.xpath('@href').extract()  # 提取链接
                item['page'] = current_page
                item['rank'] = i+1
                item['title'] = title
                yield item

        #依次访问百度下面的更多页面，再次分别查找
        for p in response.xpath('//div[@id="page"]/a'):
            p_url = 'http://www.baidu.com' + str(p.xpath('./@href').extract_first())
            yield scrapy.Request(p_url, callback=self.parse_other_page)

    def parse_other_page(self, response):
        #拿到当前页码
        current_page = int(response.xpath('//div[@id="page"]/strong/span[@class="pc"]/text()').extract_first())

        #当前页面查找内容
        for i,a in enumerate(response.xpath('//div[@class="result c-container "]/h3/a')):
            # 拿到标题文本
            title = ''.join(a.xpath('./em/text() | ./text()').extract())
            # 精确找到自己
            if title.find('灵动的艺术的博客') > -1:
                item = BaiDuSearchItem()
                item['visit_url'] = a.xpath('@href').extract()  # 提取链接
                item['page'] = current_page
                item['rank'] = i+1
                item['title'] = title
                yield item




