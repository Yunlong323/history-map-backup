#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint,jsonify,g
from common.libs.VenueService import VenueService
from common.libs.Helper import ops_render

route_index = Blueprint("index_page", __name__)

@route_index.route("/", methods=["GET", "POST"])
def index():
    return ops_render('/index/index.html')


@route_index.route("/index/getAllPOI", methods=["GET", "POST"])
def getAllPOI():

    resp_data = {"code": 200, "msg": "success", "data": {}}

    # if user_info.super==None:
    # 权限判断
    if g.current_user.super==1:#超级管理员
        data=VenueService.getAllForIndex("")
    else:#场所管理员
        data=VenueService.getAllForIndex(g.current_user.no)


    # 场所列表
    resp_data['data'] = data
    return jsonify(resp_data)

