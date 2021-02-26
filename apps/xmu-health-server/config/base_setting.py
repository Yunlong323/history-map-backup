#!/usr/bin/env python
# -*- coding: utf-8 -*-
SERVER_PORT = 9000
# DEBUG = False
DEBUG = True

#使用CDN加速静态资源
CDN = True

SALT = "46nourJfj2f44534341D"

AUTH_COOKIE_NAME = "xmu_health"

# 过滤 url,以下URL不经过权限判断
IGNORE_URLS = [

    #外部操作用户state
    "^/api/setPersonState",
    "^/api/getPersonState",
    "^/api/addCardTrack",
    "^/api/getScanRecord",
    "^/api/setLeader",#设置领导
    "^/api/getLeader",#获取领导

    # 静态资源
    "^/static",
    "^/favicon.ico",

    # 后台管理员
    "^/admin/login",
    "^/admin/callback",

    # 微信小程序用户
    "^/wechat/getAllPlace",#待删除
    "^/wechat/callback",
    "^/wechat/login"
]


PAGE_SIZE = 100
PAGE_DISPLAY = 10

UPLOAD = {
    "ext": ["txt", "TXT"],#["jpg", "gif", "bmp", "jpeg", "png"],
    # "prefix_path": "/webs/static/upload/",
    # "prefix_url": "/static/upload/"
    "whitelist_prefix_path": "/files/whitelist/",
    "adminlist_prefix_path": "/files/adminlist/",
    "wxcode_prefix_path": "/webs/static/images/WXcode/",
    "wxcode_prefix_url": "/static/images/WXcode/"
}

APP = {
    "domain": "http://127.0.0.1:9000"
}

NEO4J = {
<<<<<<< HEAD
    "address": "bolt://219.229.80.233:7687",
=======
    "address": "bolt://localhost",
>>>>>>> 21adb85b8062d7d1796db3cc9b25822099f247d4
    "username": "neo4j",
    "password": "Mars@2018"
}


WECHAT={
<<<<<<< HEAD
    "APPID": "wxc136b7f8bc1430ff",
=======
    "APPID": "wxxxxx",
>>>>>>> 21adb85b8062d7d1796db3cc9b25822099f247d4
    "APPKEY": "d6xxxxxxxxx"
}


TOKEN="DKp5UpBSfAsP1eRSQ5WMbFeYbyourDKuOxoAAOmhPQ"




ALLOWED_IP = [
    "127.0.0.1",
    "210.34.218.170",
    "121.192.190.97",
    "211.97.104.44",#my福州
    "172.18.61.130",#my厦门vpn
    "10.30.161.217"
]


FILESERVER = {
    "ip":"172.27.65.191",
    "port":22,
    "username":"WXcode",
    "password":"Ltevsa@173#qw",
    "path":"/home/WXcode/passport_file/WXcode/"
}

