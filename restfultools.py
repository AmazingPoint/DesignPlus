#-*- coding: UTF-8 -*-
from flask import jsonify
from functools import wraps
from flask import make_response

# define statu_dics here
R200_OK = {'code': 200, 'message': 'OK all right.'}
R201_CREATED = {'code': 201, 'message': 'All created.'}
R204_NOCONTENT = {'code': 204, 'message': 'All deleted.'}
R400_BADREQUEST= {'code': 400, 'message': 'Bad request.'}
R401_UNAUTHORIZED= {'code': 401, 'message': 'Unauthorized.'}
R403_FORBIDDEN = {'code': 403, 'message': 'You can not do this.'}
R404_NOTFOUND = {'code': 404, 'message': 'No result matched.'}


def fullResponse(statu_dic, data):
    return jsonify({'status': statu_dic, 'data': data})


def statusResponse(statu_dic):
    return jsonify({'status': statu_dic})


def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun
