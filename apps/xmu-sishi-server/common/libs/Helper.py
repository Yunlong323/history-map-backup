#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import g, render_template
import datetime
from application import app, get_db
import json
import requests
import os
import stat
# import paramiko

# 安全
from html.parser import HTMLParser

def iPagination(params):
    """
    自定义分页类
    """
    import math

    ret = {
        "is_prev": 1,
        "is_next": 1,
        "from": 0,
        "end": 0,
        "current": 0,
        "total_pages": 0,
        "page_size": 0,
        "total": 0,
    }

    total = int(params['total'])
    page_size = int(params['page_size'])
    page_num = int(params['page_num'])
    display = int(params['display'])
    total_pages = int(math.ceil(total / page_size))
    total_pages = total_pages if total_pages > 0 else 1
    if page_num <= 1:
        ret['is_prev'] = 0

    if page_num >= total_pages:
        ret['is_next'] = 0

    semi = int(math.ceil(display / 2))

    if page_num - semi > 0:
        ret['from'] = page_num - semi
    else:
        ret['from'] = 1

    if page_num + semi <= total_pages:
        ret['end'] = page_num + semi
    else:
        ret['end'] = total_pages

    ret['current'] = page_num
    ret['total_pages'] = total_pages
    ret['page_size'] = page_size
    ret['total'] = total
    return ret


def iPaginationForAPI(params):
    """
    API分页类
    """
    import math

    ret = {
        "is_prev": 1,
        "is_next": 1,
        "current": 0,
        "total_pages": 0,
        "page_size": 0,
        "total": 0,
    }

    total = int(params['total'])
    page_size = int(params['page_size'])
    page_num = int(params['page_num'])

    total_pages = int(math.ceil(total / page_size))
    total_pages = total_pages if total_pages > 0 else 1
    if page_num <= 1:
        ret['is_prev'] = 0

    if page_num >= total_pages:
        ret['is_next'] = 0

    ret['current'] = page_num
    ret['total_pages'] = total_pages
    ret['page_size'] = page_size
    ret['total'] = total
    return ret




def ops_render(template, context={}):
    """
    统一渲染方法
    """
    if "current_user" in g:
        context["current_user"] = g.current_user

    return render_template(template, **context)


class StripTagsHTMLParser(HTMLParser):
    data = ""
    def handle_data(self, data):
        self.data += data
    
    def getData(self):
        return self.data


def getParserValue(data):
    parser = StripTagsHTMLParser()
    parser.feed(data)
    data = parser.getData()

    charList=['|','&',';','$','%','@','\'','"','<>','()','+','CR','LF',',','script','document','eval','','',]
    for char in charList:
        data = data.replace(char, "");

    return data


def getCurrentDate(format="%Y-%m-%d %H:%M:%S"):
    """
    获取当前时间
    """
    return datetime.datetime.now().strftime(format)

'''
获取当前格式化的时间
'''
def getFormatDate( date = None ,format = "%Y-%m-%d %H:%M:%S" ):
    if date is None:
        date = datetime.datetime.now()

    return date.strftime( format )

# 生成小程序码
def createWXcode(venueID):
    WXcodeUrl=''
    data = {"scene": venueID}
    data = json.dumps(data).encode(encoding='utf-8')
    # header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    #                "Content-Type": "application/json"}
    db = get_db()
    results = db.run("match (n:CONFIG)"
                    "return n.ACCESS_TOKEN as ACCESS_TOKEN")
    ACCESS_TOKEN = results.data()[0]["ACCESS_TOKEN"]

    url = 'https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token=' + ACCESS_TOKEN
    res = requests.post(url=url, data=data)# headers=header_dict
    # print(res.text)
    if "42001" in res.text:
        print("token过期了")

        getTokenurl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="+app.config['WECHAT']["APPID"]+"&secret="+app.config['WECHAT']["APPKEY"]
        res = requests.get(url=getTokenurl)# headers=header_dict
        jsondata = json.loads(res.text)

        db.run("match (n:CONFIG)"
               f"set n.ACCESS_TOKEN='{jsondata['access_token']}'")

        url = 'https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token=' + jsondata['access_token']
        res = requests.post(url=url, data=data)

    try:
        imgdata=res.content

        save_dir = app.root_path + app.config["UPLOAD"]["wxcode_prefix_path"]
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
            os.chmod(save_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IRWXO)


        filename = "%s.jpeg" % venueID
        file = open(os.path.join(save_dir, filename), 'wb')
        file.write(imgdata)


        # 将二维码图片传至统一的文件服务器上 用于分布式环境
        # transport = paramiko.Transport((app.config.get("FILESERVER")["ip"],app.config.get("FILESERVER")["port"]))  # 获取Transport实例
        # transport.connect(username=app.config.get("FILESERVER")["username"], password=app.config.get("FILESERVER")["password"])  # 建立s连接
        # # 创建sftp对象，SFTPClient是定义怎么传输文件、怎么交互文件
        # sftp = paramiko.SFTPClient.from_transport(transport)
        # # 将本地 api.py 上传至服务器  。文件上传并重命名为
        # sftp.put(os.path.join(save_dir, filename),app.config.get("FILESERVER")["path"]+filename)
        # # 关闭连接
        # transport.close()

        file.close()

        WXcodeUrl=app.config["UPLOAD"]["wxcode_prefix_url"]+filename

    except Exception as e:
        print("图片异常了"+str(e))
        WXcodeUrl=None

    return WXcodeUrl



# 获取微信统计信息
def getWXStatistics():
    
    WXdata=[]
    data = {"begin_date": '20200601',"end_date" : "20200601"}
    data = json.dumps(data).encode(encoding='utf-8')

    db = get_db()
    results = db.run("match (n:CONFIG)"
                    "return n.ACCESS_TOKEN as ACCESS_TOKEN")
    ACCESS_TOKEN = results.data()[0]["ACCESS_TOKEN"]

    url = 'https://api.weixin.qq.com/datacube/getweanalysisappiddailyvisittrend?access_token=' + ACCESS_TOKEN
    res = requests.post(url=url, data=data)# headers=header_dict

    if "42001" in res.text:
        print("token过期了")

        getTokenurl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="+app.config['WECHAT']["APPID"]+"&secret="+app.config['WECHAT']["APPKEY"]
        res = requests.get(url=getTokenurl)# headers=header_dict
        jsondata = json.loads(res.text)

        db.run("match (n:CONFIG)"
               f"set n.ACCESS_TOKEN='{jsondata['access_token']}'")

        ACCESS_TOKEN = jsondata['access_token']
        
    try:
        # print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        now = datetime.datetime.now()
        for i in range(11,1,-1):#[1,30]天 10天 30天要10秒左右
            date = (now + datetime.timedelta(days=-i)).strftime('%Y%m%d')

            data = {"begin_date": date,"end_date" : date}
            data = json.dumps(data).encode(encoding='utf-8')
            url = 'https://api.weixin.qq.com/datacube/getweanalysisappiddailyvisittrend?access_token=' + ACCESS_TOKEN
            res = requests.post(url=url, data=data)# headers=header_dict

            WXdata.append([date,res.content])

    except Exception as e:
        print("异常了"+str(e))
        WXdata=None

    return WXdata