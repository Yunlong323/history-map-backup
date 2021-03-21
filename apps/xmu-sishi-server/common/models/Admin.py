#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Admin:
    def __init__(self, admin):
        self.no= admin['no']
        self.name= admin['name']
        self.dept= admin['dept']
        self.super= admin['super']
        self.status= admin['status']
        self.token= admin['token']
        self.expiretime= admin['expiretime']