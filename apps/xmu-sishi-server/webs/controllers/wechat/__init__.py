#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from common.libs.Helper import ops_render

route_wechat = Blueprint("wechat_page", __name__)
from webs.controllers.wechat.User import *
from webs.controllers.wechat.callback import *

@route_wechat.route("/")
def index():
    return ops_render("error/error.html", {"status": 404, "msg": "很抱歉！您访问的页面不存在"})