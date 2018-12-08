#! /usr/bin/env python3
# -*- coding:utf-8 -*-
import requests
import sys
import redis
import time
sys.path.append('../..')
from backend.libs.Util import Util

def speed_test(line):
    ip = line.split(':')[0]
    headers = Util.get_header('2018.ip138.com',ip=ip)
    proxies = {"http": "http://{}".format(line.replace('\n',''))}
    try:
        resp = requests.get('http://2018.ip138.com/ic.asp',headers=headers,proxies=proxies,timeout=1)
        if resp.status_code == 200 and resp.text.find(ip)>-1:
            return True
    except Exception as e:
        print(e)
        return False

r = redis.Redis(host='127.0.0.1', port=6379)

def save_redis_set(line=None):
    line = '383 36.110.234.244:80'
    today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    key = 'proxypool'+'_'+today+'_'+'key'
    print(key)
    r.sadd(key,line)
    r.expire(key, 2)
    print(r.smembers(key))

    time.sleep(3)
    print(r.smembers(key))



if __name__ == '__main__':

    # can_user_num = 0
    # with open('../../proxy_pool.txt','r') as f:
    #     lines = f.readlines()
    #
    # for i,line in enumerate(lines):
    #     print(i,line)
    #     if speed_test(line):
    #         can_user_num +=1
    # print('total :',len(lines),' can_user_num :',can_user_num)
    save_redis_set()

