#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application import app

"""
统计拦截器
"""
from webs.interceptors.Authinterceptor import *
from webs.interceptors.Errorinterceptor import *

"""
蓝图功能，对所有的 url 进行蓝图功能配置
"""

from webs.controllers.wechat import route_wechat
from webs.controllers.Admin import route_admin
from webs.controllers.User import route_user
from webs.controllers.Venue import route_venue
from webs.controllers.index import route_index
from webs.controllers.Track import route_track
from webs.controllers.Trace import route_trace
from webs.controllers.Business import route_business
# from webs.controllers.API import route_api

app.register_blueprint(route_wechat, url_prefix="/wechat")
app.register_blueprint(route_admin, url_prefix="/api/admin")
app.register_blueprint(route_user, url_prefix="/user")
app.register_blueprint(route_venue, url_prefix="/venue")
app.register_blueprint(route_index, url_prefix="/")
app.register_blueprint(route_track, url_prefix="/track")
app.register_blueprint(route_trace, url_prefix="/trace")
app.register_blueprint(route_business, url_prefix="/business")
# app.register_blueprint(route_api, url_prefix="/api")



# from webs.controllers.wechat import route_wechat
# from webs.controllers.Admin import route_admin
# from webs.controllers.User import route_user
# from webs.controllers.Venue import route_venue
# from webs.controllers.index import route_index
# from webs.controllers.Track import route_track
# from webs.controllers.API import route_api

# app.register_blueprint(route_wechat, url_prefix="/wechat")
# app.register_blueprint(route_admin, url_prefix="/admin/admin")
# app.register_blueprint(route_user, url_prefix="/admin/user")
# app.register_blueprint(route_venue, url_prefix="/admin/venue")
# app.register_blueprint(route_index, url_prefix="/admin/index")
# app.register_blueprint(route_track, url_prefix="/admin/track")
# app.register_blueprint(route_api, url_prefix="/api")




from webs.controllers.static import route_static
app.register_blueprint(route_static, url_prefix="/static")