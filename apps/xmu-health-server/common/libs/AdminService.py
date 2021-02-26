<<<<<<< HEAD
 #!/usr/bin/env python
=======
#!/usr/bin/env python
>>>>>>> 21adb85b8062d7d1796db3cc9b25822099f247d4
# -*- coding: utf-8 -*-
from application import get_db
from common.models.Admin import Admin
import hashlib
import base64
import random
import string


class AdminService:
<<<<<<< HEAD
    @staticmethod
    def display_sceneries():
        db = get_db()
        expression = "match(place:xmu:signable) return place"
        try:
            sceneries = db.run(expression)
            return list(sceneries) #把查找到的对象结点全部转化为列表
        except Exception as e:
            return e
    @staticmethod
    def delete_scenery_node(scenery_name):
        db = get_db()
        expression = "match (place:xmu:signable {name:$name}) delete place "
        try:
            db.run(expression,{"name":scenery_name})
            return 1
        except Exception as e:
            return None


    @staticmethod
    def create_scenery_node(label_list,name,cloud,score,open_time,must_know,intro_text,intro_audio,intro_video):
        db = get_db()
        label_string = ":".join(label_list)
        property_dict = {"name":name,"cloud":cloud,"score":score,"open_time":open_time,"must_know":must_know,"intro_text":intro_text,"intro_audio":intro_audio,"intro_video":intro_video}

        expression = "CREATE(place"+":"+label_string+'''
            {
                name:$name,
                cloud:$cloud,
                score:$score,
                open_time:$open_time,
                must_know:$must_know,
                intro_text:$intro_text,
                intro_audio:$intro_audio,
                intro_video:$intro_video
            }
        '''+")"  
        try:
            results = db.run(expression,property_dict)
            return 1 #1代表成功

        except Exception as e:
            return None
=======
>>>>>>> 21adb85b8062d7d1796db3cc9b25822099f247d4

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
<<<<<<< HEAD

    # @staticmethod
    # def create_user_node(label_list,property_dict):
    #     db = get_db()
    #     # 将label_list中的各个元素变成:分隔的形式 譬如[Admin,Person,xmu]  变成Admin:Person:xmu
    #     label_string = ":".join(label_list)

    #     expression = "CREATE("+"user:"+label_string+"{id:$id,point:$point,visited:$visited}"+")"  #visited作为一个list传入，打卡地点
        
    #     try:
    #         # results = db.run(expression,{"id":id,"point":point,"visited":visited})
    #         results = db.run(expression,property_dict)
    #         return jsonify(msg="用户结点创建成功")

    #     except Exception as e:
    #         db.rollback()
    #         return jsonify(msg=e)
    
=======
>>>>>>> 21adb85b8062d7d1796db3cc9b25822099f247d4
