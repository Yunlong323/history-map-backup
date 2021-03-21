# -*- coding: utf-8 -*-
from flask import Blueprint, request,jsonify,g
from common.libs.Helper import ops_render, iPagination
from common.libs.UrlManager import UrlManager
from common.libs.UserService import UserService
from application import app

route_user = Blueprint('user_page', __name__)

@route_user.route("/student")
def student():
    return ops_render("user/student.html")

@route_user.route("/teacher")
def teacher():
    return ops_render("user/teacher.html")

@route_user.route("/staff")
def staff():
    return ops_render("user/staff.html")

@route_user.route("/getStudentList", methods=["POST"])
def getStudentList():
    return getUserList(1)

@route_user.route("/getTeacherList", methods=["POST"])
def getTeacherList():
    return getUserList(2)

@route_user.route("/getStaffList", methods=["POST"])
def getStaffList():
    return getUserList(3)

def getUserList(usertype):
    resp_data = {"code": 200, "msg": "操作成功", "data": {}}

    # 权限判断
    if g.current_user.super!=1:#超级管理员权限
        resp_data["code"] = -1
        resp_data["msg"] = "无权限"
        return jsonify(resp_data)

    req = request.values
    page = int(req["p"]) if ("p" in req and req["p"]) else 1
    dept = req["dept"] if 'dept' in req else ''
    no = req["no"] if 'no' in req else ''
    name = req["name"] if 'name' in req else ''

    totalCount,userList = UserService.search(usertype,dept,no,name,page,app.config["PAGE_SIZE"])

    page_params = {
        "total": totalCount,
        "page_size": app.config["PAGE_SIZE"],
        "page_num": page,
        "display": app.config["PAGE_DISPLAY"],
    }

    pages = iPagination(page_params)
    
    resp_data["list"] = userList
    resp_data["pages"] = pages
    return jsonify(resp_data)

