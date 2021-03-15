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

@route_admin.route("/post")
def post_scenery_info(label_list,name,cloud,score,open_time,must_know,intro_text,intro_audio,intro_video):
    #header =  {'Access-Control-Allow-Origin':'*',"Access-Control-Allow-Methods":"PUT,GET,POST,DELETE"}
    status = AdminService.create_scenery_node(label_list,name,cloud,score,open_time,must_know,intro_text,intro_audio,intro_video)
    return jsonify(msg=status)

@route_admin.route("/delete")
def delete_scenery_node(scenery_name):
 #   header =  {'Access-Control-Allow-Origin':'*',"Access-Control-Allow-Methods":"PUT,GET,POST,DELETE"}
    status = AdminService.delete_scenery_node(scenery_name)
    return jsonify(msg=status)

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
    resp_data["list"] = _venueList
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
