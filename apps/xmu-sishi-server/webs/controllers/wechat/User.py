#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import MySQLdb
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

@route_wechat.route("/getSceneryInfo",methods=["POST"])
def getSceneryInfo():
    resp = {"code": 200, "msg": "创建景点操作成功", "intro_text":"","intro_audio":"","intro_video":""}
    scenery_id = request.values["scenery_id"] if "scenery_id" in request.values else None
    #约定接口POST过来{"scenery_id":"0"}
    if not scenery_name:
        resp["code"] = -1
        resp["msg"] = "没有正确给出景点id"
        return jsonify(resp)
    
    node = AdminService.getSceneryNodeInfo(scenery_id)
    resp["intro_text"] = node.intro_text
    resp["intro_audio"] = node.intro_audio
    resp["intro_video"] = node.intro_video 
    return jsonify(resp)




@route_wechat.route("/addTrack", methods=["GET","POST"])
def addTrack():
    resp = {"code": 1000, "msg": "venue_name", "data": {}}
    req = request.values
    venueid = req["venueid"] if "venueid" in req else None
    if not venueid:
        resp["code"] = -1
        resp["msg"] = "需要场所id"
        return jsonify(resp)

    venue_info=VenueService.getByID(venueid)

    if not venue_info:
        resp["code"] = -1
        resp["msg"] = "场所不存在"
        return jsonify(resp)

    if venue_info.status==-1:
        resp["code"] = -1
        resp["msg"] = "场所已删除"
        return jsonify(resp)

    member_info = g.member_info
    if member_info.leader == None:  # 不是领导
        resp['data']={
            "userdept": member_info.dept,
            "username": member_info.name,
        }
    else:#是领导
        resp['data']={
            "userdept": "",
            "username": "领导",
        }
    
    # if "STUDENT" in member_info.labels:#学生
    #     print("是学生")
    # if "TEACHER" in member_info.labels:#教职工
    #     print("是老师")

    # print(venue_info.permissionType)
    

    now = datetime.datetime.now()
    str_now = getFormatDate(date=now)
    # now = datetime.datetime.now()
    # expiretime = now + datetime.timedelta(days=+10)
    # str_now = getFormatDate(date=expiretime)

    #人员state=-1直接红码
    if member_info.state==-1:
        # print("红码")
        resp["code"] = 2000
        resp["msg"] = venue_info.name #获取场所名称返回 放在msg里
        return jsonify(resp)

    #人员state=1直接绿码
    if member_info.state==1:
        # print("超级用户绿码")
        # 添加轨迹
        TrackService.create(member_info.no,venueid,str_now,1)#type=1 绿码 2黄码

        resp["code"] = 1001#1001绿码 1002黄码 #2000红码
        resp["msg"] = venue_info.name#绿码
        return jsonify(resp)

    # 判断是否有提交过审批 需要审批通过且时间合法
    result2 = UserService.hasLegalApply(member_info.no,venueid,str_now)
    if result2 == True:
        TrackService.create(member_info.no,venueid,str_now,1)#绿码
        resp["code"] = 1001#1001绿码 1002黄码 #2000红码
        resp["msg"] = venue_info.name
        return jsonify(resp)


    permissionType=venue_info.permissionType
    if permissionType==2:#对全体教职工开放
        if "TEACHER" in member_info.labels:#教职工
            # print("绿码")
            TrackService.create(member_info.no,venueid,str_now,1)#type=1 绿码 2黄码
            resp["code"] = 1001#1001绿码 1002黄码 #2000红码
            resp["msg"] = venue_info.name#绿码
            return jsonify(resp)
        else:
            # print("黄码")
            TrackService.create(member_info.no,venueid,str_now,2)#type=1 绿码 2黄码
            resp["code"] = 1002#1001绿码 1002黄码 #2000红码
            resp["msg"] = venue_info.name#绿码
            return jsonify(resp)
    elif permissionType==3:#对全体学生开放
        if "STUDENT" in member_info.labels:#学生
            # print("绿码")
            TrackService.create(member_info.no,venueid,str_now,1)#type=1 绿码 2黄码
            resp["code"] = 1001#1001绿码 1002黄码 #2000红码
            resp["msg"] = venue_info.name#绿码
            return jsonify(resp)
        else:
            TrackService.create(member_info.no,venueid,str_now,2)#type=1 绿码 2黄码
            resp["code"] = 1002#1001绿码 1002黄码 #2000红码
            resp["msg"] = venue_info.name#绿码
            return jsonify(resp)
    elif permissionType==4:#对所有人开放
        TrackService.create(member_info.no,venueid,str_now,1)#type=1 绿码 2黄码
        resp["code"] = 1001#1001绿码 1002黄码 #2000红码
        resp["msg"] = venue_info.name#绿码
        return jsonify(resp)
    else:#permissionType==1 #根据白名单授权

        if member_info.state == None:#没有赋值过state状态,暂且当做黄码处理
            # 添加轨迹
            TrackService.create(member_info.no,venueid,str_now,2)#type=1 绿码 2黄码
            resp["code"] = 1002#1001绿码 1002黄码 #2000红码
            resp["msg"] = venue_info.name#绿码
            return jsonify(resp)

        if member_info.state==0:
            # print("需要进一步判断")

            result = TrackService.hasPermission(member_info.no,venueid)
            if result == True:
                # print("有权限")
                type=1
                resp["code"] = 1001#1001绿码 1002黄码 #2000红码
            else:
                type=2
                resp["code"] = 1002#1001绿码 1002黄码 #2000红码

            # 添加轨迹
            TrackService.create(member_info.no,venueid,str_now,type)#绿码
            resp["msg"] = venue_info.name
            return jsonify(resp)


@route_wechat.route("/getMyTrack", methods=["GET", "POST"])
def getMyTrack():

    req = request.values
    pageNum = int(req["pageNum"]) if ("pageNum" in req and req["pageNum"]) else 1
    pageSize = int(req["pageSize"]) if ("pageSize" in req and req["pageSize"]) else app.config["PAGE_SIZE"]

    member_info = g.member_info
    resp_data = {"code": 200, "msg": "success", "data": {}}
    trackList = TrackService.getMyTrackByNo(member_info.no,pageNum,pageSize)

    resp_data['data'] = trackList
    return jsonify(resp_data)



@route_wechat.route("/login", methods=["POST"])
def login():

    resp = {"code": 200, "msg": "", "data": {}}

    req = request.values
    userno = req["userno"] if "userno" in req else None
    if not userno:
        resp["code"] = -1
        resp["msg"] = "请输入完整信息"
        return jsonify(resp)

    username = req["username"] if "username" in req else None
    if not username:
        resp["code"] = -1
        resp["msg"] = "请输入完整信息"
        return jsonify(resp)


    # 连接数据库匹配count()，等于1则存在账号，登录成功。否则失败
    # if userno!='186123456' or username!='张三':
    exist,userorg=checkExist(userno,username)

    if exist==False:
        resp["code"] = -1
        resp["msg"] = "账号不存在"
        return jsonify(resp)
    
    usertype = 3
    userid = UserService.geneUserid(userno, app.config["SALT"])

    data= {'userno': userno,'userorg': userorg,'username':username,'usertype':usertype,'userid':userid}
    UserService.updateUser(data)

    resp["data"] = data
    return jsonify(resp)


def checkExist(userno,username):

    # 打开数据库连接
    # _db = MySQLdb.connect(app.config.get("MYSQL")["address"], app.config.get("MYSQL")["username"], app.config.get("MYSQL")["password"], app.config.get("MYSQL")["schema"], charset='utf8' )
    _db = ""
    # 使用cursor()方法获取操作游标 
    cursor = _db.cursor()
    
    # sql = "SELECT Id,TBRQ,XGH,XM,DWMC,JRJKZK,JRJLDGJ,SFZX,SZSSQ,QTXYSMSX,CZLX,CLRQ from V_XS_MRJK where Id>'%s'" % (maxId)

    # sql = "SELECT distinct XGH from V_JBXX order by XGH asc limit 10"
    # sql = "SELECT COUNT(1),DWMC from V_JBXX WHERE XGH=%s AND XM=%s"
    sql = "SELECT COUNT(1),any_value(DWMC) from V_JBXX_QT WHERE SJH=%s AND XM=%s"
    # print(sql)
    count=0
    dept=""

    try:
        # 执行SQL语句
        cursor.execute(sql,(userno,username))
        # 获取所有记录列表
        result = cursor.fetchone()
        count=result[0]
        dept=result[1]

        # print("结果有"+str(count)+"个,"+str(dept))
        
        
    except Exception as ex:
       # 发生错误时回滚
        print(ex)
        _db.rollback()
        
    finally:
        # 关闭数据库连接
        _db.close()


        if count==0:
            return False,dept
        else:
            return True,dept



# 审批相关

# 1 普通用户
# 获取场所列表和审核人列表 不分页
@route_wechat.route("/getVenueAndReviewer", methods=["GET","POST"])
def getVenueAndReviewer():
    resp_data = {"code": 200, "msg": "success", "venueList": {},"reviewerList": {}}
    
    venueList = VenueService.getVenueIdAndName()
    reviewerList = UserService.getReviewerNoAndName()
    
    resp_data['venueList'] = venueList
    resp_data['reviewerList'] = reviewerList
    return jsonify(resp_data)


# 提交的新的申请
@route_wechat.route("/addApply", methods=["GET","POST"])
def addApply():
    resp = {"code": 200, "msg": "success", "data": {}}
    req = request.values

    venueid = req["venueid"] if "venueid" in req else None
    if not venueid:
        resp["code"] = -1
        resp["msg"] = "请选择场所"
        return jsonify(resp)

    reviewer = req["reviewer"] if "reviewer" in req else None
    if not reviewer:
        resp["code"] = -1
        resp["msg"] = "请选择审核人"
        return jsonify(resp)

    starttime = req["starttime"] if "starttime" in req else None
    if not starttime:
        resp["code"] = -1
        resp["msg"] = "请选择开始时间"
        return jsonify(resp)

    endtime = req["endtime"] if "endtime" in req else None
    if not endtime:
        resp["code"] = -1
        resp["msg"] = "请选择结束时间"
        return jsonify(resp)

    reason = req["reason"] if "reason" in req else None
    if not reason:
        resp["code"] = -1
        resp["msg"] = "请填写申请原因"
        return jsonify(resp)

    id = VenueService.geneVenueID() #生成审批id
    applytime = getFormatDate(date=datetime.datetime.now())

    member_info = g.member_info
    UserService.addApply(member_info.no,venueid,reviewer,id,applytime,starttime,endtime,reason)

    return jsonify(resp)


# 获取我提交的申请列表(含详情) 分页
@route_wechat.route("/getMyApply", methods=["GET","POST"])
def getMyApply():
    req = request.values
    pageNum = int(req["pageNum"]) if ("pageNum" in req and req["pageNum"]) else 1
    pageSize = int(req["pageSize"]) if ("pageSize" in req and req["pageSize"]) else app.config["PAGE_SIZE"]
    type = int(req["type"]) if ("type" in req and req["type"]) else 1 #1全部 2未审 3已审

    member_info = g.member_info
    resp_data = {"code": 200, "msg": "success", "data": {}}
    applyList = UserService.getMyApply(member_info.no,type,pageNum,pageSize)

    resp_data['data'] = applyList
    return jsonify(resp_data)




# 2 审核人
# 查看提交给我的申请列表 已审/待审 分页
@route_wechat.route("/getMyApprove", methods=["GET","POST"])
def getMyApprove():
    req = request.values
    pageNum = int(req["pageNum"]) if ("pageNum" in req and req["pageNum"]) else 1
    pageSize = int(req["pageSize"]) if ("pageSize" in req and req["pageSize"]) else app.config["PAGE_SIZE"]
    type = int(req["type"]) if ("type" in req and req["type"]) else 1 #1全部 2未审 3已审

    member_info = g.member_info
    resp_data = {"code": 200, "msg": "success", "data": {}}
    approveList = UserService.getMyApprove(member_info.no,type,pageNum,pageSize)

    resp_data['data'] = approveList
    return jsonify(resp_data)


# 审批:通过/拒绝
@route_wechat.route("/approve", methods=["GET","POST"])
def approve():
    resp = {"code": 200, "msg": "success", "data": {}}
    req = request.values

    id = req["id"] if "id" in req else None
    if not id:
        resp["code"] = -1
        resp["msg"] = "请选择审批单"
        return jsonify(resp)

    state = int(req["state"]) if ("state" in req and req["state"]) else None
    if not state:
        resp["code"] = -1
        resp["msg"] = "请选择意见"
        return jsonify(resp)


    approvetime = getFormatDate(date=datetime.datetime.now())
    member_info = g.member_info

    UserService.approve(member_info.no,id,state,approvetime)
    return jsonify(resp)


# 批量审批:通过/拒绝
@route_wechat.route("/approveBatch", methods=["GET","POST"])
def approveBatch():
    resp = {"code": 200, "msg": "success", "data": {}}
    req = request.values

    ids = req["ids"] if "ids" in req else None
    if not ids:
        resp["code"] = -1
        resp["msg"] = "请选择审批单"
        return jsonify(resp)

    state = int(req["state"]) if ("state" in req and req["state"]) else None
    if not state:
        resp["code"] = -1
        resp["msg"] = "请选择意见"
        return jsonify(resp)


    approvetime = getFormatDate(date=datetime.datetime.now())
    member_info = g.member_info

    for id in ids.split(","):
        # print(id)
        UserService.approve(member_info.no,id,state,approvetime)

    return jsonify(resp)



# 撤销
@route_wechat.route("/cancel", methods=["GET","POST"])
def cancel():
    resp = {"code": 200, "msg": "success", "data": {}}
    req = request.values

    ids = req["ids"] if "ids" in req else None
    if not ids:
        resp["code"] = -1
        resp["msg"] = "请选择审批单"
        return jsonify(resp)

    member_info = g.member_info
    
    for id in ids.split(","):
        UserService.cancel(member_info.no,id)
    return jsonify(resp)



# 反扫功能 获取我管理的场所
@route_wechat.route("/getMyVenue", methods=["GET","POST"])
def getMyVenue():
    resp_data = {"code": 200, "msg": "success", "venueList": {}}
    
    member_info = g.member_info
    venueList = VenueService.getMyVenueIdAndName(member_info.no)
    
    resp_data['venueList'] = venueList
    return jsonify(resp_data)


# 反扫
@route_wechat.route("/addTrackByAdmin", methods=["GET","POST"])
def addTrackByAdmin():
    resp = {"code": 1000, "msg": "venue_name", "data": {}}
    req = request.values
    venueid = req["venueid"] if "venueid" in req else None
    if not venueid:
        resp["code"] = -1
        resp["msg"] = "需要场所id"
        return jsonify(resp)

    userid = req["userid"] if "userid" in req else None
    if not userid:
        resp["code"] = -1
        resp["msg"] = "需要用户id"
        return jsonify(resp)


    venue_info=VenueService.getByID(venueid)

    if not venue_info:
        resp["code"] = -1
        resp["msg"] = "场所不存在"
        return jsonify(resp)

    if venue_info.status==-1:
        resp["code"] = -1
        resp["msg"] = "场所已删除"
        return jsonify(resp)

    #通过userid获取User
    member_info = UserService.getByUserid(userid)
    if not member_info:
        resp["code"] = -1
        resp["msg"] = "用户不存在"
        return jsonify(resp)


    if member_info.leader == None:#不是领导
        resp['data']={
            "userdept": member_info.dept,
            "username": member_info.name,
        }
    else:#是领导
        resp['data']={
            "userdept": "",
            "username": "领导",
        }
        

    now = datetime.datetime.now()
    str_now = getFormatDate(date=now)
    # now = datetime.datetime.now()
    # expiretime = now + datetime.timedelta(days=+10)
    # str_now = getFormatDate(date=expiretime)

    currentUser = g.member_info

    # -1直接红码
    if member_info.state==-1:
        # print("红码")
        resp["code"] = 2000
        resp["msg"] = venue_info.name #获取场所名称返回 放在msg里
        return jsonify(resp)

    # 1直接绿码
    if member_info.state==1:
        # print("超级用户绿码")
        # 添加轨迹
        TrackService.createByAdmin(currentUser.no,member_info.no,venueid,str_now,1)#type=1 绿码 2黄码

        resp["code"] = 1001#1001绿码 1002黄码 #2000红码
        resp["msg"] = venue_info.name#绿码
        return jsonify(resp)

    # 判断是否有提交过审批 需要审批通过且时间合法
    result2 = UserService.hasLegalApply(member_info.no,venueid,str_now)
    if result2 == True:
        TrackService.create(member_info.no,venueid,str_now,1)#绿码
        resp["code"] = 1001#1001绿码 1002黄码 #2000红码
        resp["msg"] = venue_info.name
        return jsonify(resp)

    permissionType=venue_info.permissionType
    if permissionType==2:#对全体教职工开放
        if "TEACHER" in member_info.labels:#教职工
            # print("绿码")
            TrackService.createByAdmin(currentUser.no,member_info.no,venueid,str_now,1)#type=1 绿码 2黄码
            resp["code"] = 1001#1001绿码 1002黄码 #2000红码
            resp["msg"] = venue_info.name#绿码
            return jsonify(resp)
        else:
            # print("黄码")
            TrackService.createByAdmin(currentUser.no,member_info.no,venueid,str_now,2)#type=1 绿码 2黄码
            resp["code"] = 1002#1001绿码 1002黄码 #2000红码
            resp["msg"] = venue_info.name#绿码
            return jsonify(resp)
    elif permissionType==3:#对全体学生开放
        if "STUDENT" in member_info.labels:#学生
            # print("绿码")
            TrackService.createByAdmin(currentUser.no,member_info.no,venueid,str_now,1)#type=1 绿码 2黄码
            resp["code"] = 1001#1001绿码 1002黄码 #2000红码
            resp["msg"] = venue_info.name#绿码
            return jsonify(resp)
        else:
            # print("黄码")
            TrackService.createByAdmin(currentUser.no,member_info.no,venueid,str_now,2)#type=1 绿码 2黄码
            resp["code"] = 1002#1001绿码 1002黄码 #2000红码
            resp["msg"] = venue_info.name#绿码
            return jsonify(resp)
    elif permissionType==4:#对所有人开放
        # print("绿码")
        TrackService.createByAdmin(currentUser.no,member_info.no,venueid,str_now,1)#type=1 绿码 2黄码
        resp["code"] = 1001#1001绿码 1002黄码 #2000红码
        resp["msg"] = venue_info.name#绿码
        return jsonify(resp)
    else:#permissionType==1 #根据白名单授权

        if member_info.state == None:#没有赋值过state状态,暂且当做黄码处理
            # 添加轨迹
            TrackService.createByAdmin(currentUser.no,member_info.no,venueid,str_now,2)#type=1 绿码 2黄码
            resp["code"] = 1002#1001绿码 1002黄码 #2000红码
            resp["msg"] = venue_info.name#绿码
            return jsonify(resp)


        if member_info.state==0:
            # print("需要进一步判断")

            result = TrackService.hasPermission(member_info.no,venueid)
            if result == True:
                # print("有权限")
                type=1
                resp["code"] = 1001#1001绿码 1002黄码 #2000红码
            else:
                type=2
                resp["code"] = 1002#1001绿码 1002黄码 #2000红码

            # 添加轨迹
            TrackService.createByAdmin(currentUser.no,member_info.no,venueid,str_now,type)#绿码
            resp["msg"] = venue_info.name
            return jsonify(resp)


