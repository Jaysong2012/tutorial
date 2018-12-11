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

def redis_save():
    r = redis.Redis(host='127.0.0.1', port=6379)
    key = 'proxypool' + '_' + time.strftime("%Y-%m-%d", time.localtime(time.time())) + '_' + 'key'

    can_user_num = 0
    with open('../../proxy_pool.txt','r') as f:
        lines = f.readlines()

    for i,line in enumerate(lines):
        print(i,line)
        if speed_test(line):
            can_user_num +=1
            r.sadd(key, line.replace('\n',''))

    print('total :',len(lines),' can_user_num :',can_user_num)

    r.expire(key, 7*24*60*60)
    print(r.smembers(key))

def print_useful():
    can_use_proxies = []
    can_user_num = 0
    with open('../../proxy_pool.txt', 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        line = line.replace('\n','')
        print(i, line)
        if speed_test(line):
            can_user_num += 1
            if line not in can_use_proxies:
                can_use_proxies.append(line)

    print(can_use_proxies)

    print('total :',len(lines),' can_user_num :',can_user_num)


if __name__ == '__main__':
    print_useful()

