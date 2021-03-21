 #!/usr/bin/env python
# -*- coding: utf-8 -*-
from application import get_db
from common.models.Admin import Admin
from common.models.Venue import Venue
import hashlib
import base64
import random
import string


class SceneryService:
    @staticmethod
    def getSceneryNodeInfo(id):  # 获取数据库里的景点结点即可，在User.py中对结点进行提取信息
        db = get_db()
        results = db.run("MATCH (place:xmu:signable) WHERE place.id=$id RETURN place",{"id":id} )
        venue_list = []
        for record in results:
            tmp = Venue(record["place"])#构造python景点对象
            # venue_list.append(tmp)
        return tmp

    @staticmethod
    def display_sceneries():
        db = get_db()
        # results = db.run("match (scenery:xmu:signable) return scenery")
        results = db.run("match (scenery:signable) return scenery")
        venueList = []
        for record in results:
            tmp = Venue(record['scenery'])  # 转化为python中的数据库Venue类
            venueList.append(tmp)
        return venueList
        # expression = "match(place:xmu:signable) return place"
        # try:
        #     sceneries = db.run(expression)
        #     return list(sceneries) #把查找到的对象结点全部转化为列表
        # except Exception as e:
        #     return e

    @staticmethod
    def delete_scenery_node(id):
        # db = get_db()
        # expression = "match (place:xmu:signable {id:$id}) delete place "
        # try:
        #     db.run(expression,{"id":id})
        #     return "1"
        # except Exception as e:
        #     return None
    #    print(id)
        db = get_db()
        # expression = "match (place:xmu:signable {id:$id}) delete place "
        expression = "match (scenery:signable {id:$id}) delete scenery "
        try:
            db.run(expression, {"id": id})
            return 1
        except Exception as e:
            return None


    @staticmethod
    def create(id, label_list, name, cloud, score, open_time, must_know, intro_text, intro_audio, intro_video,signable):
       # print(4, id, label_list, name, cloud, score, open_time, must_know, intro_text, intro_audio, intro_video,signable)
        try:
            db = get_db()
            #label_list = eval(label_list)
            label_string = ":".join(label_list)
            # expression = "CREATE(place"+":"+label_string+'''
            # {
            #     id:$id,
            #     name:$name,
            #     cloud:$cloud,
            #     score:$score,
            #     open_time:$open_time,
            #     must_know:$must_know,
            #     intro_text:$intro_text,
            #     intro_audio:$intro_audio,
            #     intro_video:$intro_video
            # }
            # '''+")"
            # label_list[0]标签干什么用？
            expression = f"CREATE(scenery:SCENERY:"+label_string+'''
            {
                id:$id,
                name:$name,
                cloud:$cloud,
                score:$score,
                open_time:$open_time,
                must_know:$must_know,
                intro_text:$intro_text,
                intro_audio:$intro_audio,
                intro_video:$intro_video,
                signable:$signable
            }
            '''+")"
            property_dict = {"id" :id ,"name" :name ,"cloud" :cloud ,"score" :score ,"open_time" :open_time
                             ,"must_know" :must_know ,"intro_text" :intro_text ,"intro_audio" :intro_audio
                             ,"intro_video" :intro_video,"signable":signable}

            results = db.run(expression, property_dict)
            return 1  # 1代表成功

        except Exception as e:
            print("服务器错误", str(e))
            return None
