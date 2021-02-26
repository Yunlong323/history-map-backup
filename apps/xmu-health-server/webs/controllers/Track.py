# -*- coding: utf-8 -*-
from flask import Blueprint, request,jsonify,g
from common.libs.Helper import ops_render, iPagination
from application import app
from common.libs.TrackService import TrackService

route_track = Blueprint('track_page', __name__)


@route_track.route("/index")
def index():
    return ops_render("track/index.html")


@route_track.route("/getStudentTrackByNo", methods=["POST"])
def getStudentTrackByNo():
    resp_data = {"code": 200, "msg": "操作成功", "data": {}}

    # 权限判断
    if g.current_user.super!=1:#超级管理员权限
        resp_data["code"] = -1
        resp_data["msg"] = "无权限"
        return jsonify(resp_data)

    req = request.values
    no = req["no"] if 'no' in req else ''
    page = int(req["p"]) if ("p" in req and req["p"]) else 1

    # 轨迹列表
    totalCount,trackList = TrackService.getTrackByNo(1,no,page,app.config["PAGE_SIZE"])

    page_params = {
        "total": totalCount,
        "page_size": app.config["PAGE_SIZE"],
        "page_num": page,
        "display": app.config["PAGE_DISPLAY"],
    }

    pages = iPagination(page_params)
    resp_data["list"] = trackList
    resp_data["pages"] = pages
    return jsonify(resp_data)
    

@route_track.route("/getTeacherTrackByNo", methods=["POST"])
def getTeacherTrackByNo():
    resp_data = {"code": 200, "msg": "操作成功", "data": {}}

    # 权限判断
    if g.current_user.super!=1:#超级管理员权限
        resp_data["code"] = -1
        resp_data["msg"] = "无权限"
        return jsonify(resp_data)

    req = request.values
    no = req["no"] if 'no' in req else ''
    page = int(req["p"]) if ("p" in req and req["p"]) else 1
    
    # 轨迹列表
    totalCount,trackList = TrackService.getTrackByNo(2,no,page,app.config["PAGE_SIZE"])

    page_params = {
        "total": totalCount,
        "page_size": app.config["PAGE_SIZE"],
        "page_num": page,
        "display": app.config["PAGE_DISPLAY"],
    }

    pages = iPagination(page_params)
    resp_data["list"] = trackList
    resp_data["pages"] = pages
    return jsonify(resp_data)



@route_track.route("/getStaffTrackByNo", methods=["POST"])
def getStaffTrackByNo():
    resp_data = {"code": 200, "msg": "操作成功", "data": {}}

    # 权限判断
    if g.current_user.super!=1:#超级管理员权限
        resp_data["code"] = -1
        resp_data["msg"] = "无权限"
        return jsonify(resp_data)

    req = request.values
    no = req["no"] if 'no' in req else ''
    page = int(req["p"]) if ("p" in req and req["p"]) else 1
    
    # 轨迹列表
    totalCount,trackList = TrackService.getTrackByNo(3,no,page,app.config["PAGE_SIZE"])

    page_params = {
        "total": totalCount,
        "page_size": app.config["PAGE_SIZE"],
        "page_num": page,
        "display": app.config["PAGE_DISPLAY"],
    }

    pages = iPagination(page_params)
    resp_data["list"] = trackList
    resp_data["pages"] = pages
    return jsonify(resp_data)


@route_track.route("/getTrackList", methods=["POST"])
def getTrackList():
    resp_data = {}
    req = request.values

    page = int(req["p"]) if ("p" in req and req["p"]) else 1
    type = int(req["type"]) if ("type" in req and req["type"]) else 0
    venue = req["venue"] if ("venue" in req) else ""
    no = req["no"] if ("no" in req) else ""
    name = req["name"] if ("name" in req) else ""
    begintime = req['begintime'] if ('begintime' in req and req["begintime"]) else '0000-00-00'
    endtime = req['endtime'] if ('endtime' in req and req["endtime"]) else '9999-99-99'
    endtime = endtime+" 23:59:59"


    # 权限判断
    if g.current_user.super==1:#超级管理员
        totalCount,trackList = TrackService.search("",type,venue,no,name,begintime,endtime,page,app.config["PAGE_SIZE"])
    else:#场所管理员
        totalCount,trackList = TrackService.search(g.current_user.no,type,venue,no,name,begintime,endtime,page,app.config["PAGE_SIZE"])


    page_params = {
        "total": totalCount,
        "page_size": app.config["PAGE_SIZE"],
        "page_num": page,
        "display": app.config["PAGE_DISPLAY"],
    }

    pages = iPagination(page_params)

    resp_data["list"] = trackList
    resp_data["pages"] = pages
    return jsonify(resp_data)


@route_track.route("/exportTrackList", methods=["get"])
def exportTrackList():
    req = eval(request.args.get("req"))
    def getAllTrackList():
        '''
        获取全部轨迹数据
        :param: global变量 req
        :return: track list
        '''
        if not req:
            return []
        resp_data = {}
        page = int(req["p"]) if ("p" in req and req["p"]) else 1
        type = int(req["type"]) if ("type" in req and req["type"]) else 0
        venue = req["venue"] if ("venue" in req) else ""
        no = req["no"] if ("no" in req) else ""
        name = req["name"] if ("name" in req) else ""
        begintime = req['begintime'] if ('begintime' in req and req["begintime"]) else '0000-00-00'
        endtime = req['endtime'] if ('endtime' in req and req["endtime"]) else '9999-99-99'
        endtime = endtime + " 23:59:59"

        # 权限判断
        if g.current_user.super == 1:  # 超级管理员
            totalCount, trackList = TrackService.searchAll("", type, venue, no, name, begintime, endtime)
        else:  # 场所管理员
            totalCount, trackList = TrackService.searchAll(g.current_user.no, type, venue, no, name, begintime, endtime)

        page_params = {
            "total": totalCount,
            "page_size": app.config["PAGE_SIZE"],
            "page_num": page,
            "display": app.config["PAGE_DISPLAY"],
        }

        pages = iPagination(page_params)

        resp_data["list"] = trackList
        resp_data["pages"] = pages
        return resp_data['list']
    track_list = getAllTrackList()
    response = TrackService.exportTrackList(track_list)
    return response