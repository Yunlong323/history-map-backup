
# -*- coding: utf-8 -*-
from flask import jsonify
from neo4j.v1 import GraphDatabase
uri = "bolt://219.229.80.233:7687"         #表示我们的driver指向哪个数据库地址
driver = GraphDatabase.driver(uri, auth=("neo4j", "Mars@2018")) #创建驱动对象，去帮python到数据库执行neo4j语句

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
    def create_scenery_node(label_list, name, cloud, score, open_time, must_know, intro_text, intro_audio, intro_video):
        db = driver.session()
        label_string = ":".join(label_list)
        property_dict = {"name": name, "cloud": cloud, "score": score, "open_time": open_time, "must_know": must_know,
                         "intro_text": intro_text, "intro_audio": intro_audio, "intro_video": intro_video}

        expression = "CREATE(place" + ":" + label_string + '''{name:$name,cloud:$cloud,score:$score,open_time:$open_time,must_know:$must_know,intro_text:$intro_text,intro_audio:$intro_audio,intro_video:$intro_video}''' + ")"
        try:
            results = db.run(expression, property_dict)
            return "1" # 1代表成功

        except Exception as e:
            print(e)
            return None

    @staticmethod
    def create_user_node(label_list,property_dict):
        db = driver.session()
        # 将label_list中的各个元素变成:分隔的形式 譬如[Admin,Person,xmu]  变成Admin:Person:xmu
        label_string = ":".join(label_list)
        #问题：不能把节点名，标签名，属性名都作为变量传入到语句中吗？
        #答：可以用python的str连接成一句Cypher表达式，只对属性用json传参
        expression = "CREATE("+"user"+":"+label_string+"{id:$id,point:$point,visited:$visited}"+")" #把传入参数连接成一句cypher语句，这个语句就存入expression变量
        #print(expression)
        try:
            results = db.run(expression,property_dict) #驱动运行expression，参数是键值对property_dict    例如{"id":"001","point":0,"visited":[]}  键必须是string
            return "1" 

        except:
            return None
    @staticmethod
    def search_user_node(o_name):
        db = driver.session()
        expression="MATCH("+"p:xmu"+"{name:o_name}"+")"+"RETURN"+"p.id"
        try:
            results = db.run(expression) 
            return "1"

        except:
            return None
    @staticmethod
    def delete_user_node(o_name):
        db = driver.session()
        expression="MATCH("+"p:xmu"+"{name:o_name}"+")"+"DELETE"+"p"
        try:
            results = db.run(expression) 
            return "1"

        except:
            return None
    @staticmethod
    def change_user_node(o_name,o_lable,o_property):
        db = driver.session()
        expression="MATCH("+"p:xmu"+"{name:o_name}"+")"+"SET"+"p."+o_lable+"="+o_property
        try:
            results = db.run(expression) 
            return "1"

        except:
            return None
admin = AdminService()
#(label_list, name, cloud, score, open_time, must_know, intro_text, intro_audio, intro_video):
admin.create_scenery_node(["xmu","signable"],"涉台文物古迹","hot",8.5,"8:00-22:00","可以拍照",'''涉台文物古迹位于成智楼前，是刻有建盖大小担山寨城碑记的石碑，始建于清代。碑为花岗岩，下有梯形底座，碑身周边刻有云鹤仙子，花叶卷浪等浮雕纹饰石碑上。碑文记叙了起义军攻袭大小担清军防地及尔后为加强防务由厦门行商捐款建盖大小担山寨城的经过，为研究蔡牵起义和台湾历史提供了珍贵实物资料。
建盖大小担山寨城碑记反映了清代大陆和台湾之间的交流交往，体现了两岸同胞同宗同源的亲缘关系。厦门大学始终与台湾保持友好交流，1945年台湾光复后，厦大毕业生满腔热情赴台参与重建，两岸关系恢复后，台湾学生亦是将厦大作为台外求学首选。1980年，在厦大校园里，海内外第一个专门从事台湾研究的学术机构——厦大台湾研究所（后为厦大台湾研究院）成立。其开创了多个第一：招收了第一批硕士研究生，创办了第一份专门研究台湾问题的学术刊物，成立大陆第一个专门研究台湾的民间学术机构，充分发挥地域优势，加强了与台湾地区的学术交流。一届届厦大人成为两岸沟通合作的桥梁，为实现祖国统一和中华民族复兴，发光发热。
''',"暂无","暂无")