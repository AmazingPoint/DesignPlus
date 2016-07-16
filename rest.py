# -*- coding: UTF-8 -*-
from flask import Flask, request, jsonify
from restfultools import *
import datasource

app = Flask(__name__)


#http://api.com/designs?p=1&prep=5
#http://api.com/designs?p=1

@app.route('/designs')
@allow_cross_domain
def getAPage():
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
    if isinstance(param, int):
        return True
    if isinstance(param, unicode):
        if param.isdigit():
            return True
        else:
            return False
