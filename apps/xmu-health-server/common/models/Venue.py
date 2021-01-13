#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Venue():
    def __init__(self, venue):
        self.id= venue['id']
        self.name= venue['name']
        self.lat= venue['lat']
        self.lon= venue['lon']
        self.status= venue['status']
        self.permissionType= venue['permissionType']
        self.createtime= venue['createtime']

