from flask import jsonify
from neo4j import GraphDatabase
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
            return 1 # 1代表成功

        except Exception as e:
            print(e)
            return None

admin = AdminService()
#admin.create_node(["Admin","Person","xmu"],3,0,"嘉庚像")
#admin = AdminService()
admin.create_scenery_node(["xmu","signable"],"厦门大学革命史展览馆","hot",8.5,"9:00-22:00","可以拍照不可以亵渎哦","介绍文本","音频超链接","视频超链接")
#问题：不能把节点名，标签名，属性名都作为变量传入到语句中吗
#可以用python的str连接成一句Cypher表达式，只对属性用json传参
admin.display_sceneries()
#AdminService.create_scenery_node(["xmu","signable"],"厦门大学革命史展览馆","hot",8.5,"9:00-22:00","可以拍照不可以亵渎哦","介绍文本","音频超链接","视频超链接")
print("创建成功")