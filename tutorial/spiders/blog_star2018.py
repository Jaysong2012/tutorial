# -*- coding: utf-8 -*-
import scrapy
import json
from tutorial.items import BlogStar2018Item


class BlogStar2018Spider(scrapy.Spider):
    name = 'blog_star2018'
    allowed_domains = ['blog.csdn.net']
    start_urls = ['https://bss.csdn.net/m/topic/blog_star2018']

    def parse(self, response):
        for user_info in response.xpath('//div[@class="user-info"]'):
            info = {}
            user_id = user_info.xpath('./div[@class="user-id"]/text()').extract_first()
            user_addr = user_info.xpath('./div[@class="avatar"]/a/@href').extract_first()
            user_name  = user_info.xpath('./div[@class="user-name"]/span/text()').extract_first()
            user_number = user_info.xpath('./div[@class="user-number"]/span/em/text()').extract_first()
            print(user_id,user_addr,user_name,user_number)
            info['user_id'] = user_id
            info['user_addr'] = user_addr
            info['user_name'] = user_name
            info['user_number'] = user_number
            yield scrapy.Request(user_addr,
                                 callback=lambda response, info=info: self.parse_blog_user_info(response,info))

    def parse_blog_user_info(self,response,info):
        item = BlogStar2018Item()
        item['link'] = response.request.url
        item['blogstar_vote'] = info
        item['blog_title'] = response.xpath('//div[@class="title-box"]/h1[@class="title-blog"]/a/text()').extract_first()
        item['description'] = response.xpath('//p[@class="description"]/text()').extract_first()
        item['avatar_pic'] = response.xpath('//div[@class="profile-intro d-flex"]/div[@class="avatar-box d-flex justify-content-center flex-column"]/a/img/@src').extract_first()

        for data in response.xpath('//div[@class="data-info d-flex item-tiling"]/dl[@class="text-center"]'):
            data_key = data.xpath('./dt/a/text() | ./dt/text()').extract_first()
            data_value = data.xpath('./@title').extract_first()
            if data_key.find('原创') > -1:
                item['original'] = int(data_value)
            elif data_key.find('粉丝') > -1:
                item['fans'] = int(data_value)
            elif data_key.find('喜欢') > -1:
                item['star'] = int(data_value)
            elif data_key.find('评论') > -1:
                item['comment'] = int(data_value)
        for grade in response.xpath('//div[@class="grade-box clearfix"]/dl'):
            grade_key = grade.xpath('./dt/text()').extract_first()
            grade_value = grade.xpath('./dd/@title | ./dd/a/@title | ./@title').extract_first()
            if grade_key.find('等级') > -1:
                item['level'] = int(grade_value.replace('级,点击查看等级说明',''))
            elif grade_key.find('访问') > -1:
                item['visit'] = int(grade_value)
            elif grade_key.find('积分') > -1:
                item['score'] = int(grade_value)
            elif grade_key.find('排名') > -1:
                item['rank'] = int(grade_value)

        #勋章
        item['medal'] = response.xpath('//div[@class="badge-box d-flex"]/div[@class="icon-badge"]/@title').extract()

        blog_expert = ''.join(response.xpath('//div[@class="user-info d-flex justify-content-center flex-column"]/p[@class="flag expert"]/text()').extract()).replace('\n','').replace(' ','')
        if blog_expert and '' is not blog_expert :
            item['medal'].append(blog_expert)

        #博主专栏
        colunms = []
        for li in response.xpath('//div[@id="asideColumn"]/div[@class="aside-content"]/ul/li'):
            colunms.append({'colunm_name':li.xpath('./div[@class="info"]/p/a/text()').extract_first()
                               ,
                            'colunm_count': li.xpath('./div[@class="info"]/div[@class="data"]/span/text()').extract_first().replace(' ', '').replace('篇',
                                                                                                                 '')
                               ,
                            'colunm_read': li.xpath('./div[@class="info"]/div[@class="data"]/span/text()').extract()[-1].replace(' ', '')})

        item['colunms'] = colunms
        yield item