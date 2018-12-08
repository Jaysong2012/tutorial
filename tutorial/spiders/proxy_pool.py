# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import ProxyItem
import execjs
import re
import time


class ProxyPoolSpider(scrapy.Spider):
    name = 'proxy_pool'
    allowed_domains = ['www.iphai.com',
                       'ip.jiangxianli.com',
                       'www.data5u.com',
                       'www.66ip.cn',
                       'www.kuaidaili.com',
                       'www.89ip.cn',
                       'www.ip3366.net']
    start_urls = ['http://www.iphai.com/free/ng',
                  'http://www.data5u.com/free/gngn/index.shtml',
                  'http://ip.jiangxianli.com/',
                  'http://www.66ip.cn/areaindex_{}/{}.html',
                  'https://www.kuaidaili.com/ops/proxylist/{}/',
                  'http://www.89ip.cn/index_{}.html',
                  'http://www.ip3366.net/?stype=1&page={}']

    @staticmethod
    def get_66ip_headers(cookie=None):
        if cookie:
            return {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Host': 'www.66ip.cn',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
                'cookie': 'yd_cookie=10cf4030-46f7-4f68e382359f0e756b4ff69840a8218e262a; Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1544168568; _ydclearance=' +
                          cookie['_ydclearance'] + '; Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=' + str(int(time.time()))
            }
        else:
            return {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Host': 'www.66ip.cn',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
            }

    def start_requests(self):
        for url in self.start_urls:
            if url.find('www.iphai.com') >-1:
                yield scrapy.Request(url ,callback=self.parse_iphai)
                #pass
            elif url.find('www.data5u.com')>-1:
                yield scrapy.Request(url ,callback=self.parse_data5u)
                #pass
            elif url.find('ip.jiangxianli.com')>-1:
                for i in range(3):
                    yield scrapy.Request(url+'?page='+str(i+1), callback=self.parse_jiangxianli)
                #pass
            elif url.find('www.66ip.cn')>-1:
                for area_index in range(1, 12):
                    yield scrapy.Request(url.format(area_index, 1),headers=__class__.get_66ip_headers(),callback=self.parse_66ip_cookie)
                #pass
            elif url.find('www.kuaidaili.com')>-1:
                for list_index in range(1,3):
                    yield scrapy.Request(url.format(list_index), callback=self.parse_kuaidaili)
                #pass
            elif url.find('www.89ip.cn')>-1:
                #for list_index in range(1,3):
                    #yield scrapy.Request(url.format(list_index), callback=self.parse_89ip)
                pass
            elif url.find('www.ip3366.net')>-1:
                for page_index in range(1,3):
                    yield scrapy.Request(url.format(page_index), callback=self.parse_ip3366)
                #pass


    def parse_iphai(self, response):
        for tr in response.xpath('//div[@class="table-responsive module"]/table/tr'):
            td_list = [td.replace(' ', '').replace('\r\n','') for td in tr.xpath('./td/text()').extract()]

            if len(td_list) == 7:
                item = ProxyItem()
                item['ip'] = td_list[0]  # 提取IP
                item['port'] = td_list[1]  # 提取port
                item['type'] = td_list[2]  # 提取type
                item['schemes'] = td_list[3]  # 提取schemes
                item['addr'] = td_list[4]  # 提取addr
                item['speed'] = td_list[5]  # 提取speed
                item['update'] = td_list[6]  # 提取update
                item['ori'] = 'iphai'  # 提取update
                yield item

    def parse_data5u(self, response):
        for i ,ul in enumerate(response.xpath('//div[@class="wlist"]/ul/li[@style="text-align:center;"]/ul')):
            if i !=0:
                ul_list = ul.xpath('./span/li/text()').extract()
                item = ProxyItem()
                item['ip'] = ul_list[0]  # 提取IP
                item['port'] = ul_list[1]  # 提取port
                item['type'] = ul_list[2]  # 提取type
                item['schemes'] = ul_list[3]  # 提取schemes
                item['addr'] = ul_list[5]  # 提取addr
                item['speed'] = ul_list[7]  # 提取speed
                item['update'] = ul_list[8]  # 提取update
                item['ori'] = 'data5u'  # 提取update
                yield item

    def parse_jiangxianli(self, response):
        for tr in response.xpath('//table[@class="table table-hover table-bordered table-striped"]/tbody/tr'):
            td_list = tr.xpath('./td/text()').extract()
            item = ProxyItem()
            item['ip'] = td_list[1]  # 提取IP
            item['port'] = td_list[2]  # 提取port
            item['type'] = td_list[3]  # 提取type
            item['schemes'] = td_list[4]  # 提取schemes
            item['addr'] = td_list[5]  # 提取addr
            item['speed'] = td_list[7]  # 提取speed
            item['update'] = td_list[8]  # 提取update
            item['ori'] = 'jiangxianli'  # 提取update
            yield item

    def parse_66ip_cookie(self,response):
        first_html = response.text
        # 提取其中的JS加密函数名称
        js_fun_name = str(''.join(re.findall('window.onload=setTimeout\("(.*?)", 200\);', first_html))).split('(')[0]
        # 提取其中的JS加密函数
        js_func = ''.join(re.findall(r'(function .*?)</script>', first_html))
        # 提取其中执行JS函数的参数
        js_arg = ''.join(re.findall(r'setTimeout\(\"\D+\((\d+)\)\"', first_html))
        # 修改JS函数，使其返回Cookie内容
        js_func = js_func.replace('eval("qo=eval;qo(po);")', 'return po')
        # 编译js代码
        ctx = execjs.compile(js_func)
        # 执行JS获取Cookie
        cookie_str = ctx.call(js_fun_name, js_arg)

        # 将Cookie转换为字典格式
        cookie = {cookie_str.replace("document.cookie='", "").split(';')[0].split('=')[0]:cookie_str.replace("document.cookie='", "").split(';')[0].split('=')[1]}

        print(cookie)
        yield scrapy.Request(response.request.url, headers=__class__.get_66ip_headers(cookie), callback=self.parse_66ip,dont_filter=True,cookies=cookie)

    def parse_66ip(self, response):
        for i ,tr in enumerate(response.xpath('//div[@class="footer"]/div[@align="center"]/table/tr')):
            if i != 0:
                td_list = tr.xpath('./td/text()').extract()
                item = ProxyItem()
                item['ip'] = td_list[0]  # 提取IP
                item['port'] = td_list[1]  # 提取port
                item['type'] = td_list[3]  # 提取type
                item['addr'] = td_list[2]  # 提取addr
                item['update'] = td_list[4]  # 提取update
                item['ori'] = '66ip'  # 提取update
                yield item

    def parse_kuaidaili(self,response):
        for i, tr in enumerate(response.xpath('//div[@id="freelist"]/table/tbody/tr')):
            td_list = tr.xpath('./td/text()').extract()
            item = ProxyItem()
            item['ip'] = td_list[0]  # 提取IP
            item['port'] = td_list[1]  # 提取port
            item['type'] = td_list[2]  # 提取type
            item['schemes'] = td_list[3]  # 提取schemes
            item['addr'] = td_list[5]  # 提取addr
            item['speed'] = td_list[6]  # 提取speed
            item['update'] = td_list[7]  # 提取update
            item['ori'] = 'kuaidaili'  # 提取update
            yield item

    def parse_89ip(self,response):
        for i, tr in enumerate(response.xpath('//table[@class="layui-table"]/tbody/tr')):
            td_list = [td.replace(' ', '').replace('\n','').replace('\t','').replace('\r','') for td in tr.xpath('./td/text()').extract()]
            item = ProxyItem()
            item['ip'] = td_list[0]  # 提取IP
            item['port'] = td_list[1]  # 提取port
            item['type'] = 'unknow'  # 提取type
            item['addr'] = td_list[2]  # 提取addr
            item['update'] = td_list[4]  # 提取update
            item['ori'] = '89ip'  # 提取update
            yield item

    def parse_ip3366(self,response):
        for i, tr in enumerate(response.xpath('//div[@id="list"]/table/tbody/tr')):
            td_list = tr.xpath('./td/text()').extract()
            item = ProxyItem()
            item['ip'] = td_list[0]  # 提取IP
            item['port'] = td_list[1]  # 提取port
            item['type'] = td_list[2]  # 提取type
            item['schemes'] = td_list[3]  # 提取schemes
            item['addr'] = td_list[5]  # 提取addr
            item['speed'] = td_list[6]  # 提取speed
            item['update'] = td_list[7]  # 提取update
            item['ori'] = 'ip3366'  # 提取update
            yield item