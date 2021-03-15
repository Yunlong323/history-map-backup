#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify, make_response, redirect, g,render_template
import json
import requests
from common.libs.AdminService import AdminService
from common.libs.Helper import ops_render
from common.libs.UrlManager import UrlManager
from common.models.Admin import Admin
from common.libs.Helper import getFormatDate
from application import app
import re
import datetime
# from functools import wraps
# from flask import make_response
 
 
# def allow_cross_domain(fun):
#     @wraps(fun)
#     def wrapper_fun(*args, **kwargs):
#         rst = make_response(fun(*args, **kwargs))
#         rst.headers['Access-Control-Allow-Origin'] = '*'
#         rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
#         allow_headers = "Referer,Accept,Origin,User-Agent"
#         rst.headers['Access-Control-Allow-Headers'] = allow_headers
#         return rst
#     return wrapper_fun #允许跨域

route_admin = Blueprint('admin_page', __name__)

@route_admin.route("/login")
def login():
    return render_template("admin/login.html")

@route_admin.route("/post",methods=['POST'])#上传一个景点的信息
def post_scenery_info():
    resp = {"code": 200, "msg": "创建景点操作成功", "data": {}}
    req = request.values

    id = req["id"] if "id" in req else None
    label_list = req["label_list"] if "label_list" in req else None
    name = req["name"] if "name" in req else None
    cloud = req["cloud"] if "cloud" in req else None
    score = req["score"] if "score" in req else None
    open_time = req["open_time"] if "open_time" in req else None
    must_know=req["must_know"] if "must_konw" in req else None
    intro_text = req["intro_text"] if "intro_text" in req else None
    intro_audio = req["intro_audio"] if "intro_audio" in req else None
    intro_video = req["intro_video"] if "intro_video" in req else None

    if not id:
        resp["code"] = -1
        resp["msg"] = "缺少景点id信息"
        return jsonify(resp)
    elif not label_list:
        resp["code"] = -1
        resp["msg"] = "缺少景点标签列表信息"
        return jsonify(resp)
    elif not name:
        resp["code"] = -1
        resp["msg"] = "缺少景点名称信息"
        return jsonify(resp)
    elif not cloud:
        resp["code"] = -1
        resp["msg"] = "缺少景点热度信息"
        return jsonify(resp)
    elif not score:
        resp["code"] = -1
        resp["msg"] = "缺少景点评分信息"
        return jsonify(resp)
    elif not open_time:
        resp["code"] = -1
        resp["msg"] = "缺少景点开放时间信息"
        return jsonify(resp)
    elif not must_know:
        resp["code"] = -1
        resp["msg"] = "缺少景点游客须知信息"
        return jsonify(resp)
    elif not intro_text:
        resp["code"] = -1
        resp["msg"] = "缺少景点文本介绍信息"
        return jsonify(resp)
    elif not intro_audio:
        resp["code"] = -1
        resp["msg"] = "缺少景点音频介绍信息"
        return jsonify(resp)
    elif not intro_video:
        resp["code"] = -1
        resp["msg"] = "缺少景点视频介绍信息"
        return jsonify(resp)
    AdminService.create_scenery_node(id,label_list,name,cloud,score,open_time,must_know,intro_text,intro_audio,intro_video)
    return jsonify(resp_data)

@route_admin.route("/delete",methods=['POST'])
def delete_scenery_node():#通过id来删除
    resp = {"code": 200, "msg": "删除景点操作成功", "data": {}}
    req = request.values
    del_scenery_id = req["id"] if "id" in req else None    
    if not del_scenery_id:
        resp["code"] = -1
        resp["msg"] = "请正确提供景点的id值"
        return jsonify(resp)
    AdminService.delete_scenery_node(del_scenery_id)
    return jsonify(resp_data)

@route_admin.route("/display")
def display_sceneries():
    resp_data = {}
    venueList = AdminService.display_sceneries()
    _venueList= []
    for record in venueList:
        _venueList.append({
        "name": record.name,
        "cloud": record.cloud,
        "score": record.score,
        "open_time": record.open_time,
        "must_know": record.must_know,
        "intro_text": record.intro_text,
        "intro_audio": record.intro_audio,
        "intro_video": record.intro_video,
    })
    resp_data["list"] = _venueList  # 数据库返回的值用对象（字典）接
    return jsonify(resp_data)


# @route_admin.route("/logout")
# def logout():
#     # 随机化admin的token，防止重登录
#     token = AdminService.geneToken(32)
#     AdminService.updateToken(g.current_user.no,token)

#     response = make_response(redirect(UrlManager.buildUrl("/admin/login")))
#     # 删除cookie,双重保险
#     response.delete_cookie(app.config["AUTH_COOKIE_NAME"])
#     return response



#管理员登录
# @route_admin.route("/callback")
# def callback():


#     ticket = request.args.get('ticket', 'Default')
#     xml=requests.get(url='http://ids.xmu.edu.cn/authserver/serviceValidate?ticket='+ticket+'&service=https://passport.xmu.edu.cn/admin/callback')

#     if "authenticationFailure" in xml.text:
#         msg = "登录失败"
#         return render_template("admin/login.html",msg=msg)
#     else:
#         if "eduPersonStudentID" in xml.text:
#             userno = re.findall(r'<cas:eduPersonStudentID>(.*?)</cas:eduPersonStudentID>', xml.text)[0]#学号
#             usertype=1
#         else:
#             userno = re.findall(r'<cas:eduPersonStaffID>(.*?)</cas:eduPersonStaffID>', xml.text)[0]#工号
#             usertype=2
    
#         userorg = re.findall(r'<cas:eduPersonOrgDN>(.*?)</cas:eduPersonOrgDN>', xml.text)[0]#单位
#         username = re.findall(r'<cas:cn>(.*?)</cas:cn>', xml.text)[0]#单位
        
#         admin_info=AdminService.getByNoWhenLogin(userno)
#         # 管理员不存在或status为禁用状态
#         if admin_info is None:
#             msg="登录失败，无权限"
#             return render_template("admin/login.html",msg=msg)

#         token = AdminService.geneToken(32) #需要改成生成全球唯一不重复值,并且加过期时间字段

#         #过期时间为1天
#         now = datetime.datetime.now()
#         expiretime = now + datetime.timedelta(days=+1)
#         expiretime = getFormatDate(date=expiretime)

#         data= {'no': userno,'name':username,'dept': userorg,'usertype':usertype,'token':token,'expiretime':expiretime}

#         # 更新属性
#         AdminService.updateUserInfo(data)

#         #首页是流量统计,不用显示当前用户信息
#         # return render_template('index/index.html')

#         response = make_response(redirect(UrlManager.buildUrl("/")))
#         response.set_cookie(app.config["AUTH_COOKIE_NAME"], token)
#         return response
