#-*- coding: UTF-8 -*-
from flask import jsonify
from functools import wraps
from flask import make_response

#参考restful规范 定义的一堆状态
R200_OK = {'code': 200, 'message': 'OK all right.'}
R201_CREATED = {'code': 201, 'message': 'All created.'}
R204_NOCONTENT = {'code': 204, 'message': 'All deleted.'}
R400_BADREQUEST = {'code': 400, 'message': 'Bad request.'}
R401_UNAUTHORIZED = {'code': 401, 'message': 'Unauthorized.'}
R403_FORBIDDEN = {'code': 403, 'message': 'You can not do this.'}
R404_NOTFOUND = {'code': 404, 'message': 'No result matched.'}


def fullResponse(statu_dic, data):
    '''返回数据信息和状态信息'''
    return jsonify({'status': statu_dic, 'data': data})


def statusResponse(statu_dic):
    '''返回状态信息'''
    return jsonify({'status': statu_dic})


def allow_cross_domain(fun):
    ''' 装饰器：
        为headers添加访问控制信息
        解除web端跨域访问的限制'''

    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun
