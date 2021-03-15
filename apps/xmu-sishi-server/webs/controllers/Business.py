# -*- coding: utf-8 -*-
from flask import Blueprint, request,jsonify,g
from common.libs.Helper import ops_render, iPagination,getFormatDate,getWXStatistics
from application import app
import datetime
import json

route_business = Blueprint('business_page', __name__)


@route_business.route("/index")
def index():
    return ops_render("business/index.html")


@route_business.route("/getStatistics")
def getStatistics():
    WXdata = getWXStatistics()
    data1=[]
    data2=[]
    data3=[]
    data4=[]
    print(WXdata)
    for date,t in WXdata:
        temp = json.loads(t)
        # print(temp['list'][0]['session_cnt'])#打开次数
        # print(temp['list'][0]['visit_uv'])
        # print(date)
        data1.append({ 'date': date, 'value': temp['list'][0]['session_cnt'] })#打开次数
        data2.append({ 'date': date, 'value': temp['list'][0]['visit_uv'] })#访问人数
        data3.append({ 'date': date, 'value': temp['list'][0]['stay_time_uv'] })#人均停留时长
        data4.append({ 'date': date, 'value': temp['list'][0]['stay_time_session'] })#次均停留时长

        

        # print(temp['list'][0]['stay_time_uv'])#人均停留时长
        # print(temp['list'][0]['stay_time_session'])#次均停留时长


    # print(data1)
    resp_data = {"code": 200, "msg": "操作成功", "data1": {},"data2": {},"data3": {},"data4": {}}
    

    # jsonData["results"]["data"]["graph"]["nodes"]=nodesList
    # jsonData={"results":[{"data":[{"graph":{"nodes":nodesList,"relationships":relationshipList}}]}]};
    
    # print(venue['venueid']+'==='+venue['venuename']+'==='+venue['time'])

    # jsonData={"results":[]};

    # data1= [
    #     { 'date': '200801', 'value': 5 },
    #     { 'date': '200901', 'value': 10 },
    #     { 'date': '201001', 'value': 8 },
    #     { 'date': '201101', 'value': 22 },
    #     { 'date': '201201', 'value': 8 },
    #     { 'date': '201401', 'value': 10 },
    #     { 'date': '201501', 'value': 5 }
    # ]

    resp_data["data1"] = data1
    resp_data["data2"] = data2
    resp_data["data3"] = data3
    resp_data["data4"] = data4
    return jsonify(resp_data)
