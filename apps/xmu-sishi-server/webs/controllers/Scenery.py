import datetime
from flask import Blueprint, request, jsonify, make_response, redirect, g,render_template
import time
from common.libs.SceneryService import SceneryService
from common.libs.Helper import ops_render, iPagination,createWXcode,getFormatDate,getCurrentDate,getParserValue
from werkzeug.utils import secure_filename
import os
import stat
import uuid
import csv

route_scenery = Blueprint('scenery_page', __name__)

@route_scenery.route("/post_scenery_info",methods=['POST'])#上传一个景点的信息
def post_scenery_info():
    print()
    resp = {"code": 200, "msg": 1, "data": {}}
    req = request.values
    # file = request.files["file"] if "file" in request.files else None  # 要上传的目的文件
    label_list = req["label_list"] if "label_list" in req else None
    name = req["name"] if "name" in req else None
    cloud = req["cloud"] if "cloud" in req else None
    score = req["score"] if "score" in req else None
    open_time = req["open_time"] if "open_time" in req else None
    must_know = req["must_know"] if "must_know" in req else None
    intro_text = req["intro_text"] if "intro_text" in req else None
    intro_audio = req["intro_audio"] if "intro_audio" in req else None
    intro_video = req["intro_video"] if "intro_video" in req else None
    print("1", req)
    print("2", label_list, name, cloud, score, open_time, must_know, intro_text, intro_audio, intro_video)
    #先获取属性，再判空
    if not label_list:
        resp["code"] = -1
        resp["msg"] = "请输入景点标签列表信息"
        return jsonify(resp)
    if not name:
        resp["code"] = -1
        resp["msg"] = "请输入景点名称信息"
        return jsonify(resp)
    if not cloud:
        resp["code"] = -1
        resp["msg"] = "请输入景点热度信息"
        return jsonify(resp)
    if not score:
        resp["code"] = -1
        resp["msg"] = "请输入景点评分信息"
        return jsonify(resp)
    if not open_time:
        resp["code"] = -1
        resp["msg"] = "请输入景点开放时间信息"
        return jsonify(resp)
    if not must_know:
        resp["code"] = -1
        resp["msg"] = "请输入景点游客须知信息"
        return jsonify(resp)
    if not intro_text:
        resp["code"] = -1
        resp["msg"] = "请输入景点文本介绍信息"
        return jsonify(resp)
    if not intro_audio:
        resp["code"] = -1
        resp["msg"] = "请输入景点音频介绍信息"
        return jsonify(resp)
    if not intro_video:
        resp["code"] = -1
        resp["msg"] = "请输入景点视频介绍信息"
        return jsonify(resp)
    # if not file:
    #     resp["code"] = -1
    #     resp["msg"] = "请选择文件"
    #     return jsonify(resp)
    #  判空后，保存文件(此功能未做)




    # 转义
    timestamp = int(round(time.time()))
    id = timestamp
    # label_list = getParserValue(label_list)
    name = getParserValue(name)
    cloud = getParserValue(cloud)
    score = getParserValue(score)
    open_time = getParserValue(open_time)
    must_know = getParserValue(must_know)
    intro_text = getParserValue(intro_text)
    intro_audio = getParserValue(intro_audio)
    intro_video = getParserValue(intro_video)

    print("3", label_list, name, cloud, score, open_time, must_know, intro_text, intro_audio, intro_video)
    sign = SceneryService.create(id, label_list, name, cloud, score, open_time, must_know, intro_text, intro_audio, intro_video)
    if not sign:
        resp["code"] = -1
        resp["msg"] = "服务器创建失败"
        return jsonify(resp)
    return jsonify(resp)

@route_scenery.route("/delete_scenery_node",methods=['POST'])
def delete_scenery_node():  # 通过id来删除
    resp = {"code": 200, "msg": "删除景点操作成功", "data": {}}
    req = request.values
    print(req)
    del_scenery_id = req["id"] if "id" in req else None
    SceneryService.delete_scenery_node(del_scenery_id)
    return jsonify(resp)

    if not del_scenery_id:
        resp["code"] = -1
        resp["msg"] = "请正确提供景点的id值"
        return jsonify(resp)
@route_scenery.route("/display")
def display_sceneries():
    resp_data = {}
    venueList = SceneryService.display_sceneries()
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
