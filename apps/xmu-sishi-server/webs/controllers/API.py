# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from common.libs.UserService import UserService
from common.libs.TrackService import TrackService
from common.libs.Helper import getFormatDate,iPaginationForAPI
import json
from application import app
import datetime
import datetime

route_api = Blueprint('api_page', __name__)


# 外部更新用户state
@route_api.route("/setPersonState", methods=["POST"])
def setPersonState():

    resp = {"code": 200, "msg": ""}

    ip = request.remote_addr
    # resp['msg']=ip
    if ip not in app.config["ALLOWED_IP"]:
        resp['code']=-1
        resp['msg']="无权限"
        return jsonify(resp)

    try:
        reqData = json.loads(request.get_data(as_text=True))

        if "token" not in reqData or reqData['token'] != app.config["TOKEN"]:
            resp['code']=-1
            resp['msg']="无权限"
            return jsonify(resp)

        now = datetime.datetime.now()
        str_now = getFormatDate(date=now)

        for item in reqData['data']:
            UserService.updateState(item['state'],item['list'],str_now)

    except Exception as e:
        resp['code']=-1
        resp['msg']="请求失败"
        print (e)

    return jsonify(resp)


# 外部获取用户state
@route_api.route("/getPersonState", methods=["POST"])
def getPersonState():

    resp = {"code": 200, "msg": ""}

    ip = request.remote_addr
    # resp['msg']=ip
    if ip not in app.config["ALLOWED_IP"]:
        resp['code']=-1
        resp['msg']="无权限"
        return jsonify(resp)

    try:
        reqData = json.loads(request.get_data(as_text=True))
        if "token" not in reqData or reqData['token'] != app.config["TOKEN"]:
            resp['code']=-1
            resp['msg']="无权限"
            return jsonify(resp)

        page_num = reqData['data']['page_num']
        page_size = reqData['data']['page_size']
        state = reqData['data']['state']
        noList = reqData['data']['XGH']

        if state == "":
            if noList == []:  # print("noList是空")
                totalCount,stateList = UserService.getStateAll(page_num,page_size)
            else:  # print("noList不空")
                totalCount,stateList = UserService.getStateWithNoList(noList,page_num,page_size)

        elif state == "null":  # 查找状态为null的信息
            if noList == []:  # print("noList是空")
                totalCount,stateList = UserService.getStateNull(page_num,page_size)
            else:  # print("noList不空")
                totalCount,stateList = UserService.getStateNullWithNoList(noList,page_num,page_size)

        else:  # print("state不空="+state)
            state=int(state)
            if noList == []:  # print("noList是空")
                totalCount,stateList = UserService.getStateWithState(state,page_num,page_size)
            else:  # print("noList不空")
                totalCount,stateList = UserService.getStateWithNoListAndState(state,noList,page_num,page_size)

        page_params = {
            "total": totalCount,
            "page_size": page_size,
            "page_num": page_num,
            "display": app.config["PAGE_DISPLAY"],
        }

        pages = iPaginationForAPI(page_params)
        resp["pages"] = pages
        resp['data']=stateList
        
    except Exception as e:
        resp['code']=-1
        resp['msg']="请求失败"
        print (e)

    return jsonify(resp)


# 设置领导名单
@route_api.route("/setLeader", methods=["POST"])
def setLeader():

    resp = {"code": 200, "msg": ""}

    ip = request.remote_addr
    # resp['msg']=ip
    if ip not in app.config["ALLOWED_IP"]:
        resp['code']=-1
        resp['msg']="无权限"
        return jsonify(resp)

    try:
        reqData = json.loads(request.get_data(as_text=True))

        if "token" not in reqData or reqData['token'] != app.config["TOKEN"]:
            resp['code']=-1
            resp['msg']="无权限"
            return jsonify(resp)

        # 首先清空领导名单
        UserService.deleteLeader()
        # 再添加领导名单
        UserService.addLeader(reqData['data']['list'])

    except Exception as e:
        resp['code']=-1
        resp['msg']="请求失败"
        print (e)

    return jsonify(resp)


# 获取领导名单
@route_api.route("/getLeader", methods=["POST"])
def getLeader():

    resp = {"code": 200, "msg": ""}

    ip = request.remote_addr
    # resp['msg']=ip
    if ip not in app.config["ALLOWED_IP"]:
        resp['code']=-1
        resp['msg']="无权限"
        return jsonify(resp)

    try:
        reqData = json.loads(request.get_data(as_text=True))
        if "token" not in reqData or reqData['token'] != app.config["TOKEN"]:
            resp['code']=-1
            resp['msg']="无权限"
            return jsonify(resp)

        page_num=reqData['data']['page_num']
        page_size=reqData['data']['page_size']


        totalCount,userList = UserService.getLeader(page_num,page_size)
        
        page_params = {
            "total": totalCount,
            "page_size": page_size,
            "page_num": page_num,
            "display": app.config["PAGE_DISPLAY"],
        }

        pages = iPaginationForAPI(page_params)
        resp["pages"] = pages
        resp['data']=userList
        
    except Exception as e:
        resp['code']=-1
        resp['msg']="请求失败"
        print (e)

    return jsonify(resp)


# 外部添加刷卡记录
@route_api.route("/addCardTrack", methods=["POST"])
def addCardTrack():

    resp = {"code": 200, "msg": "success"}
    # IP认证
    ip = request.remote_addr
    # resp['msg']=ip
    if ip not in app.config["ALLOWED_IP"]:
        resp['code'] = -1
        resp['msg'] = "无权限"
        return jsonify(resp)

    try:
        # token认证
        reqData = json.loads(request.get_data(as_text=True))
        if "token" not in reqData or reqData['token'] != app.config["TOKEN"]:
            resp['code'] = -1
            resp['msg'] = "无权限"
            return jsonify(resp)

        # 在数据库中添加相应的用户和场所以及关系
        for track in reqData['data']['item']:
            TrackService.addCardTrack(track['user'], track['venue'], track['time'],
                                      track['source'])

    except Exception as e:
        resp['code'] = -1
        resp['msg'] = "fail"
        print(e)

    return jsonify(resp)


# 外部获取扫码记录
@route_api.route("/getScanRecord", methods=["POST"])
def getScanRecord():
    resp = {"code": 200, "msg": "success"}
    # IP认证
    ip = request.remote_addr
    # resp['msg']=ip
    if ip not in app.config["ALLOWED_IP"]:
        resp['code'] = -1
        resp['msg'] = "无权限"
        return jsonify(resp)

    try:
        # token认证
        #req = request.values
        reqData = json.loads(request.get_data(as_text=True))
        if "token" not in reqData or reqData['token'] != app.config["TOKEN"]:
            resp['code'] = -1
            resp['msg'] = "无权限"
            return jsonify(resp)

        page_num = int(reqData['data']['page_num']) if ("page_num" in reqData['data'] and reqData['data']['page_num']) else 1
        page_size = int(reqData['data']['page_size']) if ("page_size" in reqData['data'] and reqData['data']['page_size']) \
            else app.config['PAGE_SIZE']
        type = int(reqData['data']["type"]) if ("type" in reqData['data'] and reqData['data']["type"]) else 0
        venue = reqData['data']["venue"] if ("venue" in reqData['data']) else ""
        no = reqData['data']["no"] if ("no" in reqData['data']) else ""
        name = reqData['data']["name"] if ("name" in reqData['data']) else ""
        begintime = reqData['data']['begintime'] if ('begintime' in reqData['data'] and reqData['data']["begintime"]) else '0000-00-00 00:00:00'
        endtime = reqData['data']['endtime'] if ('endtime' in reqData['data'] and reqData['data']["endtime"]) else '9999-99-99 23:59:59'

        totalCount, trackList = TrackService.search("", type, venue, no, name, begintime, endtime, page_num,
                                                    page_size)

        page_params = {
            "total": totalCount,
            "page_size": page_size,
            "page_num": page_num,
            "display": app.config["PAGE_DISPLAY"],
        }

        pages = iPaginationForAPI(page_params)
        resp["data"] = trackList
        resp["pages"] = pages

    except Exception as e:
        resp['code'] = -1
        resp['msg'] = "请求失败"
        print(e)

    return jsonify(resp)


@route_api.route("/test", methods=["GET","POST"])
def test():

    resp = {"code": 200, "msg": "test"}

    # reqData = json.loads(request.get_data(as_text=True))
    # UserService.updateTest(reqData['test'])

    # UserService.updateTest()
    return jsonify(resp)
