# -*- coding: UTF-8 -*-
from redis import Redis


rdb = Redis(host='127.0.0.1', port=6379, db=0)
    
    
def aPage(page, pre_number_page):

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
