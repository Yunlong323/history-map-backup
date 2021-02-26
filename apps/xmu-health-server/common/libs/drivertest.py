from neo4j import GraphDatabase
from flask import jsonify
driver = GraphDatabase.driver("bolt://219.229.80.233:7687",auth=("neo4j","Mars@2018"))

class Service:
    @staticmethod
    def delete_scenery_node(scenery_name):
        db = driver.session()
        expression = "match (place:xmu:signable {name:$name}) delete place "
        try:
            db.run(expression,{"name":scenery_name})
            return jsonify(msg="1")
        except Exception as e:
            return None

    @staticmethod
    def create_scenery_node(label_list,name,cloud,score,open_time,must_know,intro_text,intro_audio,intro_video):
        db = driver.session()
        label_string = ":".join(label_list)
        #property_dict = {"name":name,"cloud":cloud,"score":score,"open_time":open_time,"must_know":must_know,"intro_text":intro_text,"intro_audio":intro_audio,"intro_video":intro_video}

        expression = "CREATE(place"+":"+label_string+'''
            {
                name:$name,
                cloud:$cloud,
                score: $score,
                open_time:8:$open_time,
                must_know:$must_know,
                intro_text:$intro_text,
                intro_audio:$intro_audio,
                intro_video:$intro_video
            }
        '''+")"  
        try:
            results = db.run(expression,{"name":name,"cloud":cloud,"score":score,"open_time":open_time,"must_know":must_know,"intro_text":intro_text,"intro_audio":intro_audio,"intro_video":intro_video})
            return jsonify(msg="1") #1代表成功

        except Exception as e:
            print("出错")
            return jsonify(msg=e)

    @staticmethod
    def display_sceneries():
        db = driver.session()
        expression = "match(place:xmu:signable) return place"
        try:
            sceneries = db.run(expression)
            return sceneries
        except Exception as e:
            return e

Service.create_scenery_node(["xmu","signable"],"厦门大学革命史展览馆","hot",8.5,"9:00-22:00","可以拍照不可以亵渎哦","介绍文本","音频超链接","视频超链接")
print("创建成功")
