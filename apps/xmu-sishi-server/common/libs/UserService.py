#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import base64
import random
import string
import json
import requests
from application import app,get_db
from common.models.User import User

class UserService:
   


    @staticmethod
    def updateTest2(test):
        db = get_db()

        results = db.run("MATCH (user:USER) "
                 "SET user.test=$test,user.time='20202020202020202020'",{"test": test}
        )


    @staticmethod
    def updateTest():
        db = get_db()

        results = db.run("MATCH (user:USER) "
                 "SET user.test='测试',user.time='20202020202020202020'"
        )
        # db = get_driver()
        # with db.session() as session:
        #     results = session.run("MATCH (user:USER) "
        #          "SET user.test='测试',user.time='20202020202020202020'"
        #     )




    @staticmethod
    def createuser(data):
        db = get_db
        if data['usertype'] == 1:
            usertype = 'STUDENT'
        elif data['usertype'] == 2:
            usertype = 'TEACHER'
        else:
            usertype = 'STAFF'
        expression="CREATE(no:$data['no'])"
        try:
            results = db.run(expression)
            return 1
        except Exception as e:
            return None

    @staticmethod
    def searchuser(name,label):
        db=get_db
        expression="MATCH(user:USER,{name:$name} RETURN user"
        result=db.run(expression)
        userList = []
        for record in results:
            tmp = User(record['node'])
            userList.append(tmp)
        return userList
        
    @staticmethod
    def geneUserid(userno, salt):
        m = hashlib.md5()
        s = "%s-%s" % (base64.encodebytes(userno.encode("utf-8")), salt)
        m.update(s.encode("utf-8"))
        return m.hexdigest()


    @staticmethod
    def updateUser(data):
        db = get_db()
        if data['usertype']==1 :
            usertype='STUDENT'
        elif data['usertype']==2 :
            usertype='TEACHER'
        else:
            usertype='STAFF'

        results = db.run("MERGE (user:USER {no:$no}) "
                 "SET user:"+usertype+",user.name=$name,user.dept=$dept ,user.userid=$userid",
                 {"no": data['userno'] ,"name": data['username'],"dept": data['userorg'],"userid": data['userid']}
        )


    @staticmethod
    def getByUserid(userid):
        db = get_db()
        #todo student或teacher标签,需要知道该token的角色
        results = db.run("MATCH (user:USER {userid:$userid}) "
                 "RETURN user,labels(user) as labels", {"userid": userid}
        )
        record = results.single();
        if not record:
            return None
        
        user=User(record['user'],record['labels'])
        
        return user



    @staticmethod
    def updateState(state,userlist,updatetime):
        db = get_db()

        results = db.run("FOREACH ( "
                 "no IN $userlist | "
                 "MERGE (user:USER {no:no}) "
                 "SET user.state=$state,user.updatetime=$updatetime )",
                 {"userlist": userlist ,"state": state,"updatetime": updatetime}
        )





    @staticmethod
    def search(usertype,dept,no,name,page,size):
        db = get_db()
        if usertype==1 :
            usertype='STUDENT'
        elif usertype==2:
            usertype='TEACHER'
        else:
            usertype='STAFF'

        #获取总数
        results = db.run("MATCH (user:USER:"+usertype+") "
                 "WHERE user.dept =~ $dept AND user.no =~ $no AND user.name =~ $name "
                 "RETURN COUNT(1) AS count", {"dept": "(?i).*" + dept + ".*","no": "(?i).*" + no + ".*","name": "(?i).*" + name + ".*"}
        )

        result=results.single()
        totalCount=result['count']

        offset = (page - 1) * size

        #获取列表
        results = db.run("MATCH (user:USER:"+usertype+") "
                 "WHERE user.dept =~ $dept AND user.no =~ $no AND user.name =~ $name "
                 "RETURN user.dept AS dept,user.no AS no,user.name AS name ORDER BY user.no skip $offset limit $size ", {"dept": "(?i).*" + dept + ".*","no": "(?i).*" + no + ".*","name": "(?i).*" + name + ".*","offset":offset,"size":size}
        )

        userList=[]
        for record in results:
            userList.append({
            "dept": record['dept'],
            "no": record['no'],
            "name": record['name'],
            })

        return totalCount,userList




    



    @staticmethod
    def getStateAll(page,size):
        db = get_db()
        
        #获取总数
        results = db.run("MATCH (user:USER) "
                 "RETURN COUNT(1) AS count"
        )

        result=results.single()
        totalCount=result['count']

        offset = (page - 1) * size

        #获取列表
        results = db.run("MATCH (user:USER) "
                 "RETURN user.no AS no,user.state AS state,user.updatetime AS updatetime ORDER BY user.no skip $offset limit $size ", {"offset":offset,"size":size}
        )

        stateList=[]
        for record in results:
            stateList.append({
            "XGH": record['no'],
            "state": record['state'],
            "updatetime": record['updatetime'],
            })

        return totalCount,stateList


    @staticmethod
    def getStateNull(page,size):
        db = get_db()
        
        #获取总数
        results = db.run("MATCH (user:USER) "
                 "WHERE user.state is null "
                 "RETURN COUNT(1) AS count"
        )

        result=results.single()
        totalCount=result['count']

        offset = (page - 1) * size

        #获取列表
        results = db.run("MATCH (user:USER) "
                 "WHERE user.state is null "
                 "RETURN user.no AS no,user.state AS state,user.updatetime AS updatetime ORDER BY user.no skip $offset limit $size ", {"offset":offset,"size":size}
        )

        stateList=[]
        for record in results:
            stateList.append({
            "XGH": record['no'],
            "state": record['state'],
            "updatetime": record['updatetime'],
            })

        return totalCount,stateList


    @staticmethod
    def getStateNullWithNoList(noList,page,size):
        db = get_db()
        
        #获取总数
        results = db.run("MATCH (user:USER) "
                 "WHERE user.no IN $noList AND user.state is null "
                 "RETURN COUNT(1) AS count",{"noList":noList}
        )

        result=results.single()
        totalCount=result['count']

        offset = (page - 1) * size

        #获取列表
        results = db.run("MATCH (user:USER) "
                 "WHERE user.no IN $noList AND user.state is null "
                 "RETURN user.no AS no,user.state AS state,user.updatetime AS updatetime ORDER BY user.no skip $offset limit $size ", {"noList":noList,"offset":offset,"size":size}
        )

        stateList=[]
        for record in results:
            stateList.append({
            "XGH": record['no'],
            "state": record['state'],
            "updatetime": record['updatetime'],
            })

        return totalCount,stateList



    @staticmethod
    def getStateWithNoList(noList,page,size):
        db = get_db()
        
        #获取总数
        results = db.run("MATCH (user:USER) "
                 "WHERE user.no IN $noList "
                 "RETURN COUNT(1) AS count",{"noList":noList}
        )

        result=results.single()
        totalCount=result['count']

        offset = (page - 1) * size

        #获取列表
        results = db.run("MATCH (user:USER) "
                 "WHERE user.no IN $noList "
                 "RETURN user.no AS no,user.state AS state,user.updatetime AS updatetime ORDER BY user.no skip $offset limit $size ", {"noList":noList,"offset":offset,"size":size}
        )

        stateList=[]
        for record in results:
            stateList.append({
            "XGH": record['no'],
            "state": record['state'],
            "updatetime": record['updatetime'],
            })

        return totalCount,stateList


    @staticmethod
    def getStateWithState(state,page,size):
        db = get_db()
        
        #获取总数
        results = db.run("MATCH (user:USER{state:$state}) "
                 "RETURN COUNT(1) AS count",{"state":state}
        )

        result=results.single()
        totalCount=result['count']

        offset = (page - 1) * size

        #获取列表
        results = db.run("MATCH (user:USER{state:$state}) "
                 "RETURN user.no AS no,user.state AS state,user.updatetime AS updatetime ORDER BY user.no skip $offset limit $size ", {"state":state,"offset":offset,"size":size}
        )

        stateList=[]
        for record in results:
            stateList.append({
            "XGH": record['no'],
            "state": record['state'],
            "updatetime": record['updatetime'],
            })

        return totalCount,stateList

    
    
    @staticmethod
    def getStateWithNoListAndState(state,noList,page,size):
        db = get_db()
        
        #获取总数
        results = db.run("MATCH (user:USER{state:$state}) "
                 "WHERE user.no IN $noList "
                 "RETURN COUNT(1) AS count",{"state":state,"noList":noList}
        )

        result=results.single()
        totalCount=result['count']

        offset = (page - 1) * size

        #获取列表
        results = db.run("MATCH (user:USER{state:$state}) "
                 "WHERE user.no IN $noList "
                 "RETURN user.no AS no,user.state AS state,user.updatetime AS updatetime ORDER BY user.no skip $offset limit $size ", {"state":state,"noList":noList,"offset":offset,"size":size}
        )

        stateList=[]
        for record in results:
            stateList.append({
            "XGH": record['no'],
            "state": record['state'],
            "updatetime": record['updatetime'],
            })

        return totalCount,stateList



    @staticmethod
    def deleteLeader():
        db = get_db()
        results = db.run("MATCH (user:USER) "
                 "REMOVE user.leader "
        )


    @staticmethod
    def addLeader(userlist):
        db = get_db()

        results = db.run("FOREACH ( "
                 "no IN $userlist | "
                 "MERGE (user:USER {no:no}) "
                 "SET user.leader=1 )",
                 {"userlist": userlist }
        )


    @staticmethod
    def getLeader(page,size):
        db = get_db()
        
        #获取总数
        results = db.run("MATCH (user:USER{leader:1}) "
                 "RETURN COUNT(1) AS count"
        )

        result=results.single()
        totalCount=result['count']

        offset = (page - 1) * size

        #获取列表
        results = db.run("MATCH (user:USER{leader:1}) "
                 "RETURN user.no AS no ORDER BY user.no skip $offset limit $size ", {"offset":offset,"size":size}
        )

        userList=[]
        for record in results:
            userList.append({
            "XGH": record['no'],
            })

        return totalCount,userList



    # 审批相关
    @staticmethod
    def getReviewerNoAndName():
        db = get_db()

        results = db.run("MATCH (user:REVIEWER) "
                 "RETURN user.no as no,user.name as name ORDER BY user.name DESC"
        )
        
        reviewerList=[]
        for record in results:
            reviewerList.append({
            "no": record['no'],
            "name": record['name']
        })

        return reviewerList


    @staticmethod
    def getMyApply(no,type,pageNum,pageSize):
        db = get_db()
        offset = (pageNum - 1) * pageSize
        # if usertype==1 :
        #     usertype='STUDENT'
        # elif usertype==2:
        #     usertype='TEACHER'
        #获取列表 todo 增加角色标签

        # todo 分类 WHERE rr.state=0 or rr.state=-1 or rr.state=1 

        if type==2:#2未审
            results = db.run("MATCH (a:USER{ no : $no }) -[r:APPLY]-> (b:REVIEWER) WITH a,r,b "
                     "MATCH (a) -[rr:APPLY{id:r.id}]-> (v:VENUE) "
                     "WHERE rr.state=0 "
                     "RETURN rr.id as id,rr.starttime as starttime,rr.endtime as endtime,rr.applytime as applytime,rr.approvetime as approvetime,rr.state as state,rr.reason as reason,b.name as reviewer,v.name as venue ORDER BY rr.applytime DESC skip $offset limit $size ", 
                     {"no": no,"offset":offset,"size":pageSize}
            )
        elif type==3:#3已审
            results = db.run("MATCH (a:USER{ no : $no }) -[r:APPLY]-> (b:REVIEWER) WITH a,r,b "
                     "MATCH (a) -[rr:APPLY{id:r.id}]-> (v:VENUE) "
                     "WHERE rr.state=-1 or rr.state=1 "
                     "RETURN rr.id as id,rr.starttime as starttime,rr.endtime as endtime,rr.applytime as applytime,rr.approvetime as approvetime,rr.state as state,rr.reason as reason,b.name as reviewer,v.name as venue ORDER BY rr.applytime DESC skip $offset limit $size ", 
                     {"no": no,"offset":offset,"size":pageSize}
            )
        else:#1全部
            results = db.run("MATCH (a:USER{ no : $no }) -[r:APPLY]-> (b:REVIEWER) WITH a,r,b "
                     "MATCH (a) -[rr:APPLY{id:r.id}]-> (v:VENUE) "
                     "RETURN rr.id as id,rr.starttime as starttime,rr.endtime as endtime,rr.applytime as applytime,rr.approvetime as approvetime,rr.state as state,rr.reason as reason,b.name as reviewer,v.name as venue ORDER BY rr.applytime DESC skip $offset limit $size ", 
                     {"no": no,"offset":offset,"size":pageSize}
            )

        myApplyList=[]
        for record in results:
            tmp_data = {
                "id": record['id'],
                "starttime": record['starttime'],
                "endtime": record['endtime'],
                "applytime": record['applytime'],
                "approvetime": record['approvetime'],
                "state": record['state'],
                "reason": record['reason'],
                "reviewer": record['reviewer'],
                "venue": record['venue'],
            }
            myApplyList.append(tmp_data)

        return myApplyList


    @staticmethod
    def getMyApprove(no,type,pageNum,pageSize):
        db = get_db()
        offset = (pageNum - 1) * pageSize
        # if usertype==1 :
        #     usertype='STUDENT'
        # elif usertype==2:
        #     usertype='TEACHER'
        #获取列表 todo 增加角色标签

        # todo 分类 WHERE rr.state=0 or rr.state=-1 or rr.state=1 
        if type==2:#2未审
            results = db.run("MATCH (a:USER) -[r:APPLY]-> (b:REVIEWER{ no : $no }) WITH a,r,b "
                     "MATCH (a) -[rr:APPLY{id:r.id}]-> (v:VENUE) "
                     "WHERE rr.state=0 "
                     "RETURN rr.id as id,rr.starttime as starttime,rr.endtime as endtime,rr.applytime as applytime,rr.approvetime as approvetime,rr.state as state,rr.reason as reason,v.name as venue, a.dept as userdept,a.no as userno,a.name as username ORDER BY rr.applytime DESC skip $offset limit $size ", 
                     {"no": no,"offset":offset,"size":pageSize}
            )
        elif type==3:#3已审
            results = db.run("MATCH (a:USER) -[r:APPLY]-> (b:REVIEWER{ no : $no }) WITH a,r,b "
                     "MATCH (a) -[rr:APPLY{id:r.id}]-> (v:VENUE) "
                     "WHERE rr.state=-1 or rr.state=1 "
                     "RETURN rr.id as id,rr.starttime as starttime,rr.endtime as endtime,rr.applytime as applytime,rr.approvetime as approvetime,rr.state as state,rr.reason as reason,v.name as venue, a.dept as userdept,a.no as userno,a.name as username ORDER BY rr.applytime DESC skip $offset limit $size ", 
                     {"no": no,"offset":offset,"size":pageSize}
            )
        else:
            results = db.run("MATCH (a:USER) -[r:APPLY]-> (b:REVIEWER{ no : $no }) WITH a,r,b "
                     "MATCH (a) -[rr:APPLY{id:r.id}]-> (v:VENUE) "
                     "RETURN rr.id as id,rr.starttime as starttime,rr.endtime as endtime,rr.applytime as applytime,rr.approvetime as approvetime,rr.state as state,rr.reason as reason,v.name as venue, a.dept as userdept,a.no as userno,a.name as username ORDER BY rr.applytime DESC skip $offset limit $size ", 
                     {"no": no,"offset":offset,"size":pageSize}
            )

        myApplyList=[]
        for record in results:
            tmp_data = {
                "id": record['id'],
                "starttime": record['starttime'],
                "endtime": record['endtime'],
                "applytime": record['applytime'],
                "approvetime": record['approvetime'],
                "state": record['state'],
                "reason": record['reason'],
                "venue": record['venue'],
                "userdept": record['userdept'],
                "userno": record['userno'],
                "username": record['username'],
            }
            myApplyList.append(tmp_data)

        return myApplyList

        

    # @staticmethod
    # def addApply(no,venueid,reviewer,id,applytime,starttime,endtime,reason):
    #     db = get_db()
    #     results = db.run("MATCH (user:USER{no:$no}) "
    #              "MATCH (venue:VENUE{id:$venueid}) "
    #              "MATCH (reviewer:REVIEWER{no:$reviewer}) "
    #              "CREATE (user)-[r:APPLY{id:$id,starttime:$starttime,endtime:$endtime,reason:$reason,applytime:$applytime,approvetime:'',state:0}]->(venue) "
    #              "CREATE (user)-[rr:APPLY{id:$id2}]->(reviewer) ",
    #              {"no": no ,"venueid": venueid,"reviewer": reviewer,"id": id,"starttime":starttime,"endtime":endtime,"reason":reason,"applytime":applytime,"id2": id}
    #     )

    @staticmethod
    def addApply(no,venueid,reviewer,id,applytime,starttime,endtime,reason):
        db = get_db()
        results = db.run("MATCH (user:USER{no:$no}) "
                 "MATCH (venue:VENUE{id:$venueid}) "
                 "MATCH (reviewer:REVIEWER{no:$reviewer}) "
                 "CREATE (user)-[r:APPLY{id:$id,starttime:$starttime,endtime:$endtime,reason:$reason,applytime:$applytime,approvetime:$applytime,state:1}]->(venue) "
                 "CREATE (user)-[rr:APPLY{id:$id2}]->(reviewer) ",
                 {"no": no ,"venueid": venueid,"reviewer": reviewer,"id": id,"starttime":starttime,"endtime":endtime,"reason":reason,"applytime":applytime,"id2": id}
        )


    @staticmethod
    def approve(no,id,state,approvetime):
        db = get_db()
        results = db.run("MATCH (a:USER)-[r:APPLY{id:$id}]->(b:REVIEWER{no:$no}) with a,r,b "
                 "MATCH (a)-[rr:APPLY{id:r.id}]->(v:VENUE) "
                 "SET rr.approvetime=$approvetime,rr.state=$state ",
                 {"no": no ,"id": id,"state":state,"approvetime":approvetime}
        )

    @staticmethod
    def cancel(no,id):
        db = get_db()
        db.run("MATCH (a:USER{no:$no})-[r:APPLY{id:$id}]->(b:REVIEWER) "
                 "DELETE r",
                 {"no": no ,"id": id}
        )

        db.run("MATCH (a:USER{no:$no})-[r:APPLY{id:$id}]->(v:VENUE) "
                 "DELETE r",
                 {"no": no ,"id": id}
        )


    @staticmethod
    def hasLegalApply(no,venueid,str_now):
        db = get_db()
        # if data['usertype']=='student' :
        #     usertype='STUDENT'
        # elif data['usertype']=='teacher' :
        #     usertype='TEACHER'

        # todo 增加角色标签 Student or Teacher
        results = db.run("MATCH (a:USER{no:$no})-[r:APPLY{state:1}]->(v:VENUE{id:$id}) "
                         "WHERE r.starttime < $starttime AND r.endtime > $endtime "
                         "RETURN r ",
                        {"no": no,"id": venueid,"starttime": str_now,"endtime": str_now}
        )

        result=results.single()
        
        if not result:
            return False
        else:
            return True

