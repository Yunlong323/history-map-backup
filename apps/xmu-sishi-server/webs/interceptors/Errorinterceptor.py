#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application import app
from common.libs.Helper import ops_render

@app.errorhandler(404)
def error_404(e):
    return ops_render("error/error.html", {"status": 404, "msg": "很抱歉！您访问的页面不存在"})
