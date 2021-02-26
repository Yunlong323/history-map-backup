#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint,request,render_template
from common.libs.UserService import UserService
from application import app
from webs.controllers.wechat import route_wechat
import requests
import re

@route_wechat.route("/callback", methods=["GET", "POST"])
def callback():
    ticket = request.args.get('ticket', 'Default')
    xml=requests.get(url='http://ids.xmu.edu.cn/authserver/serviceValidate?ticket='+ticket+'&service=https://passport.xmu.edu.cn/wechat/callback')

    if "authenticationFailure" in xml.text:
        data= {'userno': '','userorg': '','username':'','usertype':'','userid':''}
        return render_template('callback.html',user=data)
    else:
        if "eduPersonStudentID" in xml.text:
            userno = re.findall(r'<cas:eduPersonStudentID>(.*?)</cas:eduPersonStudentID>', xml.text)[0]#学号
            userorg = re.findall(r'<cas:eduPersonOrgDN>(.*?)</cas:eduPersonOrgDN>', xml.text)[0]#单位
            usertype=1
        elif "eduPersonStaffID" in xml.text:
            userno = re.findall(r'<cas:eduPersonStaffID>(.*?)</cas:eduPersonStaffID>', xml.text)[0]#工号
            userorg = re.findall(r'<cas:eduPersonOrgDN>(.*?)</cas:eduPersonOrgDN>', xml.text)[0]#单位
            usertype=2
        else:#退休职工
            userno = re.findall(r'<cas:user>(.*?)</cas:user>', xml.text)[0]#工号
            userorg = "厦门大学"#单位
            usertype=2
        
        
        username = re.findall(r'<cas:cn>(.*?)</cas:cn>', xml.text)[0]#姓名
        
        userid = UserService.geneUserid(userno, app.config["SALT"])
        data= {'userno': userno,'userorg': userorg,'username':username,'usertype':usertype,'userid':userid}

        UserService.updateUser(data)
        
        return render_template('callback.html',user=data)

