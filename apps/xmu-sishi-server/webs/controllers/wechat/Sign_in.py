import MySQLdb
from flask import Blueprint
from flask ilibs.Adminmport request, jsonify, g
from common.libs.Helper import getFormatDate
from common.libs.TrackService import TrackService
from common.Service import AdminService
from common.libs.VenueService import VenueService
from common.libs.UserService import UserService
from webs.controllers.wechat import route_wechat
import datetime
from application import app
import json
import random
import time


@route_wechat.route("/login", methods=["POST"])
def userLogin():
    resp = {"code": 200, "msg": "操作成功", "userid": ""}
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
    result = UserService.search_user_node(del_uesr_tel)
    if result:
        labels1 = result.labels
        if(labels1=='admin'):
        resp["msg"] = "管理员登录成功"
        else:
        resp["msg"] = "用户登录成功"


    else:
      resp["msg"] = "请去注册"
@route_wechat.route("/register", methods=["POST"])
def userRegister():
    resp =  {"code": 200, "msg": "注册操作成功", "tel": ""}
    req = request.values
    name = req["name"] if "name" in req else None
    tel = req["tel"] if "tel" in req else None
    adminPhoneList = ["13906040102"]  #凡是管理员的tel都放在这里面
    if not name:
        resp["code"] = -1
        resp["msg"] = "请给出昵称"
        return jsonify(resp)
    if not tel:
        resp["code"] = -1
        resp["msg"] = "请给出电话"
        return jsonify(resp)
    timestamp = int(round(time.time()))
    userid = str(timestamp)
    if str(tel) in adminPhoneList:
        labels = "admin"
    else:
        labels = "user"

    status = UserService.create_user_node(name,userid,tel,labels)
    if status == 1:
        resp["msg"] = "用户注册成功！"
        return jsonify(resp)
    else :
        resp["msg"] = "注册失败，请检查提交的信息"
        return jsonify(resp)