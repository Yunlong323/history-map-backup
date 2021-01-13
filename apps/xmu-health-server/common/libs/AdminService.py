#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application import get_db
from common.models.Admin import Admin
import hashlib
import base64
import random
import string


class AdminService:

    @staticmethod
    def getByNoWhenLogin(no):
        db = get_db()
        results = db.run("MATCH (user:USER:ADMIN {no:$no,status:1}) "
                 "RETURN user", {"no": no}
        )
        record = results.single()
        # 管理员不存在或status为禁用状态
        if not record:
            return None

        return ""

    @staticmethod
    def geneToken(length=16):
        keylist = [random.choice(string.ascii_letters + string.digits) for i in range(length)]
        return "".join(keylist)


    @staticmethod
    def updateUserInfo(data):
        if data['usertype']==1 :
            usertype='STUDENT'
        elif data['usertype']==2 :
            usertype='TEACHER'
        else:
            usertype='STAFF'

        db = get_db()
        result = db.run("MATCH (user:ADMIN {no:$no}) "
         "SET user:"+usertype+",user.name=$name,user.dept=$dept,user.token=$token,user.expiretime=$expiretime",
         {"no": data['no'],"name":data['name'],"dept":data['dept'],"token":data['token'],"expiretime":data['expiretime']}
         )

    @staticmethod
    def getByToken(token):
        db = get_db()
        results = db.run("MATCH (user:ADMIN {token:$token}) "
                 "RETURN user", {"token": token}
        )
        record = results.single();
        if not record: #if user_info.status != 1: return False
            return None

        admin=Admin(record['user'])
        return admin


    @staticmethod
    def updateToken(no,token):
        db = get_db()
        result = db.run("MATCH (user:ADMIN {no:$no}) "
                     "SET user.token=$token",
                     {"no": no,"token":token}
        )
