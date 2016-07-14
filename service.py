# -*- coding: UTF-8 -*-

from redis import Redis
from servicetools import SOURCE_HTML, Browser
from threading import Thread
import time


class Master:
    rdb = None

    def __init__(self):
        if self.rdb is None:
            self.rdb = Redis(host='localhost', port=6379, db=0)
        if self.rdb.dbsize() == 0:
            self.pushTodoList(SOURCE_HTML)
            #self.pushTodoList(SOURCE_PPT)

    def pushTodoList(self, url_list):
        for url in url_list:
            self.rdb.rpush('wait', url)

    def pubTodoList(self):
        url = self.rdb.lrange('wait', 0, 0)
        if len(url) == 0:
            return None
        return url[0]

    def popTodoList(self):
        self.rdb.lpop('wait')

    def pushDoneList(self, url):
        self.rdb.rpush('done', url)

    def getDoneList(self):
        return self.rdb.lrange('done', 0, -1)

    def pushData(self, result):
        print type(result)
        if isinstance(result, list):
            self.pushTodoList(result)
        if isinstance(result, dict):
            for key in result.keys():
                self.rdb.hset(result['title'], key, result[key])
        else:
            pass

    def finish(self, url):
            self.popTodoList()
            self.pushDoneList(url)

    def showProgress(self):
        print ('wait : %d --- done : %d') %\
            (self.rdb.llen('wait'), \
            self.rdb.llen('done'))
    
        

class Worker:

    browser = None
    result = None

    def __init__(self):
        if self.browser is None:
            self.browser = Browser()

    def doJob(self, url):
        result = self.browser.queryResult(url)
        return result
    
    def restartJob(self, url):
        self.browser.restart()
        self.doJob()



def work(master):
    url = master.pubTodoList()
    while url is not None:
        master.showProgress()
        done_list = master.getDoneList()
        if url in done_list:
            print url + ' repeat! breaked!'
            master.popTodoList()
        else:
            result = worker.doJob(url)
            master.pushData(result)
            master.finish(url)
        url = master.pubTodoList()
        lissen_url = url


def workLissener(master, worker):
    count = 0
    while True:
        time.sleep(10)
        if lissen_url == master.pubTodoList():
            count = count + 1
        if count == 2:
            print '该地指已经尝试%d次，怀疑线程假死，现在重启：' % count
            woker.restart()
            count = 0 
            

if __name__ == '__main__':
    master = Master()
    lissen_url = None
    worker = Worker()
    lissener = Thread(target=workLissener, args=(master, worker,))
    lissener.start()
    work(master)
