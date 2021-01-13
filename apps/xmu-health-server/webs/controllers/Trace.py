# -*- coding: utf-8 -*-
from flask import Blueprint, request,jsonify,g
from common.libs.Helper import ops_render, iPagination,getFormatDate
from application import app
from common.libs.TrackService import TrackService
import datetime

route_trace = Blueprint('trace_page', __name__)


@route_trace.route("/index")
def index():
    return ops_render("trace/index.html")

@route_trace.route("/getTrace", methods=["POST"])
def getTrace():
    resp_data = {"code": 200, "msg": "操作成功", "data": {}}
    req = request.values

    no = req["no"] if ("no" in req) else ""

    begintime = req['begintime'] if ('begintime' in req and req["begintime"]) else '0000-00-00'
    endtime = req['endtime'] if ('endtime' in req and req["endtime"]) else '9999-00-00'
    endtime = endtime+" 23:59:59"


    minute=3600000
    try:
        minute = int(req["minute"]) if ("minute" in req and req["minute"]) else 3600000
    except Exception as ex:
        resp_data["code"] = -1
        resp_data["msg"] = "请输入整数型的分钟数"
        return jsonify(resp_data)

    
    # time = req['time'] if ('time' in req and req["time"]) else '0000-00-00'
    # time = time+" 23:59:59"

    # date_array=time.split("-")
    # date_from=datetime.date(int(date_array[0]),int(date_array[1]),int(date_array[2]))
    # date_from = date_from + datetime.timedelta(days=-3)
    # date_from = getFormatDate(date=date_from)

    # date_to=time

    # 权限判断
    if g.current_user.super!=1:#超级管理员权限
        resp_data["code"] = -1
        resp_data["msg"] = "无权限"
        return jsonify(resp_data)



    # jsonData={"results":[{"data":[{"graph":{"nodes":[],"relationships":[]}}]}]};
    # print(date_from)
    # print(date_to)
    # venueList = TrackService.searchByNoTime(no,date_from,date_to)
    venueList = TrackService.searchByNoTime(no,begintime,endtime)
    relationshipList=[]

    nodesList=[]
    nodesList.append({
            "id": no,
            "labels": ["目标人员"],
            # "properties":{"姓名":"姓名","学工号":no},
            "properties":{"学工号":no},
        })


    for venue in venueList:
        nodesList.append({
            # "id": venue['venueid'],
            "id": venue['id'],
            "labels": ["场所"],
            "properties":{"名称":venue['venuename']},
        })

        if venue['id']=='1':
            relationshipList.append({
                "type": "去过",
                "startNode": no,
                "endNode": venue['id'],
                "properties": {
                    "时间": venue['time']
                }
            })
        else:
            relationshipList.append({
                "type": "接着去了",
                "startNode": str(int(venue['id'])-1),
                "endNode": venue['id'],
                "properties": {
                    "时间": venue['time']
                }
            })



        tmp_date=datetime.datetime.strptime(venue['time'],'%Y-%m-%d %H:%M:%S')
        tmp_date_from=tmp_date + datetime.timedelta(minutes=-minute)#minute分钟前
        tmp_date_to=tmp_date + datetime.timedelta(minutes=+minute)#minute分钟后

        tmp_date_from = getFormatDate(date=tmp_date_from)
        tmp_date_to = getFormatDate(date=tmp_date_to)

        # userList = TrackService.searchByVenueTime(venue['id'],date_from_venue,date_to_venue,no)
        userList = TrackService.searchByVenueTime(venue['venueid'],tmp_date_from,tmp_date_to,no)

        for user in userList:
            nodesList.append({
                # "id": venue['venueid'],
                "id": user['no'],
                "labels": ["人员"],
                "properties":{"学工号":user['no'],"姓名":user['name']},
            })

            relationshipList.append({
                "type": "去过",
                "startNode": user['no'],
                "endNode": venue['id'],
                "properties": {
                    "时间": user['time']
                }
            })



    # jsonData["results"]["data"]["graph"]["nodes"]=nodesList
    jsonData={"results":[{"data":[{"graph":{"nodes":nodesList,"relationships":relationshipList}}]}]};
    
    # print(venue['venueid']+'==='+venue['venuename']+'==='+venue['time'])

    

    


    
    # jsonData={"results":[]};



    resp_data["data"] = jsonData
    return jsonify(resp_data)
