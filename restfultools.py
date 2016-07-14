#-*- coding: UTF-8 -*-
from flask import jsonify

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
