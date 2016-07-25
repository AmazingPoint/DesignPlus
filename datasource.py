# -*- coding: UTF-8 -*-
from redis import Redis
import random

rdb = Redis(host='127.0.0.1', port=6379, db=0)


def aPage(page, pre_number_page):
    ''' 从redis获取一个页面的信息
        参数page 页数
        参数page_number_page 每页数据数量'''
    end = page * pre_number_page
    start = end - pre_number_page
    keys = rdb.keys()[start:end]
    datas = []
    for key in keys:
        if key == 'wait' or key == 'done':
            pass
        else:
            data = rdb.hgetall(key)
            datas.append(data)
    return datas


def aRandom():
    '''从redis随机获取一个元素'''
    lenth = rdb.dbsize()
    keys = rdb.keys()
    index = random.randint(3,lenth-1)
    key = keys[index]
    data = rdb.hgetall(key)
    return data
