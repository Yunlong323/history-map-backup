# -*- coding:utf-8 -*-
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
admin = AdminService()
# admin.create_scenery_node(["xmu","signable"],"涉台文物古迹","hot",8.5,"8:00-22:00","可以拍照",'''
# 厦门大学革命史展览馆，位于厦门大学同安楼一楼，于2016年4月正式开馆。展馆设有六个展厅，分“八闽革命摇篮”、“坚持红旗不倒”、“抗日救亡基地”与“东南民主堡垒”四个单元，全面记录了从1921年至1950年厦门大学师生反抗外来侵略、拯救民族危机、加强党团建设的历史。
# “无古不成今，观今宜鉴古。”重温与党同龄的厦门大学自强不息的革命岁月，让我们更加坚定传承红色基因、弘扬革命精神，进一步为实现厦门大学“两个百年”奋斗目标和实现中华民族伟大复兴的中国梦注入了强大的精神动力。
# 2020年12月1日，厦门大学革命史展览馆“全国关心下一代党史国史教育基地”顺利揭牌，有力推进了青年学生党史国史教育这一项基础工程。立于厦大“新百年”的潮头，革命史馆将继续集聚历史能量，发挥教育效用，成为广大青年学生补足“精神之钙”、点亮“信仰之灯”、铸牢“信念之魂”的红色“聚宝盆”。
# ''',"暂无","暂无")
admin.create_scenery_node(["xmu","signable"],"厦门大学校史馆","hot",8.5,"8:00-22.00","可以拍照",'''
厦门大学校史馆坐落于群贤楼一楼，是厦大地标中集展示、教育、研究于一体的重要文化空间。它共设六个展室，内容分为“南强春秋”、“英才摇篮”、“科研重镇”、“走向世界”与“展望未来”五个部分，在校史中串联起“四史”，为厦大人铺展开一幅百年历史长卷。全方位再现了厦大百年来的办学历程与巨大成就。
“欲知大道，必先为史。”一张张校史图片，一段段厦大故事，都是厦大人“不忘初心、牢记使命”的具体体现。凝视历史，既是对厦大风雨历程的回顾，更是对追求美好未来的鞭策。
而今，经过一年多的修缮，满载着师生校友期待与祝福的厦门大学百年校史馆即将面世。按未来视角看，知“四史”与校史，才能准确把握百岁厦大所处的历史方位、历史走向。从厦门集美的一栋楼舍，到如今乘风破浪扬帆起航的“嘉庚号”巨轮，厦门大学的面貌发生了巨变，但厦大人仍然初心不改、使命不移，努力续写着“南方之强”新华章。
''')
admin.create_scenery_node(["xmu","signable"],"卢嘉锡半身像","hot",8.5,"8:00-22.00","可以拍照",'''
在厦门大学化学化工学院大楼前，树立着一尊含笑微微、动情讲课的人形雕像，他就是享誉中外的物理化学家、化学教育家和科技组织领导者——卢嘉锡先生。
卢嘉锡1930年考入厦门大学化学系，1945年回母校厦门大学任职。他是我国结构化学学科的开拓者和奠基人，培养了众多优秀学子，为中国化学领域输送了大批人才。其一生以科教兴国为己任，为我国科技进步和教育发展作出了不可磨灭的贡献。
晚年的卢嘉锡，曾笔书：“吾日三省吾身：为四化大局谋而不忠乎？与国内外同行们交流学术而乏创新乎？奖掖后进不落实乎？”卢嘉锡先生勇于开拓、勤于治学、乐于传道的品质，早已凝定为“卢嘉锡精神”，融入一代又一代厦大人的血脉之中，久久不息。
''')
admin.create_scenery_node(["xmu","signable"],"王亚南全身像","hot",8.5,"8:00-22.00","可以拍照",'''
在经济学院楼前的花坛正中央，矗立着已故校长王亚南铜像。王亚南是现代中国杰出的马克思主义经济学家和教育家，1950年出任厦门大学校长，任职长达19年。
王亚南极力倡导“我们应以中国人的资格来研究政治经济学”，倾力推动马克思主义经济学理论中国化，努力创建经济学的中国流派或具有中国特色的经济理论。他在风雨飘摇的年代，与郭大力同志耗尽十年心血，合译《资本论》三大卷，使得中国人终于有了研究经济的武器。
“先人骑鹤去，薪火有传人。”王校长成就卓越，春风化雨，哺育了无数英才，被誉为“一个懂得人的价值的经济学家”。他的经济思想、科学精神、育人理念经代代承继，已渗透于厦大人的思想深处，激励着生逢其时的厦大人在新的百年接续奋斗。
''')
admin.create_scenery_node(["xmu","signable"],"萨本栋全身像","hot",8.5,"8:00-22.00","可以拍照",'''
在厦大亦玄馆前，伫立着物理学家、电机工程专家、教育家萨本栋的塑像。萨本栋是厦门大学第一任校长。在抗战烽火中，他以一人之身，领全校之业，携全体师生内迁长汀，克服了校舍不足、经费短缺、师资匮乏等种种困难，筚路蓝缕、奋发图强，书写了“南方之强”的自强篇章。
萨本栋在艰危的时局中舍身治校，埋头苦干，以期拯救国家民族。他治校七年，成绩斐然，众口称颂。长汀岁月，是厦门大学办学史上最艰苦、最困乏的时期，但是，它却保存了完好的教育形式，对如今厦门大学的建设有着重要的启示意义。
站在新的历史起点，厦大人应矢志发扬以萨本栋校长为代表的自强精神，接续传递朴素坚韧的厦大传统，不畏艰难，始终奋进。
''')
admin.create_scenery_node(["xmu","signable"],"林文庆亭","hot",8.5,"8:00-22.00","可以拍照",'''
在图书馆大门后的一湾绿水旁，有个小亭子，名为林文庆亭。林文庆是厦门大学的第二任校长。1921年6月，林文庆博士应校主陈嘉庚先生之请，接掌厦门大学，倾其睿智才学，运筹操劳，主理校政十六载。1934年，校主经营的企业在世界经济危机的袭击下宣告破产，厦门大学濒于关闭，他毅然为陈嘉庚分忧，只身南渡，筹募经费，使厦大渡过难关。
2005年厦门大学校庆期间，文庆亭落成，亭上有对联：“禾山巍巍怀师德，鹭水泱泱见道心”。2008年厦大校庆期间，林文庆汉白玉雕像在文庆亭旁落成，雕像基座上镌刻了铭文《文庆亭记》：“一九二一年六月，林文庆博士应校主陈嘉庚先生之请，接掌厦门大学，倾其睿智才学，运筹操劳，主理校政十六载。学校事业蒸蒸日上，硕彦咸集，鸿才叠起，声名远播海内外，与公办名校并驾齐驱。”
文庆亭是为了追念任厦门大学校长达16年之久的林文庆先生，同时，文庆亭也时刻提醒着厦大人：追求至善始终如一，探寻真理永无止息。
''')
admin.create_scenery_node(["xmu","signable"],"厦门大学大南校门","hot",8.5,"8:00-22.00","可以拍照",'''
大南校门，与南普陀寺比邻，又称南校门。按标准方位来说，大南校门其实应该叫西北门，其名称中的“南”有两个说法，一是“沾”了南普陀寺的“光”，“大南”二字就取自于南普陀寺的“南”字；二是因紧靠建校之前的华侨建筑群——大南新村而取名。
大南校门是厦大最早也是最正式的大门。这座校门始建于1921年，2001年，为了庆祝厦门大学80周年校庆，学校在1921年大南校门旧址的基础上按原来的风格进行重建，校门呈欧式风格，由中式山墙和汉白玉圆柱构成，校门上方的“厦门大学”四字也是辑录于鲁迅手迹。
神佛前与山水间，自古以来都是远离尘世喧嚣、淡泊明志的好去处。大南校门在南普陀寺的旁边，给了厦大学子开了一扇进入象牙塔洗涤身心的门。如今，厦大历经岁月的洗练，取得了瞩目的教育成就，积淀了厚重的治学文化，为国家做出了杰出的贡献，大南校门也与南普陀寺一起成为了厦门市的标志性人文景观。
''')
admin.create_scenery_node(["xmu","signable"],"防空洞旧址","hot",8.5,"8:00-22.00","可以拍照",'''
厦门大学防空洞旧址，位于校园后的五老峰的花岗岩山体中。1954年，台湾海峡局势再次紧张，为了确保平时的安全教学，厦门大学于1954年下半年到1955年上半年，在各个建筑群和主要校舍之间挖筑半固定型的防空壕和遮掩体，形成防护网络，通往五老峰山下各个岩石防空洞。随着1958年8月23日，金门炮战的打响，厦门大学防空洞又担负起了抵御炮火的重任。1958年9月4日，为了进一步响应党中央和毛泽东主席的号召，建立全民皆兵的国防体系，厦门大学于防空洞内举行了民兵师成立仪式，王亚南校长担任师长，从此厦门大学师生便开始了边学习、便训练的半军事化生活，成为了祖国东南海防前线上的带枪的大学生。1979年发表《告台湾同胞书》后，两岸间的炮击停止，曾经承担保护厦大师生安全的防空洞也被闲置起来，并被改造成了供师生游览、休闲的去处。
遥想当年的五老峰山脚下，山洞里传出的是学子的朗朗书声，弦歌不辍地对抗着洞外的炮火连天。在那样严酷的环境下，厦大就像岩壁上的榕树，栉风沐雨，坚忍地生长着。厦门大学防空洞旧址展示了厦大师生的多难兴邦、艰苦奋斗、坚忍不拔的顽强意志，而那段“以洞为室”、“息心求学”的光阴也时刻提醒着我们要珍惜现在，不负时光。
''')
admin.create_scenery_node(["xmu","signable"],"湖心岛","hot",8.5,"8:00-22.00","可以拍照",'''
湖心岛位于芙蓉湖，通过芙蓉桥与陆地相连。岛上有一组名为《世纪的嘱托：陈嘉庚与学生》雕像。雕像落成于2001年厦门大学80周年校庆之际，是厦门大学校园文化的重要组成部分。
雕像打破时空的限制，分别以上世纪二三十年代、上世纪80年代以及当代大学生作为表现对象，呈现八十年的时空跨度。群像中心是嘉庚先生与一名当代学生促膝谈心，周围四名学生静心聆听、如受重托。雕像空间内外，摆设了一些石头，意在为当代和未来的大学生留出位置，让当代和未来的大学生都有机会围绕在陈嘉庚先生身边，聆听老人教诲，感受对于国家的责任。
《世纪的嘱托》体现了老一辈人的爱国精神及对青年的殷殷希望。陈嘉庚精神与学生永远在一起、与历史长存。
''')
admin.create_scenery_node(["xmu","signable"],"芙蓉二","hot",8.5,"8:00-22.00","可以拍照",'''
芙蓉楼群因陈嘉庚先生女婿李光前祖籍南安芙蓉村而得名，是嘉庚风格建筑走向成熟的标志。芙蓉二建成于1953年，楼群呈现半环状布局，主体三层，局部四层，是砖石木结构，楼面均为木结构上铺红色斗底砖，墙体用红色清水砖砌筑，花岗岩作装饰镶砌，建筑面积4820平方米。
1958年9月14日，厦门大学遭到轰炸，芙蓉二号楼损毁严重。在电视剧《换了人间》中，有这样一段真实的故事：伟大领袖毛主席和周恩来总理邀请请陈嘉庚先生到北京中南海商议重建，陈嘉庚先生执意去南洋募捐善款，重建厦门大学。如今的芙蓉二留存着当年模样，凝结着陈嘉庚与南洋华侨的心血。
''')
admin.create_scenery_node(["xmu","signable"],"厦门大学芙蓉四","hot",8.5,"8:00-22.00","可以拍照",'''
厦门大学芙蓉楼群取义于李光前的李氏家族聚居地南安芙蓉镇，芙蓉楼群共有五幢，以芙蓉湖为圆心形成半合围形，“自由空间”洒落营造出如同管弦乐般的节奏和韵律，有着流畅之美。芙蓉第四楼于1954年建成，位于东边社的东南一侧,用作学生宿舍。芙蓉四为西式，红瓦普通屋面，清水白石外墙，用料做工虽不及其他芙蓉楼考究，但造型朴素大方，简约粗粝，别具一格。
2016年9月15日凌晨，强台风“莫兰蒂”登陆厦门，来势汹汹，肆虐破坏。在防抗台风中，师生们共同抢险救灾，为恢复最美校园所做的努力让人动容。为纪念厦大人众志成城，群策群力，一起面对风雨、共抗风暴的精神，厦大保留了芙蓉四前被台风损毁的百年老树废墟，希望将这种爱校精神、人文之花永久镌刻在每个厦大人的心中。
''')
admin.create_scenery_node(["xmu","signable"],"三家村广场","hot",8.5,"8:00-22.00","可以拍照",'''
三家村广场是学校重要的三叉路口，无论是要去教学楼、南光食堂、自钦楼学生活动中心，或是芙蓉、石井公寓楼群都要从三家村广场经过。
提到三家村，大家心中一定有一连串的疑问，学校里为什么会有村子？三家又是哪三家呢？原来，当年嘉庚先生买下五老峰下的荒凉之地，辟为厦大校园，散居在附近的农民并没有迁走，仍靠种田种菜为生。校园中鸡犬相闻，农民与教授每天擦肩而过，成“校中村，村中校”独特景象。据说直到77级学生入校的时候，还能看见芙蓉湖畔的水稻和上弦场上的地瓜。
据校友叶雪音介绍，“三家村”原来是一座位于芙蓉湖畔的小院子，其后是一片村民的池塘菜地。院中有一幢浅黄色欧式住宅，由三个单元构成，学校将其分配给了经济系、历史系和化学系的三位教授居住。历史系教授叶国庆将此宅命名为“三家村”。
我们今天见到的三家村广场，已远远不同于当年。在自钦楼学生活动中心改造完成后，此处基本形成统一的嘉庚建筑风格。为了营造更加优美和谐的校园环境，校领导又对三家村进行改造，拆除周围的老旧建筑，建成我们现在看到的学生活动广场。
尽管建筑的外在形态变了，一代又一代厦大学子的情谊依然在这里生生不息。2020年12月5日，厦门大学百年校庆志愿者招募启动仪式在三家村广场举行，两千多位同学踊跃报名。这里仿佛一个时间隧道，联通了旧日学子的激情浪漫，和当今青年人的奋进拼搏。一以贯之的，是对校园的依恋，对祖国的热爱，对时代责任的担当。
''')
admin.create_scenery_node(["xmu","signable"],"芙蓉一","hot",8.5,"8:00-22.00","可以拍照",'''
围绕着芙蓉湖畔的几座红墙绿瓦的芙蓉一、一、三芙蓉楼群，建于20世纪50年代，是嘉庚风格建筑走向成熟的标志，强调西体中用，更多地增加闽南建筑的元素，突出民族特色。中式屋顶、西式屋身的外廊建筑样式所显示的中西结合的优美建筑群形象，以红、绿色为主，白色为辅，在芙蓉湖的映衬下，色彩斑斓，犹如出水芙蓉，悠然卓立，随风揉碎的倒影留在了波光粼粼的湖面上。
其中，芙蓉第一楼位于博学楼北面，于1951年最早完成。砖石木结构，四层，面阔118米、进深12米、通高15米。占地面积1154平方米、建筑面积3457平方米、使用面积1836平方米。造价156319.69万元。取意于李光前的李氏家族聚居地南安芙蓉镇，楼名“芙蓉”，用作学生宿舍。
''')
admin.create_scenery_node(["xmu","signable"],"人类学博物馆","hot",8.5,"8:00-22.00","可以拍照",'''
厦门大学人类博物馆是中国大陆最早的一所人类学专科博物馆。早在1926年秋，鲁迅在校时就举办考古文物展览会，后在国学院成立文化陈列所。1934年，我国人类学家林惠祥教授创办厦门市人类博物馆筹备处。解放后，林惠祥教授将多年收集、收藏的极为珍贵的海内外文物全部捐赠给厦门大学。1951年经教育部批准，正式成立厦门大学人类博物馆。1953年3月16日，厦门大学人类博物馆正式开馆，徐悲鸿特地为博物馆题写馆名。如今，该馆不仅在中国及东南亚享有盛誉，而且被联合国教科文组织收录为国际著名博物馆之一。
厦门大学人类博物馆共有七个展室和一个碑廊，现藏文物八千多件，展出文物分为人类及其文化的起源与进化、中国民族史、中外民族文物和碑廊四个部分，包括中国文明史各阶段的文物标本，以及中国少数民族与民俗文物、东南亚大洋洲民族考古文物，以及体现环中国海海洋文明史的来自西、南亚的宗教石刻。其中尤为特别的是新中国成立前，林惠祥从台湾调查收集的一批石器和少数民族文物，为台湾自古以来就是我国领土提供了重要的实物依据。
厦门大学人类博物馆厦门大学重要的教学与科研场所，同时是福建省和厦门市重要的科普教育基地，发挥了重要的知识普及教育功能。
''')
admin.create_scenery_node(["xmu","signable"],"鲁迅雕像","hot",8.5,"8:00-22.00","可以拍照",'''
鲁迅（1881年9月25日－1936年10月19日），原名周树人，浙江绍兴人，中国现代伟大的无产阶级文学家、思想家和革命家。1926年9月至1927年1月，鲁迅在厦门大学任国文系与国学研究院教授。鲁迅在厦大任教期间，讲授和编写了《中国文学史》和《汉文学史纲》，创作《故事新编》中的《铸剑》、《奔月》，写下了家喻户晓、脍炙人口的散文《从百草园到三味书屋》等，共约17万字，并作了五次演讲。
当年在鲁迅指导下创办的学生刊物《鼓浪》，至今也已有95年的历史。“鼓浪”一词寄予了鲁迅对厦大学子的殷切期望，希望青年们可以“鼓起时代的浪潮”。时隔近一个世纪，鲁迅雕像屹立在新时代的厦大校园里，仿佛仍在见证着今日的莘莘学子成长为新时代的国家人才，鼓起新时代的浪潮。
''')
admin.create_scenery_node(["xmu","signable"],"罗扬才烈士墓","hot",8.5,"8:00-22.00","可以拍照",'''
罗扬才烈士墓，坐落在厦门大学建南大会堂北后方边坡，于1987年9月17日与革命烈士陵园一同落成，寄托了后人对罗扬才等烈士的怀念。罗扬才烈士是厦门市第一位共产党员，是厦门共产党组织最早的领导人之一，是第一次国内革命战争时期厦门工人运动和学生运动杰出的领袖，是福建革命历史上一面闪光的旗帜。在血雨腥风、白色恐怖的岁月，他最终英勇地牺牲在敌人的屠刀之下，年仅22岁。
罗扬才烈士短暂的一生闪耀着共产主义的光辉，展现了大无畏的英雄气概。以罗扬才烈士为代表的革命精神是厦门大学“四种精神”的重要组成部分，铸就了“南方之强”的筋骨和气度，深深融入厦大师生的文化血脉，成为推动学校持续发展的不竭动力。
每年清明节和中国烈士纪念日，厦大师生都会到革命烈士陵园敬献花篮，缅怀为中国人民解放事业作出牺牲的罗扬才等烈士。这成为厦大开展思想政治教育的有效载体，增强了厦大师生的历史使命感和责任感，促进了红色革命精神的传承、发扬，激励了新时代青年人投身到中国特色社会主义事业的建设中。
''')
admin.create_scenery_node(["xmu","signable"],"萨本栋携夫人墓","hot",8.5,"8:00-22.00","可以拍照",'''
萨本栋携夫人墓位于成义楼后面，由多地厦大校友会共同捐赠修建，于1991年3月竣工。1937年萨本栋先生被任命为任国立厦门大学第一任校长，在抗战爆发、该校内迁长汀办学的艰难环境下，带领全校师生发愤图强，厦大因此成为当时粤汉铁路线以东唯一的国立大学，也是最逼近战区的国立大学，撑起了中华民族高等教育的东南半壁。萨本栋离任后，厦门大学设立了多个以其命名的奖学金。萨本栋在遗嘱中希望将骨灰献给北京清华大学、国立厦门大学，或送给南京中央研究院。厦门大学表达了强烈愿望，请求全部接受萨本栋骨灰。经夫人黄淑慎同意，将萨本栋骨灰全部安葬在厦门大学校园内。
校长萨本栋受命危难，精心迁校；披荆斩棘，呕心沥血；无私奉献，倾智办学；鞠躬尽瘁，死犹未已，以高尚人格赢得全体师生的尊敬，成了厦大长汀艰苦办学自强精神的代表。厦大内迁办学是一部爱国的历史、创业的历史和图强的历史。内迁长汀办学时期厦大形成的艰苦办学的自强精神，已经成为厦门大学宝贵的精神财富，成为厦大继往开来、生生不息的内在原因和强大动力。当前，厦大面临着“双一流”建设的历史重任，艰苦奋斗的优良品格与自强不息的精神将不断感召、激励着厦大人追求真理、艰苦奋斗、严谨治学、勇攀高峰。
''')
admin.create_scenery_node(["xmu","signable"],"建南大会堂","hot",8.5,"8:00-22.00","可以拍照",'''
建南大会堂属于建南楼群，于1952年开工，1954年竣工，和南安、南光、成智、成义楼共同构成了“一主四从”、半月状环绕上弦场的布局。建南大会堂是陈嘉庚先生亲自参与设计、督建，由女婿李光前先生为主的福建南安华侨捐资而建的，建筑精细巧妙，呈现中西合璧式建筑特征，坐北朝南，总体可分为两部分：南部为办公楼，也是建筑的主入口；北部为礼堂主体，包括观众厅和舞台。楼顶则有钟楼，每天19次由人工敲响进行报时。
建南大会堂底层入门廊处到厅里有两组石板台阶踏步，外面五级，里面三级，总合起来八级。这样的设计意图据说出自于陈嘉庚，以此纪念经历过八年抗战与三年解放战争的艰苦奋战，中国人民站起来了，警示师生胜利来之不易，更应奋发图强。建南大会堂底层门廊入大厅，中间的大门的拱塞用辉绿岩雕刻着龙虎图案，象征龙虎把大门，坚固无比，谁敢来侵犯，最后都要碰得头破血流。
建南大会堂作为第六批全国重点文物保护单位，彰显了我国悠久的历史文明和极为丰富的文化遗产，蕴含着中华民族特有的精神价值、思维方式、想象力，体现着中华民族的生命力和创造力。保护和利用好建南大会堂，对于继承、发扬嘉庚精神和民族优秀文化传统，增强师生的民族自信心和凝聚力，具有重要而深远的意义。
''')
print("创建成功")