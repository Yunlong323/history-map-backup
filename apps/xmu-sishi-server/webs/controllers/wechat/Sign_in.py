import MySQLdb
from flask import Blueprint
from flask import request, jsonify, g
from common.libs.Helper import getFormatDate
from common.libs.TrackService import TrackService
from common.libs.AdminService import AdminService
from common.libs.VenueService import VenueService
from common.libs.UserService import UserService
from webs.controllers.wechat import route_wechat
import datetime
from application import app
import json
@route_wechat.route("/login",methods=["POST"])
def userLogin():
    resp = {"code": 200, "msg": "创建景点操作成功","userid":""}
    req = request.values
    name = req["name"] if "name" in req else None
    tel = req["tel"] if "tel" in req else None
    if not name:
        resp["code"] = -1
        resp["msg"] = "请给出昵称"
        return jsonify(resp)
    if not tel:
        resp["code"] = -1
        resp["msg"] = "请给出电话"
        return jsonify(resp)
    
    # if search到了用户  数据库尚且欠缺的接口
    #     resp["msg"] = "登录成功"
    # else
    #     resp["msg"] = "请去注册"








