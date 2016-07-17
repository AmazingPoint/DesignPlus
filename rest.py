# -*- coding: UTF-8 -*-
from flask import Flask, request

#自定义模块
from restfultools import *
import datasource

app = Flask(__name__)


#http://api.com/designs?p=1&prep=5
#http://api.com/designs?p=1


@app.route('/')
@allow_cross_domain
def index():
    ''' 临时编写的首页导航
        事实上这些信息从每一个API函数的__doc__获得'''
    return '目前可以调用的地址：\
    <br/> http://api.datastack.cc/designs<br>method:GET\
    <br/>param: p=<int>&prep=<int>\
    </br>解释：p为请求的页数，prep为每页资源数量'


@app.route('/designs')
@allow_cross_domain
def getAPage():
    ''' 获取一页信息
        page为页数
        pre_number_page为每页数量
        返回json数据（通过自定义工具封装）'''
    page = 1
    pre_number_page = 5
    if 'p' in request.args:
        page = request.args.get('p')
    if 'prep' in request.args:
        pre_number_page = request.args.get('prep')
    if checkCountParam(page) and checkCountParam(pre_number_page):
        datas = datasource.aPage(int(page), int(pre_number_page))
        return fullResponse(R200_OK, datas)
    else:
        return statusResponse(R400_BADREQUEST)


def checkCountParam(param):
    ''' 参数检查
        检查某一个参数是否为合法的数字'''
    if isinstance(param, int):
        return True
    if isinstance(param, unicode):
        if param.isdigit():
            return True
        else:
            return False
    return False


if __name__ == '__main__':
    app.run()
