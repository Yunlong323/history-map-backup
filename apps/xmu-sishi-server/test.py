# -*- coding:utf-8 -*-
from flask import jsonify,g
from neo4j import GraphDatabase
from common.models.User import User
# from common.libs.UserService import UserService
# from common.libs.AdminService import AdminService

uri = "bolt://219.229.80.233:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "Mars@2018"))

class AdminService:


    @staticmethod
    def display_sceneries():
        db = driver.session()
        expression = "match(place:xmu:signable) return place"
        try:
            sceneries = db.run(expression)
            sceneries = list(sceneries)
            return sceneries
        except Exception as e:
            return e

    @staticmethod
    def create_node(label_list, id,point,visited):
        db = driver.session()
        # 将label_list中的各个元素变成:分隔的形式 譬如[Admin,Person,xmu]  变成Admin:Person:xmu
        label_string = ":".join(label_list)

        expression = "CREATE(admin"+":"+label_string+"{id:$id,point:$point,visited:$visited}"+")"
        try:
            results = db.run(expression,{"id":id,"point":point,"visited":visited})
            return 1

        except Exception as e:
            return None
#admin.create_scenery_node(["xmu","signable"],"厦门大学革命史展览馆","hot",8.5,"9:00-22:00","可以拍照不可以亵渎哦","介绍文本","音频超链接","视频超链接")

    @staticmethod
    def create_scenery_node(label_list, name, cloud, score, open_time, must_know, intro_text, intro_audio, intro_video):
        db = driver.session()
        label_string = ":".join(label_list)
        property_dict = {"name": name, "cloud": cloud, "score": score, "open_time": open_time, "must_know": must_know,
                         "intro_text": intro_text, "intro_audio": intro_audio, "intro_video": intro_video}

        expression = "CREATE(place" + ":" + label_string + '''{name:$name,cloud:$cloud,score:$score,open_time:$open_time,must_know:$must_know,intro_text:$intro_text,intro_audio:$intro_audio,intro_video:$intro_video}''' + ")"
        try:
            results = db.run(expression, property_dict)
            return 1  # 1代表成功

        except Exception as e:
            print(e)
            return None
    @staticmethod
    def delete_scenery_node(scenery_name):
        db = driver.session()
        expression = "MATCH (place:xmu:signable {name:$name}) DELETE place "
        try:
            db.run(expression,{"name":scenery_name})
            return "1"
        except Exception as e:
            return None
    @staticmethod
    def update_scenery_node(scenery_name,key,value):
        db = driver.session()
        expression = "MATCH(place:xmu:signable {name:$scenery_name}) SET place."+key+"="+value
        try:
            results = db.run(expression,{name:scenery_name})
            return "1" 
        except Exception as e:
            return None
        
    @staticmethod
    def search_scenery_node(scenery_name):
        db = driver.session()
        expression = "MATCH (place:xmu:signable {name:$name}) RETURN place"
        try:
            results = db.run(expression,{"name":scenery_name})
            return place 
        except Exception as e:
            return None


class UserService:

    @staticmethod
    def create_user_node(name, userid, tel, labels):
        # db = get_db()
        db = driver.session()
        property_dict = {"name": name, "userid": userid, "tel": tel, "labels": labels}
        expression = "CREATE(user" + ":" + "user" + '''
            {
                name:$name,
                userid:$userid,
                tel:$tel,
                labels:$labels
            }
        ''' + ")"
        try:
            results = db.run(expression, property_dict)
            return 1  # 1代表成功
        except Exception as e:
            # return e
            return None

    @staticmethod
    def search_user_node(tel):
        # db = get_db()
        db = driver.session()
        tel = str(tel)
        expression = "match(node:user)where node.tel=\'"+tel+"\' return node "
        result = db.run(expression)
        userList = []
        for record in result:
            temp = User(record['node'])
            if temp:  # 如果查找到了，直接返回python化后的neo4j结点
                return temp
            else:
                return None


admin = AdminService()
# user = UserService()
# a = user.search_user_node("13906040102")
#
# print(a.name)
admin.create_scenery_node(["xmu","signable"],"涉台文物古迹","hot",8.5,"8:00-22:00","可以拍照",'''
厦门大学革命史展览馆，位于厦门大学同安楼一楼，于2016年4月正式开馆。展馆设有六个展厅，分“八闽革命摇篮”、“坚持红旗不倒”、“抗日救亡基地”与“东南民主堡垒”四个单元，全面记录了从1921年至1950年厦门大学师生反抗外来侵略、拯救民族危机、加强党团建设的历史。
“无古不成今，观今宜鉴古。”重温与党同龄的厦门大学自强不息的革命岁月，让我们更加坚定传承红色基因、弘扬革命精神，进一步为实现厦门大学“两个百年”奋斗目标和实现中华民族伟大复兴的中国梦注入了强大的精神动力。
2020年12月1日，厦门大学革命史展览馆“全国关心下一代党史国史教育基地”顺利揭牌，有力推进了青年学生党史国史教育这一项基础工程。立于厦大“新百年”的潮头，革命史馆将继续集聚历史能量，发挥教育效用，成为广大青年学生补足“精神之钙”、点亮“信仰之灯”、铸牢“信念之魂”的红色“聚宝盆”。
''',"暂无","暂无")