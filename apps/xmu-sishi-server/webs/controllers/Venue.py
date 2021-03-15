# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect,jsonify,g
from common.libs.Helper import ops_render, iPagination,createWXcode,getFormatDate,getCurrentDate,getParserValue
from common.libs.UrlManager import UrlManager
from common.libs.VenueService import VenueService
from application import app
import datetime
import time
# 文件相关
from werkzeug.utils import secure_filename
import os
import stat
import uuid
import csv

route_venue = Blueprint('venue_page', __name__)

@route_venue.route("/index")
def index():
    return ops_render("venue/index.html")


@route_venue.route("/getVenueList", methods=["POST"])
def getVenueList():

    resp_data = {}
    req = request.values
    page = int(req["p"]) if ("p" in req and req["p"]) else 1
    status = int(req["status"]) if ("status" in req and req["status"]) else 0
    name = req["name"] if 'name' in req else ''

    # 权限判断
    if g.current_user.super==1:#超级管理员
        totalCount,venueList = VenueService.search("",status,name,page,app.config["PAGE_SIZE"])
        resp_data["super"]=1
    else:#场所管理员
        totalCount,venueList = VenueService.search(g.current_user.no,status,name,page,app.config["PAGE_SIZE"])
        resp_data["super"]=0


    page_params = {
        "total": totalCount,
        "page_size": app.config["PAGE_SIZE"],
        "page_num": page,
        "display": app.config["PAGE_DISPLAY"],
    }

    pages = iPagination(page_params)
    
    _venueList=[]
    for record in venueList:
        _venueList.append({
        "id": record.id,
        "name": record.name,
        "lat": record.lat,
        "lon": record.lon,
        "status": record.status,
        "permissionType": record.permissionType,
        "createtime": record.createtime,
    })

    resp_data["list"] = _venueList
    resp_data["pages"] = pages
    return jsonify(resp_data)


@route_venue.route("/reverseStatus", methods=["POST"])
def reverseStatus():
    resp = {"code": 200, "msg": "操作成功", "data": {}}
    req = request.values

    id = req["id"] if "id" in req else None
    
    if not id:
        resp["code"] = -1
        resp["msg"] = "请选择需要操作的场所"
        return jsonify(resp)

    # 权限判断
    if g.current_user.super==1:#超级管理员
        VenueService.reverseStatus("",id)
    else:#场所管理员
        VenueService.reverseStatus(g.current_user.no,id)
    
    return jsonify(resp)


@route_venue.route("/editVenue", methods=["POST"])
def editVenue():

    resp = {"code": 200, "msg": "操作成功", "data": {}}
    req = request.values

    id = req["id"] if "id" in req else None
    name = req["name"] if "name" in req else None
    lon = req["lon"] if "lon" in req else None
    lat = req["lat"] if "lat" in req else None
    permissionType = int(req["permissionType"]) if ("permissionType" in req and req["permissionType"]) else 1
    
    if not name:
        resp["code"] = -1
        resp["msg"] = "请输入场所名称"
        return jsonify(resp)

    if not lon or not lat:
        resp["code"] = -1
        resp["msg"] = "请选择场所地点"
        return jsonify(resp)

    if permissionType not in [1,2,3,4]:
        permissionType=1

    name = getParserValue(name)
    lon = getParserValue(lon)
    lat = getParserValue(lat)

    # print("name=="+name+"-lon"+lon+"-"+lat)

    resp["msg"] = "保存成功"

    if not id:#新增

        # 权限判断
        if g.current_user.super==1:#超级管理员才能新增
            id = VenueService.geneVenueID()
            createtime = getFormatDate(date=datetime.datetime.now())
            VenueService.create(id,name,lon,lat,permissionType,createtime)

            # 获取小程序码
            url=createWXcode(id)
            resp["wxCodeUrl"]=url;
        else:
            resp["code"] = -1
            resp["msg"] = "无权限"
            return jsonify(resp)

    else:#修改
        # 权限判断
        if g.current_user.super==1:#超级管理员
            VenueService.update("",id,name,lon,lat,permissionType)
        else:#场所管理员
            VenueService.update(g.current_user.no,id,name,lon,lat,permissionType)

    return jsonify(resp)


@route_venue.route("/getVenueStatistics", methods=["POST"])
def getVenueStatistics():
    resp_data = {"code": 200, "msg": "success", "data": {}}
    req = request.values
    id = req["id"] if 'id' in req else ''
    
    
    # 权限判断
    if g.current_user.super==1:#超级管理员
        statistics = VenueService.getVenueStatistics("",id)
    else:#场所管理员
        statistics = VenueService.getVenueStatistics(g.current_user.no,id)

    resp_data['data'] = statistics
    return jsonify(resp_data)



# tags的详细信息
@route_venue.route("/getWhiteListTagsDetail", methods=["POST"])
def getWhiteListTagsDetail():

    resp_data = {}
    req = request.values
    id = req["id"] if 'id' in req else ''
    
    # 权限判断
    if g.current_user.super==1:#超级管理员
        tagList = VenueService.getWhiteListTagsDetail("",id)
    else:#场所管理员
        tagList = VenueService.getWhiteListTagsDetail(g.current_user.no,id)

    resp_data["list"] = tagList

    return jsonify(resp_data)



@route_venue.route("/getWhiteList", methods=["POST"])
def getWhiteList():
    # timestamp=int(round(time.time()))
    # time_str=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(timestamp))
    # print(timestamp)
    # print(time_str)

    resp_data = {}
    req = request.values
    tagID = int(req["tagID"]) if 'tagID' in req else 0
    id = req["id"] if 'id' in req else ''
    dept = req["dept"] if 'dept' in req else ''
    no = req["no"] if 'no' in req else ''
    name = req["name"] if 'name' in req else ''
    page = int(req["p"]) if ("p" in req and req["p"]) else 1

    # 权限判断
    if g.current_user.super==1:#超级管理员
        totalCount,whiteList = VenueService.getWhiteList("",tagID,id,dept,no,name,page,app.config["PAGE_SIZE"])
    else:#场所管理员
        totalCount,whiteList = VenueService.getWhiteList(g.current_user.no,tagID,id,dept,no,name,page,app.config["PAGE_SIZE"])

    page_params = {
        "total": totalCount,
        "page_size": app.config["PAGE_SIZE"],
        "page_num": page,
        "display": app.config["PAGE_DISPLAY"],
    }

    pages = iPagination(page_params)
    
    resp_data["list"] = whiteList
    resp_data["pages"] = pages

    return jsonify(resp_data)


@route_venue.route("/uploadWhitelist", methods=["POST"])
def uploadWhitelist():
    resp = {"code": 200, "msg": "success", "data": {}}

    tag_name = request.values["tag_name"] if 'tag_name' in request.values else ""
    id = request.values["venue_id"] if "venue_id" in request.values else None
    file = request.files["file"] if "file" in request.files else None
    
    if not id:
        resp["code"] = -1
        resp["msg"] = "请选择场所"
        return jsonify(resp)

    if not tag_name:
        resp["code"] = -1
        resp["msg"] = "请输入批次名"
        return jsonify(resp)

    if not file:
        resp["code"] = -1
        resp["msg"] = "请选择文件"
        return jsonify(resp)

    tag_name = getParserValue(tag_name)#防注入

    # 保存文件
    config_upload = app.config["UPLOAD"]
    # filename = secure_filename(file.filename)
    filename = file.filename

    ext = filename.rsplit(".", 1)[1] #后缀名
    if ext not in config_upload["ext"]:
        resp["code"] = -1
        resp["msg"] = "文件类型错误"
        return jsonify(resp)

    root_path = app.root_path + config_upload["whitelist_prefix_path"]
    file_dir = getCurrentDate("%Y%m%d")
    save_dir = root_path + file_dir
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
        os.chmod(save_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IRWXO)

    file_name = str(uuid.uuid4()).replace("-", "") + "." + ext
    filepathname="{0}/{1}".format(save_dir, file_name)
    file.save(filepathname)


    whitelist=[]
    with open(filepathname, 'r',encoding='UTF-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or not row[0]:
                continue
            else:
                if row[0].strip()!="":
                    whitelist.append(getParserValue(row[0].strip()))#防注入

    # # 权限判断
    # if g.current_user.super==1:#超级管理员
    #     # 先批量删
    #     VenueService.deleteWhiteList("",tag,id)
    #     # 再批量增
    #     VenueService.updateWhiteList("",tag,id,whitelist)
    # else:#场所管理员
    #     # 先批量删
    #     VenueService.deleteWhiteList(g.current_user.no,tag,id)
    #     # 再批量增
    #     VenueService.updateWhiteList(g.current_user.no,tag,id,whitelist)

    timestamp=int(round(time.time()))
    tag = {
        "id": timestamp,
        "tag": tag_name,
        "active": 1,
    }

    # 权限判断
    if g.current_user.super==1:#超级管理员
        VenueService.updateWhiteList("",tag,id,whitelist)
    else:#场所管理员
        VenueService.updateWhiteList(g.current_user.no,tag,id,whitelist)
    return jsonify(resp)

@route_venue.route("/reverseTagStatus", methods=["POST"])
def reverseTagStatus():
    resp = {"code": 200, "msg": "操作成功", "data": {}}
    req = request.values

    id = req["id"] if "id" in req else None
    tagID = int(req["tagID"]) if "tagID" in req else None
    
    if not id:
        resp["code"] = -1
        resp["msg"] = "请选择需要操作的场所"
        return jsonify(resp)

    if not tagID:
        resp["code"] = -1
        resp["msg"] = "请选择需要操作的白名单"
        return jsonify(resp)

    # 权限判断
    if g.current_user.super==1:#超级管理员
        VenueService.reverseTagStatus("",id,tagID)
    else:#场所管理员
        VenueService.reverseTagStatus(g.current_user.no,id,tagID)
    
    return jsonify(resp)


@route_venue.route("/deleteTag", methods=["POST"])
def deleteTag():
    resp = {"code": 200, "msg": "操作成功", "data": {}}
    req = request.values

    id = req["id"] if "id" in req else None
    tagID = int(req["tagID"]) if "tagID" in req else None
    
    if not id:
        resp["code"] = -1
        resp["msg"] = "请选择需要操作的场所"
        return jsonify(resp)

    if not tagID:
        resp["code"] = -1
        resp["msg"] = "请选择需要操作的白名单"
        return jsonify(resp)

    # 权限判断
    if g.current_user.super==1:#超级管理员
        VenueService.deleteTag("",id,tagID)
    else:#场所管理员
        VenueService.deleteTag(g.current_user.no,id,tagID)
    
    return jsonify(resp)


@route_venue.route("/uploadBatchWhitelist", methods=["POST"])
def uploadBatchWhitelist():
    resp = {"code": 200, "msg": "success", "data": {}}

    tag_name = request.values["tag_name"] if 'tag_name' in request.values else ""
    ids = request.values["venue_ids"] if "venue_ids" in request.values else None
    file = request.files["file"] if "file" in request.files else None
    
    ids=ids.split(",")

    if not ids:
        resp["code"] = -1
        resp["msg"] = "请选择场所"
        return jsonify(resp)

    if not tag_name:
        resp["code"] = -1
        resp["msg"] = "请输入批次名"
        return jsonify(resp)

    if not file:
        resp["code"] = -1
        resp["msg"] = "请选择文件"
        return jsonify(resp)


    # 保存文件
    config_upload = app.config["UPLOAD"]
    # filename = secure_filename(file.filename)
    filename = file.filename

    ext = filename.rsplit(".", 1)[1] #后缀名
    if ext not in config_upload["ext"]:
        resp["code"] = -1
        resp["msg"] = "文件类型错误"
        return jsonify(resp)

    root_path = app.root_path + config_upload["whitelist_prefix_path"]
    file_dir = getCurrentDate("%Y%m%d")
    save_dir = root_path + file_dir
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
        os.chmod(save_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IRWXO)

    file_name = str(uuid.uuid4()).replace("-", "") + "." + ext
    filepathname="{0}/{1}".format(save_dir, file_name)
    file.save(filepathname)

    whitelist=[]
    with open(filepathname, 'r',encoding='UTF-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or not row[0]:
                continue
            else:
                if row[0].strip()!="":
                    whitelist.append(getParserValue(row[0].strip()))#防注入

    # 权限判断
    # if g.current_user.super==1:#超级管理员
    #     for id in ids:
    #         # 先批量删
    #         VenueService.deleteWhiteList("",tagID,id)
    #         # 再批量增
    #         VenueService.updateWhiteList("",tagID,id,whitelist)
    # else:#场所管理员
    #     for id in ids:
    #         # 先批量删
    #         VenueService.deleteWhiteList(g.current_user.no,tagID,id)
    #         # 再批量增
    #         VenueService.updateWhiteList(g.current_user.no,id,tagID,whitelist)

    timestamp=int(round(time.time()))
    tag = {
        "id": timestamp,
        "tag": tag_name,
        "active": 1,
    }

    # 权限判断
    if g.current_user.super==1:#超级管理员
        for id in ids:
            VenueService.updateWhiteList("",tag,id,whitelist)
    else:#场所管理员
        for id in ids:
            VenueService.updateWhiteList(g.current_user.no,tag,id,whitelist)

    resp["data"] = {
        "tagID":timestamp
    }
    return jsonify(resp)



@route_venue.route("/uploadBatchAdminlist", methods=["POST"])
def uploadBatchAdminlist():
    resp = {"code": 200, "msg": "success", "data": {}}

    # tag_name = request.values["tag_name"] if 'tag_name' in request.values else ""
    ids = request.values["venue_ids"] if "venue_ids" in request.values else None
    file = request.files["file"] if "file" in request.files else None

    ids = ids.split(",")

    if not ids:
        resp["code"] = -1
        resp["msg"] = "请选择场所"
        return jsonify(resp)

    # if not tag_name:
    #     resp["code"] = -1
    #     resp["msg"] = "请输入批次名"
    #     return jsonify(resp)

    if not file:
        resp["code"] = -1
        resp["msg"] = "请选择文件"
        return jsonify(resp)

    # 保存文件
    config_upload = app.config["UPLOAD"]
    # filename = secure_filename(file.filename)
    filename = file.filename

    ext = filename.rsplit(".", 1)[1]  # 后缀名
    if ext not in config_upload["ext"]:
        resp["code"] = -1
        resp["msg"] = "文件类型错误"
        return jsonify(resp)

    root_path = app.root_path + config_upload["adminlist_prefix_path"]
    file_dir = getCurrentDate("%Y%m%d")
    save_dir = root_path + file_dir
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
        os.chmod(save_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IRWXO)

    file_name = str(uuid.uuid4()).replace("-", "") + "." + ext
    filepathname = "{0}/{1}".format(save_dir, file_name)
    file.save(filepathname)

    adminlist = []
    with open(filepathname, 'r', encoding='UTF-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or not row[0]:
                continue
            else:
                if row[0].strip() != "":
                    adminlist.append(getParserValue(row[0].strip()))  # 防注入

    timestamp = int(round(time.time()))
    tag = {
        "id": timestamp,
        # "tag": tag_name,
        "active": 1,
    }
    for id in ids:
        VenueService.updateAdminList(id, adminlist)
    # 权限判断
    # if g.current_user.super == 1:  # 超级管理员
    #     for id in ids:
    #         VenueService.updateAdminList(id, adminlist)
    # else:  # 场所管理员
    #     for id in ids:
    #         VenueService.updateAdminList(id, adminlist)########################################################################################

    resp["data"] = {
        "tagID": timestamp
    }
    return jsonify(resp)



@route_venue.route("/addWhiteNo", methods=["POST"])
def addWhiteNo():
    resp = {"code": 200, "msg": "success", "data": {}}

    tagID = int(request.values["tagID"]) if 'tagID' in request.values else 0
    id = request.values["venue_id"] if "venue_id" in request.values else None
    no = request.values["no"] if "no" in request.values else None
    
    if not id:
        resp["code"] = -1
        resp["msg"] = "请选择场所"
        return jsonify(resp)

    if not no:
        resp["code"] = -1
        resp["msg"] = "请输入学工号"
        return jsonify(resp)

    #根据id获取tag,若不存在提示先添加版本
    tag=VenueService.getWhiteListTag(tagID,id)
    if not tag:
        resp["code"] = -1
        resp["msg"] = "请选择白名单版本"
        return jsonify(resp)

    whitelist=[]
    if(no.strip()!=""):
        whitelist.append(getParserValue(no.strip()))

    # 权限判断
    if g.current_user.super==1:#超级管理员
        VenueService.updateWhiteList("",tag,id,whitelist)
    else:
        VenueService.updateWhiteList(g.current_user.no,tag,id,whitelist)
    return jsonify(resp)
    


@route_venue.route("/deleteWhiteNo", methods=["POST"])
def deleteWhiteNo():
    resp = {"code": 200, "msg": "success", "data": {}}

    tagID = int(request.values["tagID"]) if 'tagID' in request.values else 0
    id = request.values["venue_id"] if "venue_id" in request.values else None
    no = request.values["no"] if "no" in request.values else None
    
    if not id:
        resp["code"] = -1
        resp["msg"] = "请选择场所"
        return jsonify(resp)

    if not no:
        resp["code"] = -1
        resp["msg"] = "请选择人员"
        return jsonify(resp)

    # 权限判断
    if g.current_user.super==1:#超级管理员
        VenueService.deleteWhiteNo("",tagID,id,no)
    else:
        VenueService.deleteWhiteNo(g.current_user.no,tagID,id,no)

    return jsonify(resp)





@route_venue.route("/getAdminList", methods=["POST"])
def getAdminList():

    resp_data = {"code": 200, "msg": "操作成功", "data": {}}

    # 权限判断
    if g.current_user.super!=1:#超级管理员权限
        resp_data["code"] = -1
        resp_data["msg"] = "无权限"
        return jsonify(resp_data)


    req = request.values
    id = req["id"] if 'id' in req else ''
    dept = req["dept"] if 'dept' in req else ''
    no = req["no"] if 'no' in req else ''
    name = req["name"] if 'name' in req else ''
    page = int(req["p"]) if ("p" in req and req["p"]) else 1

    totalCount,adminList = VenueService.getAdminList(id,dept,no,name,page,app.config["PAGE_SIZE"])

    page_params = {
        "total": totalCount,
        "page_size": app.config["PAGE_SIZE"],
        "page_num": page,
        "display": app.config["PAGE_DISPLAY"],
    }

    pages = iPagination(page_params)
    
    resp_data["list"] = adminList
    resp_data["pages"] = pages

    return jsonify(resp_data)


@route_venue.route("/uploadAdminlist", methods=["POST"])
def uploadAdminlist():
    resp = {"code": 200, "msg": "success", "data": {}}

    # 权限判断
    if g.current_user.super!=1:#超级管理员权限
        resp["code"] = -1
        resp["msg"] = "无权限"
        return jsonify(resp)


    id = request.values["venue_id"] if "venue_id" in request.values else None
    file = request.files["file"] if "file" in request.files else None
    
    if not id:
        resp["code"] = -1
        resp["msg"] = "请选择场所"
        return jsonify(resp)

    if not file:
        resp["code"] = -1
        resp["msg"] = "请选择文件"
        return jsonify(resp)


    # 保存文件
    config_upload = app.config["UPLOAD"]
    # filename = secure_filename(file.filename)
    filename = file.filename

    ext = filename.rsplit(".", 1)[1] #后缀名
    if ext not in config_upload["ext"]:
        resp["code"] = -1
        resp["msg"] = "文件类型错误"
        jsonify(resp)

    root_path = app.root_path + config_upload["adminlist_prefix_path"]
    file_dir = getCurrentDate("%Y%m%d")
    save_dir = root_path + file_dir
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
        os.chmod(save_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IRWXO)

    file_name = str(uuid.uuid4()).replace("-", "") + "." + ext
    filepathname="{0}/{1}".format(save_dir, file_name)
    file.save(filepathname)


    adminlist=[]
    with open(filepathname, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or not row[0]:
                continue
            else:
                if(row[0].strip()!=""):
                    adminlist.append(getParserValue(row[0].strip()))

    # 先批量删
    VenueService.deleteAdminList(id)
    # 再批量增
    VenueService.updateAdminList(id,adminlist)
    
    return jsonify(resp)


@route_venue.route("/addAdminNo", methods=["POST"])
def addAdminNo():
    resp = {"code": 200, "msg": "success", "data": {}}

    # 权限判断
    if g.current_user.super!=1:#超级管理员权限
        resp["code"] = -1
        resp["msg"] = "无权限"
        return jsonify(resp)

    id = request.values["venue_id"] if "venue_id" in request.values else None
    no = request.values["no"] if "no" in request.values else None
    
    if not id:
        resp["code"] = -1
        resp["msg"] = "请选择场所"
        return jsonify(resp)

    if not no:
        resp["code"] = -1
        resp["msg"] = "请输入学工号"
        return jsonify(resp)


    adminlist=[]
    if no.strip()!="":
        adminlist.append(getParserValue(no.strip()))

    VenueService.updateAdminList(id,adminlist)
    
    return jsonify(resp)


@route_venue.route("/deleteAdminNo", methods=["POST"])
def deleteAdminNo():
    resp = {"code": 200, "msg": "success", "data": {}}

    # 权限判断
    if g.current_user.super!=1:#超级管理员权限
        resp["code"] = -1
        resp["msg"] = "无权限"
        return jsonify(resp)

    id = request.values["venue_id"] if "venue_id" in request.values else None
    no = request.values["no"] if "no" in request.values else None
    
    if not id:
        resp["code"] = -1
        resp["msg"] = "请选择场所"
        return jsonify(resp)

    if not no:
        resp["code"] = -1
        resp["msg"] = "请选择人员"
        return jsonify(resp)

    VenueService.deleteAdminNo(id,no)
    
    return jsonify(resp)


