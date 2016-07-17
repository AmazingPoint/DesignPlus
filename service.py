# -*- coding: UTF-8 -*-
from redis import Redis
from servicetools import Browser
from threading import Thread
import time
import logging


class Master:
    ''' 爬虫工作管理
        链接redis|维护url列队|存储数据'''
    rdb = None

    def __init__(self):
        '''初始化日志信息和数据库连接'''
        self.initLogging()
        if self.rdb is None:
            self.rdb = Redis(host='localhost', port=6379, db=0)

    def pushTodoList(self, url_list):
        '''写入一批url到待爬取列队'''
        for url in url_list:
            self.rdb.rpush('wait', url)

    def pubTodoList(self):
        '''发布任务（从待爬取列队的拿第一条数据）'''
        url = self.rdb.lrange('wait', 0, 0)
        if len(url) == 0:
            return None
        logging.info('start to do: %s' % url)
        return url[0]

    def popTodoList(self):
        ''' 从待爬取列队pop一条数据
            先进先出'''
        self.rdb.lpop('wait')

    def pushDoneList(self, url):
        ''' 存储爬取过的一条url'''
        self.rdb.lpush('done', url)

    def getDoneList(self):
        '''获取爬取过的所有url'''
        return self.rdb.lrange('done', 0, -1)

    def getWaitList(self):
        '''获取等待爬取的所有url'''
        return self.rdb.lrange('wait', 0, -1)

    def pushData(self, result):
        ''' 写入数据（hset数据结构）
            如果为list，则表示数据为待爬取的url
            如果为dict，则表述数据为想要的信息'''
        if isinstance(result, list):
            self.pushTodoList(result)
        elif isinstance(result, dict):
            for key in result.keys():
                self.rdb.hset(result['title'], key, result[key])
        else:
            logging.debug('#########result error########')

    def finish(self, url):
        ''' 结束任务之后的操作
            对已爬取列队执行push
            日志写入当前爬取数量和待爬数量'''
        self.pushDoneList(url)
        wait_number = self.rdb.llen('wait')
        done_number = self.rdb.llen('done')
        logging.info('end of: %s' % url)
        logging.info('%d waited: %d done' % (wait_number, done_number))

    def initLogging(self):
        '''日志的初始化'''
        logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s %(asctime)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='service_work.log',
                    filemod='w')


class Worker:
    ''' 工作者，使用浏览器进行爬取操作'''
    browser = None
    result = None

    def __init__(self):
        '''初始化工具（browser）'''
        if self.browser is None:
            self.browser = Browser()

    def doJob(self, url):
        ''' 开始执行工作，调试期间可以打印执行秒数
            使用浏览器访问url
            获取数据'''
        start = time.time()
        result = self.browser.queryResult(url)
        self.browser.restart()
        end = time.time()
        print end - start
        return result

    def work(self, master):
        ''' 配合master的工作
            不断从列队读取url并进行实际工作'''
        url = master.pubTodoList()
        while url is not None:
            done_list = master.getDoneList()
            if url in done_list:
                logging.info('this url is done befor work! passed!')
                master.popTodoList()
            else:
                master.popTodoList()
                result = self.doJob(url)
                master.pushData(result)
                master.finish(url)
            url = master.pubTodoList()
        self.browser.quit()
