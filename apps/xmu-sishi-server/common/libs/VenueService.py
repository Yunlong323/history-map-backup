#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import string
from application import get_db
from common.models.Venue import Venue
import time

class VenueService:


    @staticmethod
    def search(adminno,status,name,page,size):
        db = get_db()
        
        #获取总数
        if status==0:#没传状态
            if adminno=="":#超级管理员
                results = db.run("MATCH (venue:VENUE) "
                         "WHERE venue.name =~ $name "
                         "RETURN COUNT(1) AS count", {"name": "(?i).*" + name + ".*"}
                )
            else:#场所管理员
                results = db.run("MATCH (user:ADMIN{no:$adminno}) - [r:MANAGE] -> (venue:VENUE) "
                         "WHERE venue.name =~ $name "
                         "RETURN COUNT(1) AS count", {"adminno":adminno,"name": "(?i).*" + name + ".*"}
                )
        else:#有传状态
            if adminno=="":#超级管理员
                results = db.run("MATCH (venue:VENUE) "
                         "WHERE venue.name =~ $name AND venue.status = $status "
                         "RETURN COUNT(1) AS count", {"name": "(?i).*" + name + ".*","status": status}
                )
            else:#场所管理员
                results = db.run("MATCH (user:ADMIN{no:$adminno}) - [r:MANAGE] -> (venue:VENUE) "
                         "WHERE venue.name =~ $name AND venue.status = $status "
                         "RETURN COUNT(1) AS count", {"adminno":adminno,"name": "(?i).*" + name + ".*","status": status}
                )

        result=results.single()
        totalCount=result['count']

        offset = (page - 1) * size

        #获取列表
        if status==0:
            if adminno=="":#超级管理员
                results = db.run("MATCH (venue:VENUE) "
                         "WHERE venue.name =~ $name "
                         "RETURN venue ORDER BY venue.createtime DESC skip $offset limit $size ", {"name": "(?i).*" + name + ".*","offset":offset,"size":size}
                )
            else:#场所管理员
                results = db.run("MATCH (user:ADMIN{no:$adminno}) - [r:MANAGE] -> (venue:VENUE) "
                         "WHERE venue.name =~ $name "
                         "RETURN venue ORDER BY venue.createtime DESC skip $offset limit $size ", {"adminno":adminno,"name": "(?i).*" + name + ".*","offset":offset,"size":size}
                )
        else:
            if adminno=="":#超级管理员
                results = db.run("MATCH (venue:VENUE) "
                         "WHERE venue.name =~ $name AND venue.status = $status "
                         "RETURN venue ORDER BY venue.createtime DESC skip $offset limit $size ", {"name": "(?i).*" + name + ".*","status": status,"offset":offset,"size":size}
                )
            else:#场所管理员
                results = db.run("MATCH (user:ADMIN{no:$adminno}) - [r:MANAGE] -> (venue:VENUE) "
                         "WHERE venue.name =~ $name AND venue.status = $status "
                         "RETURN venue ORDER BY venue.createtime DESC skip $offset limit $size ", {"adminno":adminno,"name": "(?i).*" + name + ".*","status": status,"offset":offset,"size":size}
                )

        venueList=[]
        for record in results:
            tmp=Venue(record['venue'])
            venueList.append(tmp)

        return totalCount,venueList


    @staticmethod
    def reverseStatus(adminno,id):
        db = get_db()
        if adminno=="":
            results = db.run("MATCH (venue:VENUE { id : $id}) "
                             "SET venue.status = -venue.status",
                     {"id": id}
            )
        else:
            results = db.run("MATCH (user:ADMIN{no:$adminno}) - [r:MANAGE] -> (venue:VENUE{ id : $id}) "
                             "SET venue.status = -venue.status",
                     {"adminno": adminno,"id": id}
            )



    @staticmethod
    def update(adminno,id,name,lon,lat,permissionType):
        db = get_db()
        if adminno=="":#超级管理员
            results = db.run("MATCH (venue:VENUE { id : $id}) "
                             "SET venue.name = $name,venue.lon = $lon,venue.lat = $lat,venue.permissionType = $permissionType",
                     {"id": id,"name": name ,"lon": lon,"lat": lat,"permissionType": permissionType}
            )
        else:
            results = db.run("MATCH (user:ADMIN{no:$adminno}) - [r:MANAGE] -> (venue:VENUE{ id : $id}) "
                             "SET venue.name = $name,venue.lon = $lon,venue.lat = $lat,venue.permissionType = $permissionType",
                     {"adminno": adminno,"id": id,"name": name ,"lon": lon,"lat": lat,"permissionType": permissionType}
            )


    @staticmethod
    def geneVenueID(length=16):
        keylist = [random.choice(string.ascii_letters + string.digits) for i in range(length)]
        return "".join(keylist)


    @staticmethod
    def create(id,name,lon,lat,permissionType,createtime):
        db = get_db()
        results = db.run("CREATE (venue:VENUE{ "
                         "id : $id ,name : $name ,lon : $lon ,lat : $lat,status : $status,permissionType : $permissionType,createtime : $createtime}) ",
                 {"id": id,"name": name ,"lon": lon,"lat": lat,"status": 1,"permissionType": permissionType,"createtime": createtime}
        )

    @staticmethod
    def getVenueStatistics(adminno,id):
        # 按小时统计
        db = get_db()
        if adminno=="":
            results = db.run("MATCH (a:USER)-[r:GOTO]->(b:VENUE{id:$id}) "
                     "RETURN distinct SUBSTRING(r.time,0,13) AS day, COUNT(1) AS count ORDER BY day", 
                     {"id": id})
        else:
            results = db.run("MATCH (user:ADMIN{no:$adminno}) - [r:MANAGE] -> (venue:VENUE{id:$id}) with venue "
                     "MATCH (a:USER)-[r:GOTO]->(venue) "
                     "RETURN distinct SUBSTRING(r.time,0,13) AS day, COUNT(1) AS count ORDER BY day", 
                     {"adminno": adminno,"id": id})
        
        statistics=[]
        for record in results:
            statistics.append({
                "day": record['day'],
                "count": record['count']
            })
        return statistics



    @staticmethod
    def getWhiteListTagsDetail(adminno,id):
        db = get_db()

        tagList=[]

        if adminno=="":
            #获取场所白名单的所有版本tag
            results = db.run("MATCH (user:USER)-[r:PERMISSION]->(venue:VENUE { id : $id} ) "
                     "RETURN distinct(r.id) as id ORDER BY id DESC", {"id": id}
            )

            for record in results:
                result = db.run("MATCH (user:USER)-[r:PERMISSION{id : $tag_id}]->(venue:VENUE { id : $id} ) "
                     "RETURN r limit 1", {"tag_id": record['id'],"id": id}
                )
                result=result.single()

                count = db.run("MATCH (user:USER)-[r:PERMISSION{id:$tagID}]->(venue:VENUE { id : $id} ) "
                         "RETURN COUNT(1) AS count", {"tagID": record['id'],"id": id}
                )
                count=count.single()

                #id就是时间戳
                tagList.append({
                "id": result['r']['id'],
                "time": time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(result['r']['id'])),
                "tag": result['r']['tag'],
                "active": result['r']['active'],
                "count": count['count'],
                })

        else:
            results = db.run("MATCH (user:ADMIN{no:$adminno}) - [r:MANAGE] -> (venue:VENUE{id:$id}) with venue "
                     "MATCH (user:USER)-[r:PERMISSION]->(venue) "
                     "RETURN distinct(r.id) as id ORDER BY id DESC", {"adminno": adminno,"id": id}
            )

            for record in results:
                result = db.run("MATCH (user:ADMIN{no:$adminno}) - [r:MANAGE] -> (venue:VENUE{id:$id}) with venue "
                     "MATCH (user:USER)-[r:PERMISSION{id : $tag_id}]->(venue) "
                     "RETURN r limit 1", {"adminno": adminno,"tag_id": record['id'],"id": id}
                )
                result=result.single()

                count = db.run("MATCH (user:ADMIN{no:$adminno}) - [r:MANAGE] -> (venue:VENUE{id:$id}) with venue "
                     "MATCH (user:USER)-[r:PERMISSION{id:$tagID}]->(venue) "
                     "RETURN COUNT(1) AS count", {"adminno": adminno,"tagID": record['id'],"id": id}
                )
                count=count.single()

                #id就是时间戳
                tagList.append({
                "id": result['r']['id'],
                "time": time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(result['r']['id'])),
                "tag": result['r']['tag'],
                "active": result['r']['active'],
                "count": count['count'],
                })

        return tagList


    @staticmethod
    def getWhiteListTag(tagID,id):
        db = get_db()

        result = db.run("MATCH (user:USER)-[r:PERMISSION{id : $tag_id}]->(venue:VENUE { id : $id} ) "
             "RETURN r limit 1", {"tag_id": tagID,"id": id}
        )
        result=result.single()
        if not result:
            return None
        return{
            "id": result['r']['id'],
            "tag": result['r']['tag'],
            "active": result['r']['active'],
        }

    @staticmethod
    def getWhiteList(adminno,tagID,id,dept,no,name,page,size):
        db = get_db()
        
        if adminno=="":
            if dept!="" or name!='':#dept和name要么都空 要么都不空
                results = db.run("MATCH (user:USER)-[r:PERMISSION{id:$tagID}]->(venue:VENUE { id : $id} ) "
                         "WHERE user.dept =~ $dept AND user.no =~ $no AND user.name =~ $name "
                         "RETURN COUNT(1) AS count", {"tagID": tagID,"id": id,"dept":"(?i).*" + dept + ".*","no":"(?i).*" + no + ".*","name":"(?i).*" + name + ".*"}
                )
            else:
                results = db.run("MATCH (user:USER)-[r:PERMISSION{id:$tagID}]->(venue:VENUE { id : $id} ) "
                         "WHERE user.no =~ $no "
                         "RETURN COUNT(1) AS count", {"tagID": tagID,"id": id,"no":"(?i).*" + no + ".*"}
                )

        else:
            if dept!="" or name!='':#dept和name要么都空 要么都不空
                results = db.run("MATCH (user:ADMIN{no:$adminno}) - [r:MANAGE] -> (venue:VENUE{id:$id}) with venue "
                         "MATCH (user:USER)-[r:PERMISSION{id:$tagID}]->(venue) "
                         "WHERE user.dept =~ $dept AND user.no =~ $no AND user.name =~ $name "
                         "RETURN COUNT(1) AS count", {"adminno": adminno,"tagID": tagID,"id": id,"dept":"(?i).*" + dept + ".*","no":"(?i).*" + no + ".*","name":"(?i).*" + name + ".*"}
                )
            else:
                results = db.run("MATCH (user:ADMIN{no:$adminno}) - [r:MANAGE] -> (venue:VENUE{id:$id}) with venue "
                         "MATCH (user:USER)-[r:PERMISSION{id:$tagID}]->(venue) "
                         "WHERE user.no =~ $no "
                         "RETURN COUNT(1) AS count", {"adminno": adminno,"tagID": tagID,"id": id,"no":"(?i).*" + no + ".*"}
                )



        result=results.single()
        totalCount=result['count']

        offset = (page - 1) * size

        #获取列表
        if adminno=="":
            if dept!="" or name!='':#dept和name要么都空 要么都不空
                results = db.run("MATCH (user:USER)-[r:PERMISSION{id:$tagID}]->(venue:VENUE { id : $id} ) "
                         "WHERE user.dept =~ $dept AND user.no =~ $no AND user.name =~ $name "
                         "RETURN user.dept as dept,user.no as no,user.name as name ORDER BY user.no skip $offset limit $size ", {"tagID": tagID,"id": id,"dept":"(?i).*" + dept + ".*","no":"(?i).*" + no + ".*","name":"(?i).*" + name + ".*","offset":offset,"size":size}
                )
            else:
                results = db.run("MATCH (user:USER)-[r:PERMISSION{id:$tagID}]->(venue:VENUE { id : $id} ) "
                         "WHERE user.no =~ $no "
                         "RETURN user.dept as dept,user.no as no,user.name as name ORDER BY user.no skip $offset limit $size ", {"tagID": tagID,"id": id,"no":"(?i).*" + no + ".*","offset":offset,"size":size}
                )
        else:
            if dept!="" or name!='':#dept和name要么都空 要么都不空
                results = db.run("MATCH (user:ADMIN{no:$adminno}) - [r:MANAGE] -> (venue:VENUE{id:$id}) with venue "
                         "MATCH (user:USER)-[r:PERMISSION{id:$tagID}]->(venue) "
                         "WHERE user.dept =~ $dept AND user.no =~ $no AND user.name =~ $name "
                         "RETURN user.dept as dept,user.no as no,user.name as name ORDER BY user.no skip $offset limit $size ", {"adminno": adminno,"tagID": tagID,"id": id,"dept":"(?i).*" + dept + ".*","no":"(?i).*" + no + ".*","name":"(?i).*" + name + ".*","offset":offset,"size":size}
                )
            else:
                results = db.run("MATCH (user:ADMIN{no:$adminno}) - [r:MANAGE] -> (venue:VENUE{id:$id}) with venue "
                         "MATCH (user:USER)-[r:PERMISSION{id:$tagID}]->(venue) "
                         "WHERE user.no =~ $no "
                         "RETURN user.dept as dept,user.no as no,user.name as name ORDER BY user.no skip $offset limit $size ", {"adminno": adminno,"tagID": tagID,"id": id,"no":"(?i).*" + no + ".*","offset":offset,"size":size}
                )

        whiteList=[]
        
        for record in results:
            whiteList.append({
            "dept": record['dept'],
            "no": record['no'],
            "name": record['name'],
        })

        return totalCount,whiteList

    @staticmethod
    def deleteWhiteList(adminno,tag,id):
        db = get_db()
        if adminno=="":
            results = db.run("MATCH (user:USER)-[r:PERMISSION{id:$tagID}]->(venue:VENUE { id : $id} ) "
                             "DELETE r",
                     {"tagID": tag['id'],"id": id}
            )
        else:
            results = db.run("MATCH (user:ADMIN{no:$adminno}) - [r:MANAGE] -> (venue:VENUE{id:$id}) with venue "
                             "MATCH (user:USER)-[r:PERMISSION{id:$tagID}]->(venue) "
                             "DELETE r",
                     {"adminno": adminno,"tagID": tag['id'],"id": id}
            )

    @staticmethod
    def updateWhiteList(adminno,tag,id,whitelist):

        db = get_db()
        if adminno=="":
            results = db.run("MATCH (venue:VENUE { id : $id}) with venue "
                             "FOREACH ( "
                             "no IN $whitelist | "
                             "MERGE (user:USER{no:no}) "
                             "CREATE (user)-[r:PERMISSION{id:$tagID,tag:$tagName,active:$tagActive}]->(venue) ) ",
                     {"tagID": tag['id'],"tagName": tag['tag'],"tagActive": tag['active'],"id": id,"whitelist": whitelist}
            )
        else:
            results = db.run("MATCH (user:ADMIN{no:$adminno}) - [r:MANAGE] -> (venue:VENUE{id:$id}) with venue "
                             "FOREACH ( "
                             "no IN $whitelist | "
                             "MERGE (user:USER{no:no}) "
                             "CREATE (user)-[r:PERMISSION{id:$tagID,tag:$tagName,active:$tagActive}]->(venue) ) ",
                     {"adminno": adminno,"tagID": tag['id'],"tagName": tag['tag'],"tagActive": tag['active'],"id": id,"whitelist": whitelist}
            )

    @staticmethod
    def reverseTagStatus(adminno,id,tagID):
        db = get_db()
        if adminno=="":
            results = db.run("MATCH (user:USER)-[r:PERMISSION{id:$tagID}]->(venue:VENUE { id : $id} ) "
                             "SET r.active = -r.active",
                     {"tagID": tagID,"id": id}
            )
        else:
            results = db.run("MATCH (user:ADMIN{no:$adminno}) - [r:MANAGE] -> (venue:VENUE{id:$id}) with venue "
                             "MATCH (user:USER)-[r:PERMISSION{id:$tagID}]->(venue) "
                             "SET r.active = -r.active",
                     {"adminno": adminno,"tagID": tagID,"id": id}
            )

    @staticmethod
    def deleteTag(adminno,id,tagID):
        db = get_db()
        if adminno=="":
            results = db.run("MATCH (user:USER)-[r:PERMISSION{id:$tagID}]->(venue:VENUE { id : $id} ) "
                             "DELETE r",
                     {"tagID": tagID,"id": id}
            )
        else:
            results = db.run("MATCH (user:ADMIN{no:$adminno}) - [r:MANAGE] -> (venue:VENUE{id:$id}) with venue "
                             "MATCH (user:USER)-[r:PERMISSION{id:$tagID}]->(venue) "
                             "DELETE r",
                     {"adminno": adminno,"tagID": tagID,"id": id}
            )

    @staticmethod
    def deleteWhiteNo(adminno,tagID,id,no):
        db = get_db()
        if adminno=="":
            results = db.run("MATCH (user:USER{ no : $no})-[r:PERMISSION{id:$tagID}]->(venue:VENUE { id : $id} ) "
                             "DELETE r",
                     {"tagID": tagID,"no": no,"id": id}
            )
        else:
            results = db.run("MATCH (user:ADMIN{no:$adminno}) - [r:MANAGE] -> (venue:VENUE{id:$id}) with venue "
                             "MATCH (user:USER{ no : $no})-[r:PERMISSION{id:$tagID}]->(venue) "
                             "DELETE r",
                     {"adminno": adminno,"tagID": tagID,"no": no,"id": id}
            )


    @staticmethod
    def getAdminList(id,dept,no,name,page,size):
        db = get_db()
        
        if dept!="" or name!='':#dept和name要么都空 要么都不空
            results = db.run("MATCH (user:USER:ADMIN)-[r:MANAGE]->(venue:VENUE { id : $id} ) "
                     "WHERE user.dept =~ $dept AND user.no =~ $no AND user.name =~ $name "
                     "RETURN COUNT(1) AS count", {"id": id,"dept":"(?i).*" + dept + ".*","no":"(?i).*" + no + ".*","name":"(?i).*" + name + ".*"}
            )
        else:#dept和name都空的时候
            results = db.run("MATCH (user:USER:ADMIN)-[r:MANAGE]->(venue:VENUE { id : $id} ) "
                     "WHERE user.no =~ $no "
                     "RETURN COUNT(1) AS count", {"id": id,"no":"(?i).*" + no + ".*"}
            )

        result=results.single()
        totalCount=result['count']

        offset = (page - 1) * size


        if dept!="" or name!='':
            #获取列表
            results = db.run("MATCH (user:USER:ADMIN)-[r:MANAGE]->(venue:VENUE { id : $id} ) "
                     "WHERE user.dept =~ $dept AND user.no =~ $no AND user.name =~ $name "
                     "RETURN user.dept as dept,user.no as no,user.name as name ORDER BY user.no skip $offset limit $size ", {"id": id,"dept":"(?i).*" + dept + ".*","no":"(?i).*" + no + ".*","name":"(?i).*" + name + ".*","offset":offset,"size":size}
            )
        else:#dept和name都空的时候
            #获取列表
            results = db.run("MATCH (user:USER:ADMIN)-[r:MANAGE]->(venue:VENUE { id : $id} ) "
                     "WHERE user.no =~ $no "
                     "RETURN user.dept as dept,user.no as no,user.name as name ORDER BY user.no skip $offset limit $size ", {"id": id,"no":"(?i).*" + no + ".*","offset":offset,"size":size}
            )


        adminList=[]

        for record in results:
            adminList.append({
            "dept": record['dept'],
            "no": record['no'],
            "name": record['name'],
        })

        return totalCount,adminList

    @staticmethod
    def deleteAdminList(id):
        db = get_db()
        results = db.run("MATCH (user:USER:ADMIN)-[r:MANAGE]->(venue:VENUE { id : $id} ) "
                         "DELETE r",
                 {"id": id}
        )

    @staticmethod
    def updateAdminList(id,adminlist):
        db = get_db()
        results = db.run("MATCH (venue:VENUE { id : $id}) with venue "
                         "FOREACH ( "
                         "no IN $adminlist  | "
                         "MERGE (user:USER{no:no}) "
                         "CREATE (user)-[r:MANAGE]->(venue) "
                         "SET user:ADMIN,user.status=1 )",
                 {"id": id,"adminlist": adminlist}
        )


    @staticmethod
    def deleteAdminNo(id,no):
        db = get_db()
        results = db.run("MATCH (user:USER:ADMIN{ no : $no})-[r:MANAGE]->(venue:VENUE { id : $id} ) "
                         "DELETE r",
                 {"no": no,"id": id}
        )


    @staticmethod
    def getByID(id):
        db = get_db()
        results = db.run("MATCH (venue:VENUE {id:$id}) "
                 "RETURN venue", {"id": id}
        )
        record = results.single();
        if not record: #if user_info.status != 1: return False
            return None

        venue=Venue(record['venue'])
        return venue
######################################################################################################################



    @staticmethod
    def getAll():
        db = get_db()
        results = db.run("MATCH (venue:VENUE {status:1}) "
                 "RETURN venue.id as id,venue.name as name ")
        
        if not results: #if user_info.status != 1: return False
            return []

        venueList=[]
        for record in results:
            venueList.append({
                "id": record['id'],
                "name": record['name'],
            })
        return venueList


    @staticmethod
    def getAllForIndex(adminno):
        db = get_db()

        if adminno=="":
            results = db.run("MATCH (venue:VENUE {status:1}) "
                     "RETURN venue.id as id,venue.name as name,venue.lat as lat,venue.lon as lon ORDER BY venue.createtime DESC")
        else:
            results = db.run("MATCH (user:ADMIN{no:$adminno}) - [r:MANAGE] -> (venue:VENUE {status:1}) "
                     "RETURN venue.id as id,venue.name as name,venue.lat as lat,venue.lon as lon ORDER BY venue.createtime DESC",
                     {"adminno": adminno})

        if not results: #if user_info.status != 1: return False
            return []

        venueList=[]
        for record in results:
            venueList.append({
                "id": record['id'],
                "name": record['name'],
                "lat": record['lat'],
                "lon": record['lon'],
            })
        return venueList
        

    @staticmethod
    def checkUniqueIdName(id,name):
        db = get_db()
        
        results = db.run("MATCH (venue:VENUE) "
                 "WHERE venue.id <> $id AND venue.name = $name "
                 "RETURN venue", {"id": id,"name": name}
        )
        record=results.single()
        if not record:
            return True
        else:
            return False


    @staticmethod
    def checkUniqueName(name):
        db = get_db()
        
        results = db.run("MATCH (venue:VENUE) "
                 "WHERE venue.name = $name "
                 "RETURN venue", {"name": name}
        )
        record=results.single()
        if not record:
            return True
        else:
            return False


    # 审批相关
    @staticmethod
    def getVenueIdAndName():
        db = get_db()

        # results = db.run("MATCH (venue:VENUE{status:1}) "
        #          "RETURN venue.id as id,venue.name as name ORDER BY venue.name DESC"
        # )
        results = db.run("MATCH (venue:VENUE{status:1}) WHERE venue.name =~ '.*翔安.*' "
                 "RETURN venue.id as id,venue.name as name ORDER BY venue.name DESC"
        )
        
        venueList=[]
        for record in results:
            venueList.append({
            "id": record['id'],
            "name": record['name']
        })

        return venueList




    # 获取我管理的场所
    @staticmethod
    def getMyVenueIdAndName(adminno):
        db = get_db()

        results = db.run("MATCH (user:ADMIN{no:$adminno}) - [r:MANAGE] -> (venue:VENUE{status:1}) "
                 "RETURN venue.id as id,venue.name as name ORDER BY venue.name DESC",{"adminno":adminno}
        )
        
        venueList=[]
        for record in results:
            venueList.append({
            "id": record['id'],
            "name": record['name']
        })

        return venueList

