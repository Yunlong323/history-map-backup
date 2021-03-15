#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application import app,get_db
from flask import request, redirect, g,jsonify,render_template
from common.libs.AdminService import AdminService
from common.libs.UserService import UserService
from common.libs.UrlManager import UrlManager
from common.libs.Helper import getFormatDate
import re
import datetime

@app.before_request
def before_request():
    return 
    ignore_urls = app.config["IGNORE_URLS"]
    path = request.path

    pattern = re.compile("%s" % "|".join(ignore_urls))
    if pattern.match(path):
        return


    if "/test" in path:
        return


    # 微信小程序用户
    if "/wechat" in path:
        member_info = check_user_login()
        g.member_info = None
        if not member_info:
            resp = {"code": -1, "msg": "未登录", "data": {}}
            return jsonify(resp)
        g.member_info = member_info
        return


    # 后台管理员
    user_info = check_admin_login()
    g.current_user = None
    if not user_info:
        return redirect(UrlManager.buildUrl("/admin/login"))
    else:

        now = datetime.datetime.now()
        now = getFormatDate(date=now)
        if now > user_info.expiretime:
            msg="登录超时，请重新登录"
            return render_template("admin/login.html",msg=msg)
        elif user_info.status==0:
            msg="账号已禁用，请联系管理员"
            return render_template("admin/login.html",msg=msg)
        else:
            g.current_user = user_info
            return
    


def check_admin_login():
    """
    判断管理员是否已经登录
    """
    cookies = request.cookies
    auth_cookie = cookies[app.config["AUTH_COOKIE_NAME"]] if app.config["AUTH_COOKIE_NAME"] in cookies else None

    # auth_cookie='holds9AUVVMLkCJtaoJudAjINFEOsukt'#普通管理员
    # auth_cookie='tokentokentoken007'#超级管理员
    # auth_cookie='DtRncgscjxdWV9BNLY4hcWNfqHo4n4pi'

    if auth_cookie is None:
        return None

    # 返回None或Admin
    user_info=AdminService.getByToken(auth_cookie)


    return user_info



def check_user_login():
    userid = request.headers.get("userid")

    # userid="###003###"
    # userid="###003admin###"
    
    if userid is None:
        return None

    #通过token获取User
    member_info = UserService.getByUserid(userid)
    return member_info

