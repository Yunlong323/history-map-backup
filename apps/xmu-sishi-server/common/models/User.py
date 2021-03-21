#!/usr/bin/env python
# -*- coding: utf-8 -*-

class User():
    def __init__(self, user=None,labels=None):
        self.no= user['no']
        self.name= user['name']
        self.dept= user['dept']
        self.userid= user['userid']
        self.state= user['state']
        self.leader= user['leader']

        self.usertype= 0 #1学生 2教师 3校内员工
        
        self.labels = labels #ADMIN REVIEWER STAFF STUDENT TEACHER USER