1.common/libs 写的是python后台和neo4j的交互代码
2.webs/controllers  写的是前端js和后台py的api接口，api都是由py书写，js调用，pyreturn。
3.webs/static  webs/templates 都是写的是后台与管理员界面的交互，二者需要完全分离。
需要什么功能，就用py在后台实现一个api供前端调用即可。
像前端的请求，后台在tmeplates里面有个api实现的就是：后台记录打卡，返回前端显示操作成功。
4.test.py是用于创建数据库的main函数