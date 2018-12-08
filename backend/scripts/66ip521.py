#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import requests
import execjs
import time

TARGET_URL = "http://www.66ip.cn/areaindex_1/1.html"

def get_header(cookie = None):
    if cookie:
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.66ip.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
            'cookie':'yd_cookie=10cf4030-46f7-4f68e382359f0e756b4ff69840a8218e262a; Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1544168568; _ydclearance='+cookie['_ydclearance']+'; Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4='+str(int(time.time()))
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
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
        }

#
def parseCookie(string):
    string = string.replace("document.cookie='", "")
    clearance = string.split(';')[0]
    return {clearance.split('=')[0]: clearance.split('=')[1]}


if __name__ == '__main__':
    # 第一次访问获取动态加密的JS
    first_response = requests.get(url=TARGET_URL, headers=get_header(), timeout=30)
    print(first_response.status_code)
    first_html = str(first_response.content)

    # 提取其中的JS加密函数名称
    js_fun_name = str(''.join(re.findall('window.onload=setTimeout\("(.*?)", 200\);', first_html))).split('(')[0]

    # 提取其中的JS加密函数
    js_func = ''.join(re.findall(r'(function .*?)</script>', first_html))

    # 提取其中执行JS函数的参数
    js_arg = ''.join(re.findall(r'setTimeout\(\"\D+\((\d+)\)\"', first_html))

    # 修改JS函数，使其返回Cookie内容
    js_func = js_func.replace('eval("qo=eval;qo(po);")', 'return po')

    #编译js代码
    ctx = execjs.compile(js_func)
    # 执行JS获取Cookie
    cookie_str =ctx.call(js_fun_name, js_arg)

    print(cookie_str)

    # 将Cookie转换为字典格式
    cookie = parseCookie(cookie_str)

    # 带上Cookie再次访问url,获取正确数据
    resp = requests.get(url=TARGET_URL, headers=get_header(cookie), timeout=30)
    print(resp.status_code)