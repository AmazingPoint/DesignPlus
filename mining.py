# -*- coding: UTF-8 -*-

from service import Master, Worker


def addTodo(master):
    ''' 随时都会改动的代码
        加入一批url'''
    urllist = []
    wait_url = master.getWaitList()
    for i in range(1, 192):
        url = 'http://www.templatemonster.com/website-templates.php?page=%d' % i
        if not url in wait_url:
            urllist.append(url)
    master.pushTodoList(urllist)

#程序运行的main方法
#使用单线程（暂时没有多线程的需求）
if __name__ == '__main__':
    master = Master()
    addTodo(master)
    worker = Worker()
    worker.work(master)
