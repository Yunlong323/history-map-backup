
$(function () {
    to_page(1);
});


function to_page(pageNum) {

    var data = {
        status: $('#status').val(),
        name: $('#name').val(),
        p:pageNum
    };

    $.ajax({
        url: common_ops.buildUrl("/venue/getVenueList"),
        data:data,
        type: "POST",
        dataType: "json",
        success: function (data) {
            //解析并显示数据表
            build_table(data);
            //解析并显示分页数据
            build_page_nav(data);
        },fail:function(err){
            console.log(err);
        }
    })

    function build_table(data) {
        //清空table表格
        $("#venue_table tbody").empty();
        var venue = data.list;
        // console.log(venue);
        if(venue.length==0){
            var item=$("<td></td>").attr("colspan","7").append("暂无数据");
            $("<tr></tr>").append(item).appendTo("#venue_table tbody");
            return;
        }
        var offset = (data.pages.current-1)*data.pages.page_size
        //遍历元素
        $.each(venue, function (index, item) {

            var seq = $("<td></td>").append(index+1+offset);
            var name = $("<td class='venue'></td>").append(item.name);
            var lon = $("<td></td>").append(item.lon);
            var lat = $("<td></td>").append(item.lat);

            var status = "<td><div class='switch'><div class='onoffswitch'><input type='checkbox'";
            if(item.status==1)
                status+=" checked "
            status += "class='onoffswitch-checkbox' id="+item.id+"><label class='onoffswitch-label' for="+item.id+"><span class='onoffswitch-inner'></span><span class='onoffswitch-switch'></span></label></div></div></td>";

            var createtime = $("<td></td>").append(item.createtime);

            var a1=$("<a></a>").attr("title","白名单").addClass("whitelist").attr("id", item.id).attr("name", item.name).append($("<i></i>")).addClass("fa fa-list-alt fa-lg");

            if(data.super==1){
                var a2=$("<a></a>").attr("title","管理员").addClass("m-l adminlist").attr("id", item.id).attr("name", item.name).append($("<i></i>")).addClass("fa fa-user fa-lg");
            }

            var a3=$("<a></a>").attr("title","编辑").addClass("m-l editVenue").attr("id", item.id).attr("name", item.name).attr("lat", item.lat).attr("lon", item.lon).attr("permissionType", item.permissionType).append($("<i></i>")).addClass("fa fa-edit fa-lg");

            var a4=$("<a></a>").attr("title","流量统计").addClass("m-l getVenueStatistics").attr("id", item.id).attr("name", item.name).append($("<i></i>")).addClass("fa fa-line-chart fa-lg");

            var a5=$("<a></a>").attr("title","场所定位").addClass("m-l redirectVenue").attr("id", item.id).attr("name", item.name).append($("<i></i>")).addClass("fa fa-location-arrow fa-lg");

            var a6=$("<a></a>").attr("title","小程序码").addClass("m-l getWXcode").attr("id", item.id).attr("name", item.name).append($("<i></i>")).addClass("fa fa-qrcode fa-lg");

            if(data.super==1){
                var op=$("<td></td>").append(a1).append(a2).append(a3).append(a4).append(a5).append(a6);
            }else{
                var op=$("<td></td>").append(a1).append(a3).append(a4).append(a5).append(a6);
            }
            
            $("<tr></tr>").append(seq).append(name).append(lon).append(lat).append(status).append(createtime).append(op).appendTo("#venue_table tbody");
        })
    }

    function build_page_nav(data) {
        var pages=data.pages;
        $("#pagination .col-lg-12 span").empty();
        $("#pagination .col-lg-12 span").append("共"+pages.total +"条记录 | 每页"+pages.page_size+"条");
        var dom=$("#pagination .col-lg-12 ul");
        dom.empty();

        if(pages.is_prev == 1){
            var itemFirst=$("<li></li>").append(($("<a></a>")).attr("href","#").append(($("<span></span>")).append("首页")));

            itemFirst.click(function () {
                to_page(1);
            });

            dom.append(itemFirst);
        }


        var range=[];
        for(var i=pages.from;i<pages.end+1;i++){
            range=range.concat(i);
        }

        $.each(range, function (index, item) {
            if(item==pages.current){
                var temp=$("<li></li>").addClass("active").append($("<a></a>").attr("href","#").append(item));
                dom.append(temp);
            }else{
                var temp=$("<li></li>").append($("<a></a>").attr("href","#").append(item));

                temp.click(function () {
                    to_page(item);
                });
                dom.append(temp);
            }
        });

        if(pages.is_next == 1){
            var itemLast=$("<li></li>").append(($("<a></a>")).attr("href","#").append(($("<span></span>")).append("尾页")));

            itemLast.click(function () {
                to_page(pages.total_pages);
            });

            dom.append(itemLast);
        }
    }
}


//搜索
$(".wrap_search .search").click(function () {
    to_page(1);
});

//启用禁用
$("#venue_table").on("click",".onoffswitch-checkbox",function(){

    var id=$(this).attr("id");
    $('#loading').modal('show');

    $.ajax({
        url: common_ops.buildUrl("/venue/reverseStatus"),
        type: "POST",
        data : {"id":id},
        dataType: "json",
        
        success : function(result) {
            $('#loading').modal('hide');
            if(result.code!=200)
                common_ops.alert(result.msg);
        },
        error : function(errorMsg) {
            console.log(errorMsg);
            $('#loading').modal('hide');
        }
    });
});


//新增场所模态框
$("#addVenue").click(function () {

    // $("#VenueModal").modal({backdrop: "static"})//点击空白处不能关闭模态框
    $("#VenueModal").modal()//点击空白处能关闭模态框

    $("#VenueModal .modal-dialog .modal-content .modal-header .modal-title").html("新增场所");
    $("#venue_name").val("");
    $("#id_id").attr("value","");
    $("#id_lon").attr("value","");
    $("#id_lat").attr("value","");
    $("#permissionType").val(1);
    initMap(0,0);
});

//编辑场所模态框
$("#venue_table").on("click",".editVenue",function(){

    $("#VenueModal").modal()//点击空白处不能关闭模态框

    var id=$(this).attr("id");
    var name=$(this).attr("name");
    var lat=$(this).attr("lat");
    var lon=$(this).attr("lon");
    var permissionType=$(this).attr("permissionType");
    $("#VenueModal .modal-dialog .modal-content .modal-header .modal-title").html("编辑场所");
    $("#venue_name").val(name);
    $("#id_id").attr("value",id);
    $("#id_lon").attr("value",lon);
    $("#id_lat").attr("value",lat);
    $("#permissionType").val(permissionType);

    initMap(lon,lat);
});


// //展示地图
// function initMap(lon,lat){

//     //初始化百度地图
//     var map = new BMap.Map("map",{enableMapClick:false});//new 一个地图对象 

//     if(lon==0 && lat==0){//新增
//         var point=new BMap.Point(118.103106,24.444323);        //设置地图的中心点
//     }else{//修改
//         var point=new BMap.Point(lon,lat);        //设置地图的中心点
//         var myIcon = new BMap.Icon("https://passport.xmu.edu.cn/static/images/common/map_icon.png", new BMap.Size(36,36));
//         var marker = new BMap.Marker(point,{icon:myIcon});  // 创建标注
//         map.addOverlay(marker);              // 将标注添加到地图中
//         marker.setAnimation(BMAP_ANIMATION_BOUNCE); 
//     }

//     var zoom=16;                                            //设置地图的等级
//     map.centerAndZoom(point, zoom);                         // 在地图中显示
//     map.panBy(350, 250);//中心点偏移多少像素(width,height)为div 宽高的1/2;
//     map.enableScrollWheelZoom();                 //启用滚轮放大缩小
//     map.enableContinuousZoom();         //启用地图惯性拖拽，默认禁用
//     map.enableAutoResize();//设置当地图容器发生改变时地图自动适应

//     map.addEventListener("click",function(e){    //给地图添加点击事件
//         map.clearOverlays();                   
//         var lng=e.point.lng;
//         var lat=e.point.lat;
//         //创建标注位置
//         var pt = new BMap.Point(lng,lat);
//         var myIcon = new BMap.Icon("https://passport.xmu.edu.cn/static/images/common/map_icon.png", new BMap.Size(36,36));
//         var marker = new BMap.Marker(pt,{icon:myIcon});  // 创建标注
//         map.addOverlay(marker);              // 将标注添加到地图中
//         marker.setAnimation(BMAP_ANIMATION_BOUNCE); 
//         $("#id_lon").attr("value",lng);
//         $("#id_lat").attr("value",lat);
//     });
// }


//新增或保存
$("#saveVenue").click(function () {

    var id=$("#id_id").attr("value");
    var name=$("#venue_name").val();
    var lat=$("#id_lat").attr("value");
    var lon=$("#id_lon").attr("value");
    var permissionType=$("#permissionType").val();

    if (name=="") {
        common_ops.tip("请输入场所名称","#venue_name");
        return;
    }

    if (lon == "" || lat == "") {
        common_ops.alert("请选择场所地点");
        return;
    }

    var data = {
        name: name,
        lon: lon,
        lat: lat,
        id: id,
        permissionType: permissionType,
    };
    console.log(data);

    $.ajax({
        url: common_ops.buildUrl("/venue/editVenue"),
        type: "POST",
        data: data,
        dataType: "json",
        success: function (res) {
            if (res.code == 200) {
                if(id==''){//新增
                    console.log(res.wxCodeUrl);
                    $('#VenueModal').modal('hide');
                    //小程序码modal
                    $("#wxCodeModal").modal()
                    $("#venueName").html(name);
                    $("#WXcode").attr("src",res.wxCodeUrl);
                    to_page(1)
                }else{//修改
                    $('#VenueModal').modal('hide');
                    common_ops.successTip("保存成功");
                    // 刷新当前页
                    var currentPage =$("#pagination .active").text();
                    to_page(currentPage)
                }
            }else{
                common_ops.alert(res.msg);
            }
        },fail:function(err){
            common_ops.alert(err);
        }
    })
});


//显示小程序码
$("#venue_table").on("click",".getWXcode",function(){

    var id=$(this).attr("id");
    var name=$(this).attr("name");
    var wxCodeUrl = common_ops.buildUrl("/static/images/WXcode/"+id+".jpeg");
    
    $("#wxCodeModal").modal();
    $("#venueName").html(name);
    $("#WXcode").attr("src",wxCodeUrl);
});


//显示流量统计
$("#venue_table").on("click",".getVenueStatistics",function(){

    var id=$(this).attr("id");
    var name=$(this).attr("name");
    
    var myChart = echarts.init(document.getElementById('chart'));

    myChart.setOption(
    {
        title: {
            text: name+' 流量统计',
            x:'center',
            textStyle: {
                fontWeight: 'normal',
                fontSize: 16,
            }
        },
        tooltip: {
            trigger: 'axis',
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [{
            type: 'category',
            boundaryGap: false,
            data: []
        }],
        yAxis: [{
            type: 'value',
            name: '人次',
            axisTick: {
                show: false
            },
            axisLabel: {
                margin: 10,
                textStyle: {
                    fontSize: 14
                }
            },
        }],
        series: [{
            type: 'line',
            smooth: true,
            symbol: 'circle',
            symbolSize: 5,
            showSymbol: false,
            lineStyle: {
                normal: {
                    width: 1
                }
            },
            areaStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: 'rgba(219, 50, 51, 0.3)'
                    }, {
                        offset: 0.8,
                        color: 'rgba(219, 50, 51, 0)'
                    }], false),
                    shadowColor: 'rgba(0, 0, 0, 0.1)',
                    shadowBlur: 10
                }
            },
            itemStyle: {
                normal: {
                    color: 'rgb(219,50,51)',
                    borderColor: 'rgba(219,50,51,0.2)',
                    borderWidth: 12
                }
            },
            data: []
        }, ]
    });

    $("#chartModal").modal()//点击空白处可以关闭模态框
    myChart.showLoading();

    var names=[];    //数组 X坐标值
    var nums=[];    //数组 Y坐标值

    $.ajax({
        url: common_ops.buildUrl("/venue/getVenueStatistics"),
        type: "POST",
        data : {"id":id},
        dataType: "json",
        
        success : function(result) {
            myChart.hideLoading();    //隐藏加载动画
            if (result.data) {
                for(var i=0;i<result.data.length;i++){
                    names.push(result.data[i].day);
                }
                for(var i=0;i<result.data.length;i++){
                    nums.push(result.data[i].count);
                }
                myChart.setOption({        //加载数据图表
                    xAxis: {
                        data: names
                    },
                    series: [{
                        data: nums
                    }]
                });
            }
        },
        error : function(errorMsg) {
            myChart.hideLoading();
            console.log(errorMsg);
            common_ops.alert("图表请求数据失败");
        }
    });
});


//场所定位
$("#venue_table").on("click",".redirectVenue",function(){

    var venue=$(this).attr("name");
    // window.location.href = common_ops.buildUrl("/track/index");
    if (window.localStorage) {
        //存储变量的值
        localStorage.name = venue;
        location.href = common_ops.buildUrl("/track/index");
    } else {
        alert("NOT SUPPORT");
    }
});


////////////////////////////////////白名单////////////////////////////////////
//白名单Modal
//白名单版本管理
$("#venue_table").on("click",".whitelist",function(){
    var id=$(this).attr("id");
    var name=$(this).attr("name");
    // console.log(id+"=="+name);
    $("#id_venue_name_whitelist").html(name+"&nbsp;&nbsp;&nbsp;&nbsp;白名单");
    $("#name_whitelist_id").val(id);

    //清空表格
    $('#id_tag-list tbody').empty();

    $("#WhiteListManageModal").modal();
    showTagList();
});

function showTagList(){

    id=$("#name_whitelist_id").val();
    // 获取所有tag
    $.ajax({
        url: common_ops.buildUrl("/venue/getWhiteListTagsDetail"),
        data:{id:id},
        type: "POST",
        dataType: "json",
        success: function (data) {

            //清空list
            $('#id_tag-list tbody').empty();

            var taglist = data.list;

            if(taglist.length==0){
                var item=$("<td></td>").attr("colspan","6").append("暂无数据");
                $("<tr></tr>").append(item).appendTo("#id_tag-list tbody");
                return;
            }

            //遍历元素
            $.each(taglist, function (index, item) {

                var seq = $("<td></td>").append(index+1);
                var tag = $("<td></td>").append(item.tag);
                var count = $("<td></td>").append(item.count);
                //状态

                var status = "<td><div class='switch'><div class='onoffswitch'><input type='checkbox'";
                if(item.active==1)
                    status+=" checked "
                status += "class='onoffswitch-checkbox' id="+item.id+"><label class='onoffswitch-label' for="+item.id+"><span class='onoffswitch-inner'></span><span class='onoffswitch-switch'></span></label></div></div></td>";

                var time = $("<td></td>").append(item.time);
                
                var a1=$("<a></a>").attr("title","详情").addClass("tag-list").attr("tag_id", item.id).append($("<i></i>")).addClass("fa fa-eye fa-lg");

                var a2=$("<a></a>").attr("title","删除").addClass("m-l tag-delete").attr("tag_id", item.id).append($("<i></i>")).addClass("fa fa-trash fa-lg");

                var op=$("<td></td>").append(a1).append(a2);

                $("<tr></tr>").append(seq).append(tag).append(count).append(status).append(time).append(op).appendTo("#id_tag-list tbody");
            })

            // class='link tag-update' tag_id="+data.list[i].id+">禁用

            // $('#id_tag-list').append("<div class='tag-item add'><div class='tag-new'><i class='fa fa-plus'></i><div class='text'>上传白名单</div></div></div>");

        },fail:function(err){
            console.log(err);
        }
    })
}


function to_whitelist_page(id,pageNum) {

    // var tagID=$('#id_tag_select').val();
    var tagID=$('#whitelist_tag_id').val();
    var dept=$('#id_dept').val();
    var no=$('#id_no').val();
    var name=$('#id_name').val();

    var data = {
        tagID: tagID,
        id: id,
        dept: dept,
        no: no,
        name: name,
        p:pageNum
    };

    $.ajax({
        url: common_ops.buildUrl("/venue/getWhiteList"),
        data:data,
        type: "POST",
        dataType: "json",
        success: function (data) {
            //解析并显示数据表
            build_table(data);
            //解析并显示分页数据
            build_page_nav(data);
        },fail:function(err){
            console.log(err);
        }
    })

    function build_table(data) {
        $("#whitelist_table tbody").empty();
        var whitelist = data.list;

        if(whitelist.length==0){
            var item=$("<td></td>").attr("colspan","5").append("暂无数据");
            $("<tr></tr>").append(item).appendTo("#whitelist_table tbody");
            return;
        }
        var offset = (data.pages.current-1)*data.pages.page_size
        //遍历元素
        $.each(whitelist, function (index, item) {

            var seq = $("<td></td>").append(index+1+offset);
            var dept = $("<td></td>").append(item.dept);
            var no = $("<td></td>").append(item.no);
            var name = $("<td></td>").append(item.name);
            
            var a=$("<a></a>").attr("title","删除").addClass("deleteWhiteNo").attr("no", item.no).append($("<i></i>")).addClass("fa fa-trash fa-lg");

            var op=$("<td></td>").append(a);

            $("<tr></tr>").append(seq).append(dept).append(no).append(name).append(op).appendTo("#whitelist_table tbody");
        })
    }

    function build_page_nav(data) {
        var pages=data.pages;
        $("#pagination_whitelist .col-lg-12 span").empty();
        $("#pagination_whitelist .col-lg-12 span").append("共"+pages.total +"条记录 | 每页"+pages.page_size+"条");
        var dom=$("#pagination_whitelist .col-lg-12 ul");
        dom.empty();

        if(pages.is_prev == 1){
            var itemFirst=$("<li></li>").append(($("<a></a>")).attr("href","#").append(($("<span></span>")).append("首页")));

            itemFirst.click(function () {
                to_whitelist_page(id,1);
            });

            dom.append(itemFirst);
        }


        var range=[];
        for(var i=pages.from;i<pages.end+1;i++){
            range=range.concat(i);
        }

        $.each(range, function (index, item) {
            if(item==pages.current){
                var temp=$("<li></li>").addClass("active").append($("<a></a>").attr("href","#").append(item));
                dom.append(temp);
            }else{
                var temp=$("<li></li>").append($("<a></a>").attr("href","#").append(item));

                temp.click(function () {
                    to_whitelist_page(id,item);
                });
                dom.append(temp);
            }
        });

        if(pages.is_next == 1){
            var itemLast=$("<li></li>").append(($("<a></a>")).attr("href","#").append(($("<span></span>")).append("尾页")));

            itemLast.click(function () {
                to_whitelist_page(id,pages.total_pages);
            });

            dom.append(itemLast);
        }
    }
}


//tag的具体名单
$("#id_tag-list").on("click",".tag-list",function(){
    var tagID=$(this).attr("tag_id");
    var id=$("#name_whitelist_id").val();
    // var name=$(this).attr("tag_name");
    // console.log(tagID+'+++tail++'+id);
    // return;
    
    //搜索框清空
    $('#id_dept').val("");
    $('#id_no').val("");
    $('#id_name').val("");

    //清空table表格
    $("#whitelist_table tbody").empty();
    
    $("#WhiteListModal").modal();
    // $("#id_tag_venue_name_whitelist").html(name);
    $("#whitelist_venue_id").val(id);
    $("#whitelist_tag_id").val(tagID);

    to_whitelist_page(id,1);
});

//改变tag状态
$("#id_tag-list").on("click",".onoffswitch-checkbox",function(){

    var tagID=$(this).attr("id");
    var id=$("#name_whitelist_id").val();
    // console.log(tagID+'+++++'+id);
    // return;
    $('#loading').modal('show');
    
    var data = {
        tagID:tagID,
        id: id,
    };

    $.ajax({
        url: common_ops.buildUrl("/venue/reverseTagStatus"),
        type: "POST",
        data: data,
        dataType: "json",
        success: function (res) {
            $('#loading').modal('hide');
            if (res.code == 200) {
                common_ops.successTip("操作成功");
                // 刷新当前页
                showTagList();
            }else{
                common_ops.alert(res.msg);
            }
        },fail:function(err){
            $('#loading').modal('hide');
            common_ops.alert(err);
        }
    })
});


//删除tag
$("#id_tag-list").on("click",".tag-delete",function(){

    var tagID=$(this).attr("tag_id");
    var id=$("#name_whitelist_id").val();
    
    // console.log(tagID+'+++delete++'+id);
    // return;

    common_ops.alert("确认删除吗?",function(){
        
        var data = {
            tagID:tagID,
            id: id,
        };

        $.ajax({
            url: common_ops.buildUrl("/venue/deleteTag"),
            type: "POST",
            data: data,
            dataType: "json",
            success: function (res) {
                if (res.code == 200) {
                    common_ops.successTip("删除成功");
                    // 刷新当前页
                    showTagList();
                }else{
                    common_ops.alert(res.msg);
                }
            },fail:function(err){
                common_ops.alert(err);
            }
        })
    });
});


//添加tag:上传白名单
$("#btn_whitelist").click(function(){
    var id=$("#name_whitelist_id").val();
    
    // console.log('add+++'+id);
    layer.prompt({title: "请输入批次名"},function(tagname, index){
        $("#add_tag_name").val(tagname);
        $("#whitelistFile").click();
        layer.close(index);
    });
})

//上传白名单
$(".upload_whitelist_wrap").change(function () {

    var formData = new FormData();
    var tag_name=$('#add_tag_name').val();
    var id=$("#name_whitelist_id").val();

    formData.append('file', $('#whitelistFile')[0].files[0]);
    formData.append('tag_name',tag_name );
    formData.append('venue_id',id );
    $('#whitelistFile').val('');//及时清空避免二次选择同一文件不能触发change事件

    $.ajax({
        url: common_ops.buildUrl("/venue/uploadWhitelist"),
        type: "POST",
        cache: false,
        processData: false,
        contentType: false,
        data: formData,
        success: function (res) {
            if (res.code == 200) {
                common_ops.successTip("操作成功");
                showTagList();
            }else{
                common_ops.alert(res.msg);
            }
        },fail:function(err){
            common_ops.alert(err);
        }
    })
});


//搜索白名单
$(".wrap_whitelist_search .search").click(function () {
    var id = $("#whitelist_venue_id").val();
    to_whitelist_page(id,1);
});


//新增单个白名单学工号
$("#addWhiteNo").click(function () {

    var tagID=$('#whitelist_tag_id').val();
    var venue_id = $("#whitelist_venue_id").val();

    layer.prompt({title: "请输入学工号"},function(no, index){

        var data = {
            tagID:tagID,
            venue_id: venue_id,
            no: no,
        };

        $.ajax({
            url: common_ops.buildUrl("/venue/addWhiteNo"),
            type: "POST",
            data: data,
            dataType: "json",
            success: function (res) {
                if (res.code == 200) {
                    common_ops.successTip("添加成功");
                    // 刷新当前页
                    var currentPage = $("#pagination_whitelist .active").text();
                    to_whitelist_page(venue_id,currentPage)
                }else{
                    common_ops.alert(res.msg);
                }
                layer.close(index);
            },fail:function(err){
                common_ops.alert(err);
                layer.close(index);
            }
        })
    });
});

//删除单个白名单学工号
$("#whitelist_table").on("click",".deleteWhiteNo",function(){

    var tagID=$('#whitelist_tag_id').val();
    var venue_id = $("#whitelist_venue_id").val();
    var no=$(this).attr("no");

    common_ops.alert("确认删除吗?",function(){
        
        var data = {
            tagID:tagID,
            venue_id: venue_id,
            no: no,
        };

        $.ajax({
            url: common_ops.buildUrl("/venue/deleteWhiteNo"),
            type: "POST",
            data: data,
            dataType: "json",
            success: function (res) {
                if (res.code == 200) {
                    common_ops.successTip("删除成功");
                    // 刷新当前页
                    var currentPage = $("#pagination_whitelist .active").text();
                    to_whitelist_page(venue_id,currentPage)
                }else{
                    common_ops.alert(res.msg);
                }
            },fail:function(err){
                common_ops.alert(err);
            }
        })
    });
});

////////////////////////////////////白名单////////////////////////////////////



////////////////////////////////////场所管理员////////////////////////////////////
//场所管理员Modal
$("#venue_table").on("click",".adminlist",function(){
    var id=$(this).attr("id");
    var name=$(this).attr("name");

    //搜索框清空
    $('#id_admin_dept').val("");
    $('#id_admin_no').val("");
    $('#id_admin_name').val("");

    //清空table表格
    $("#adminlist_table tbody").empty();

    $("#AdminListModal").modal();
    $("#id_venue_name_adminlist").html(name+"&nbsp;&nbsp;&nbsp;&nbsp;场所管理员");
    $("#name_adminlist_id").val(id);
    
    to_adminlist_page(id,1);
});


function to_adminlist_page(id,pageNum) {

    var dept=$('#id_admin_dept').val();
    var no=$('#id_admin_no').val();
    var name=$('#id_admin_name').val();

    var data = {
        id: id,
        dept: dept,
        no: no,
        name: name,
        p:pageNum
    };

    $.ajax({
        url: common_ops.buildUrl("/venue/getAdminList"),
        data:data,
        type: "POST",
        dataType: "json",
        success: function (data) {
            if(data.code==200){
                //解析并显示数据表
                build_table(data);
                //解析并显示分页数据
                build_page_nav(data);
            }else{
                common_ops.alert(data.msg);
            }
        },fail:function(err){
            console.log(err);
        }
    })

    function build_table(data) {
        $("#adminlist_table tbody").empty();
        var adminlist = data.list;

        if(adminlist.length==0){
            var item=$("<td></td>").attr("colspan","5").append("暂无数据");
            $("<tr></tr>").append(item).appendTo("#adminlist_table tbody");
            return;
        }
        var offset = (data.pages.current-1)*data.pages.page_size
        //遍历元素
        $.each(adminlist, function (index, item) {

            var seq = $("<td></td>").append(index+1+offset);
            var dept = $("<td></td>").append(item.dept);
            var no = $("<td></td>").append(item.no);
            var name = $("<td></td>").append(item.name);
            
            var a=$("<a></a>").attr("title","删除").addClass("deleteAdminNo").attr("no", item.no).append($("<i></i>")).addClass("fa fa-trash fa-lg");

            var op=$("<td></td>").append(a);

            $("<tr></tr>").append(seq).append(dept).append(no).append(name).append(op).appendTo("#adminlist_table tbody");
        })
    }

    function build_page_nav(data) {
        var pages=data.pages;
        $("#pagination_adminlist .col-lg-12 span").empty();
        $("#pagination_adminlist .col-lg-12 span").append("共"+pages.total +"条记录 | 每页"+pages.page_size+"条");
        var dom=$("#pagination_adminlist .col-lg-12 ul");
        dom.empty();

        if(pages.is_prev == 1){
            var itemFirst=$("<li></li>").append(($("<a></a>")).attr("href","#").append(($("<span></span>")).append("首页")));

            itemFirst.click(function () {
                to_adminlist_page(id,1);
            });

            dom.append(itemFirst);
        }


        var range=[];
        for(var i=pages.from;i<pages.end+1;i++){
            range=range.concat(i);
        }

        $.each(range, function (index, item) {
            if(item==pages.current){
                var temp=$("<li></li>").addClass("active").append($("<a></a>").attr("href","#").append(item));
                dom.append(temp);
            }else{
                var temp=$("<li></li>").append($("<a></a>").attr("href","#").append(item));

                temp.click(function () {
                    to_adminlist_page(id,item);
                });
                dom.append(temp);
            }
        });

        if(pages.is_next == 1){
            var itemLast=$("<li></li>").append(($("<a></a>")).attr("href","#").append(($("<span></span>")).append("尾页")));

            itemLast.click(function () {
                to_adminlist_page(id,pages.total_pages);
            });

            dom.append(itemLast);
        }
    }
}



$("#btn_adminlist").click(function () {
    common_ops.alert("此操作为覆盖操作，且不可逆，确定操作吗?",function(){
        $("#adminlistFile").click();
    });
});


//上传场所管理员名单
$(".upload_adminlist_wrap").change(function () {
    var formData = new FormData();
    var id=$('#name_adminlist_id').val()
    formData.append('file', $('#adminlistFile')[0].files[0]);
    formData.append('venue_id',id );
    $('#adminlistFile').val('');//及时清空避免二次选择同一文件不能触发change事件

    $.ajax({
        url: common_ops.buildUrl("/venue/uploadAdminlist"),
        type: "POST",
        cache: false,
        processData: false,
        contentType: false,
        data: formData,
        success: function (res) {
            if (res.code == 200) {
                common_ops.successTip("操作成功");
                to_adminlist_page(id,1)
            }else{
                common_ops.alert(res.msg);
            }
        },fail:function(err){
            common_ops.alert(err);
        }
    })
});


//搜索场所管理员
$(".wrap_adminlist_search .search").click(function () {
    var id = $("#name_adminlist_id").val();
    to_adminlist_page(id,1);
});


//新增单个场所管理员学工号
$("#addAdminNo").click(function () {

    var venue_id = $("#name_adminlist_id").val();

    layer.prompt({title: "请输入学工号"},function(no, index){

        var data = {
            venue_id: venue_id,
            no: no,
        };

        $.ajax({
            url: common_ops.buildUrl("/venue/addAdminNo"),
            type: "POST",
            data: data,
            dataType: "json",
            success: function (res) {
                if (res.code == 200) {
                    common_ops.successTip("添加成功");
                    // 刷新当前页
                    var currentPage = $("#pagination_adminlist .active").text();
                    to_adminlist_page(venue_id,currentPage)
                }else{
                    common_ops.alert(res.msg);
                }
                layer.close(index);
            },fail:function(err){
                common_ops.alert(err);
                layer.close(index);
            }
        })
    });
});

//删除单个场所管理员学工号
$("#adminlist_table").on("click",".deleteAdminNo",function(){
    var venue_id = $("#name_adminlist_id").val();
    var no=$(this).attr("no");

    common_ops.alert("确认删除吗?",function(){
        var data = {
            venue_id: venue_id,
            no: no,
        };

        $.ajax({
            url: common_ops.buildUrl("/venue/deleteAdminNo"),
            type: "POST",
            data: data,
            dataType: "json",
            success: function (res) {
                if (res.code == 200) {
                    common_ops.successTip("删除成功");
                    // 刷新当前页
                    var currentPage = $("#pagination_adminlist .active").text();
                    to_adminlist_page(venue_id,currentPage)
                }else{
                    common_ops.alert(res.msg);
                }
            },fail:function(err){
                common_ops.alert(err);
            }
        })
    });
});
////////////////////////////////////场所管理员////////////////////////////////////







//保存场所码
function wxCodeSave(){
    html2canvas($("#testPrint"), {
        onrendered: function(canvas) {
            canvas.id = "mycanvas"; 
            var mainwh=$("#testPrint").width(); 
            var mainhg=$("#testPrint").height();
            var img = convertCanvasToImage(canvas);
            // console.log(img);
            img.onload = function() {
                img.onload = null;
                canvas = convertImageToCanvas(img, 0, 0, 600, 600); //设置图片大小和位置
                img.src = convertCanvasToImage(canvas).src;
                $(img).css({
                background:"#fff" 
                });
                //调用下载方法 
                if(browserIsIe()){ //假如是ie浏览器    
                    DownLoadReportIMG(img.src);
                }else{
                    download(img.src)
                }
            }
        }    
    });

    //绘制显示图片 
    function convertCanvasToImage(canvas) {
        var image = new Image();
        image.src = canvas.toDataURL("image/png"); //获得图片地址
        return image;
    }
    //生成canvas元素，相当于做了一个装相片的框架
    function convertImageToCanvas(image, startX, startY, width, height) {
        var canvas = document.createElement("canvas");
        canvas.width = width;
        canvas.height = height;
        canvas.getContext("2d").drawImage(image, startX, startY, width, height, 0, 0, 600, 600); //调整图片中内容的显示（大小,放大缩小,位置等）
        return canvas;
    }
    function DownLoadReportIMG(imgPathURL) {
        //如果隐藏IFRAME不存在，则添加
        if (!document.getElementById("IframeReportImg"))
            $('<iframe style="display:none;" id="IframeReportImg" name="IframeReportImg" "DoSaveAsIMG();" width="0" height="0" src="about:blank"></iframe>').appendTo("body");
        if (document.all.IframeReportImg.src != imgPathURL) {
            //加载图片
            document.all.IframeReportImg.src = imgPathURL;
        }
        else {
            //图片直接另存为
            DoSaveAsIMG();
        }
    }
    function DoSaveAsIMG() {
        if (document.all.IframeReportImg.src != "about:blank")
            window.frames["IframeReportImg"].document.execCommand("SaveAs");
    }
    // 另存为图片
    function download(src) {
        var imgName=$("#venueName").html()+".png";
        var $a = $("<a></a>").attr("href", src).attr("download", imgName);
        $a[0].click();
    }

    //判断是否为ie浏览器
    function browserIsIe() {
        if (!!window.ActiveXObject || "ActiveXObject" in window)
            return true;
        else
            return false;
    }
} 

//打印
function wxCodePrint() {
  /* Act on the event */
   $("#testPrint").printThis({ 
    debug: false, 
    importCSS: true, 
    importStyle: false, 
    printContainer: true, 
    loadCSS: "../../bootstrap/bootstrap.min.css", 
    // pageTitle: "二维码", 
    removeInline: false, 
    printDelay: 333, 
    header: null, 
    formValues: false
   }); 
//  alert("等待打印"); 
}




//批量上传管理员模态框
$("#batchOpAdminList").click(function () {

    //搜索框清空
    $('#batch_id_dept').val("");
    $('#batch_id_no').val("");
    $('#batch_id_name').val("");

    //清空table表格 
    $("#batch_adminlist_table tbody").empty();
    $("#batch_adminlist_table_page").empty();
    $("#pagination_batch_adminlist .col-lg-12 span").empty();
    $('.demo2').empty()
    
    $("#name_batch_adminlist_id").val("");
    
    $("#BatchAdminListModal").modal();//点击空白处能关闭模态框
    //获取自己管辖的所有场所
    $.ajax({
        url: common_ops.buildUrl("/index/getAllPOI"),
        type: "GET",
        dataType: "json",
        success: function (res) {
            //console.log(res.code)
            if (res.code == 200) {
                // console.log(res.data)
                var venues = res.data

                $('.demo2').doublebox({
                    nonSelectedListLabel: '选择场所',
                    selectedListLabel: '待上传管理员的场所',
                    preserveSelectionOnMove: 'moved',
                    moveOnSelect: false,
                    nonSelectedList:venues,
                    selectedList:[],
                    optionValue:"id",
                    optionText:"name",
                    doubleMove:true,
                });

                $('#bootstrap-duallistbox-nonselected-list_doublebox2').removeAttr("style");
                $('#bootstrap-duallistbox-selected-list_doublebox2').removeAttr("style");

            }
        },
        error: function (msg) {
            console.log("错误"+msg)
        },
    })
});

//批量上传白名单模态框
$("#batchOpWhiteList").click(function () {

    //搜索框清空
    $('#batch_id_dept').val("");
    $('#batch_id_no').val("");
    $('#batch_id_name').val("");

    //清空table表格 
    $("#batch_whitelist_table tbody").empty();
    $("#batch_whitelist_table_page").empty();
    $("#pagination_batch_whitelist .col-lg-12 span").empty();
    $('.demo').empty()
    
    $("#name_batch_whitelist_id").val("");
    
    $("#BatchWhiteListModal").modal();//点击空白处能关闭模态框
    //获取自己管辖的所有场所
    $.ajax({
        url: common_ops.buildUrl("/index/getAllPOI"),
        type: "GET",
        dataType: "json",
        success: function (res) {
            //console.log(res.code)
            if (res.code == 200) {
                // console.log(res.data)
                var venues = res.data

                $('.demo').doublebox({
                    nonSelectedListLabel: '选择场所',
                    selectedListLabel: '待上传白名单的场所',
                    preserveSelectionOnMove: 'moved',
                    moveOnSelect: false,
                    nonSelectedList:venues,
                    selectedList:[],
                    optionValue:"id",
                    optionText:"name",
                    doubleMove:true,
                });

                $('#bootstrap-duallistbox-nonselected-list_doublebox').removeAttr("style");
                $('#bootstrap-duallistbox-selected-list_doublebox').removeAttr("style");

            }
        },
        error: function (msg) {
            console.log("错误"+msg)
        },
    })
});


//批量上传白名单
$("#btn_uploadWhitelist").click(function () {

    var venue_names = $("#bootstrap-duallistbox-selected-list_doublebox>option").map(function() {
        return $(this).text()
    }).get()
    // console.log(venue_names);
    if(venue_names.length==0){
        common_ops.alert("请选择至少一个场所");
        return;
    }

    common_ops.alert("确定对以下的场所操作吗?<br>"+venue_names,function(){
        layer.prompt({title: "请输入批次名"},function(tagname, index){
            $("#add_batch_tag_name").val(tagname);
            $("#batch_whitelistFile").click();
            layer.close(index);
        });
    });
});

//批量上传管理员
$("#btn_uploadAdminlist").click(function () {

    var venue_names = $("#bootstrap-duallistbox-selected-list_doublebox2>option").map(function() {
        return $(this).text()
    }).get()
    // console.log(venue_names);
    if(venue_names.length==0){
        common_ops.alert("请选择至少一个场所");
        return;
    }

    common_ops.alert("确定对以下的场所操作吗?<br>"+venue_names,function(){
        $("#batch_adminlistFile").click();
        layer.close(index);
        // layer.prompt({title: "请输入批次名"},function(tagname, index){
        //     $("#add_batch_tag_name").val(tagname);
        //     $("#batch_adminlistFile").click();
        //     layer.close(index);
        // });
    });
});


$(".upload_batch_whitelist_wrap").change(function () {

    //获取选中的场所id
    var venue_ids = $("#bootstrap-duallistbox-selected-list_doublebox>option").map(function() {
        return $(this).val()
    }).get()

    if(venue_ids.length==0){
        common_ops.alert("请选择至少一个场所");
        $('#batch_whitelistFile').val('');//及时清空避免二次选择同一文件不能触发change事件
        return;
    }

    $("#name_batch_whitelist_id").val(venue_ids[0]);

    var formData = new FormData();
    formData.append('file', $('#batch_whitelistFile')[0].files[0]);
    formData.append('venue_ids',venue_ids);
    formData.append('tag_name',$('#add_batch_tag_name').val());
    $('#batch_whitelistFile').val('');//及时清空避免二次选择同一文件不能触发change事件

    // console.log(venue_ids+"====="+$('#add_batch_tag_name').val());
    // return;
    $('#loading').modal('show');
    $.ajax({
        url: common_ops.buildUrl("/venue/uploadBatchWhitelist"),
        type: "POST",
        cache: false,
        processData: false,
        contentType: false,
        data: formData,
        success: function (res) {
            if (res.code == 200) {
                common_ops.successTip("操作成功");
                $('#batch_whitelist_tag_id').val(res.data.tagID);
                to_batch_whitelist_page(venue_ids[0],1)
            }else{
                common_ops.alert(res.msg);
            }
            $('#loading').modal('hide');
        },fail:function(err){
            common_ops.alert(err);
            $('#loading').modal('hide');
        }
    })
});

$(".upload_batch_adminlist_wrap").change(function () {

    //获取选中的场所id
    var venue_ids = $("#bootstrap-duallistbox-selected-list_doublebox2>option").map(function() {
        return $(this).val()
    }).get()

    if(venue_ids.length==0){
        common_ops.alert("请选择至少一个场所");
        $('#batch_adminlistFile').val('');//及时清空避免二次选择同一文件不能触发change事件
        return;
    }

    $("#name_batch_adminlist_id").val(venue_ids[0]);

    var formData = new FormData();
    formData.append('file', $('#batch_adminlistFile')[0].files[0]);
    formData.append('venue_ids',venue_ids);
    // formData.append('tag_name',$('#add_batch_tag_name').val());
    $('#batch_adminlistFile').val('');//及时清空避免二次选择同一文件不能触发change事件

    // console.log(venue_ids+"====="+$('#add_batch_tag_name').val());
    // return;
    $('#loading').modal('show');
    $.ajax({
        url: common_ops.buildUrl("/venue/uploadBatchAdminlist"),
        type: "POST",
        cache: false,
        processData: false,
        contentType: false,
        data: formData,
        success: function (res) {
            if (res.code == 200) {
                common_ops.successTip("操作成功");
                $('#batch_adminlist_tag_id').val(res.data.tagID);
                to_batch_whitelist_page(venue_ids[0],1)
            }else{
                common_ops.alert(res.msg);
                common_ops.successTip("操作1");
            }
            $('#loading').modal('hide');
        },fail:function(err){
            common_ops.alert(err);
            common_ops.successTip("操作2");
            $('#loading').modal('hide');
        }
    })
});

function to_batch_whitelist_page(id,pageNum) {

    var tagID=$('#batch_whitelist_tag_id').val();
    var dept=$('#batch_id_dept').val();
    var no=$('#batch_id_no').val();
    var name=$('#batch_id_name').val();

    var data = {
        tagID: tagID,
        id: id,
        dept: dept,
        no: no,
        name: name,
        p:pageNum
    };

    $.ajax({
        url: common_ops.buildUrl("/venue/getWhiteList"),
        data:data,
        type: "POST",
        dataType: "json",
        success: function (data) {
            //解析并显示数据表
            build_table(data);
            //解析并显示分页数据
            build_page_nav(data);
        },fail:function(err){
            console.log(err);
        }
    })

    function build_table(data) {
        $("#batch_whitelist_table tbody").empty();
        var whitelist = data.list;

        if(whitelist.length==0){
            var item=$("<td></td>").attr("colspan","4").append("暂无数据");
            $("<tr></tr>").append(item).appendTo("#batch_whitelist_table tbody");
            return;
        }
        var offset = (data.pages.current-1)*data.pages.page_size
        //遍历元素
        $.each(whitelist, function (index, item) {

            var seq = $("<td></td>").append(index+1+offset);
            var dept = $("<td></td>").append(item.dept);
            var no = $("<td></td>").append(item.no);
            var name = $("<td></td>").append(item.name);
            
            $("<tr></tr>").append(seq).append(dept).append(no).append(name).appendTo("#batch_whitelist_table tbody");
        })
    }

    function build_page_nav(data) {
        var pages=data.pages;
        $("#pagination_batch_whitelist .col-lg-12 span").empty();
        $("#pagination_batch_whitelist .col-lg-12 span").append("共"+pages.total +"条记录 | 每页"+pages.page_size+"条");
        var dom=$("#pagination_batch_whitelist .col-lg-12 ul");
        dom.empty();

        if(pages.is_prev == 1){
            var itemFirst=$("<li></li>").append(($("<a></a>")).attr("href","#").append(($("<span></span>")).append("首页")));

            itemFirst.click(function () {
                to_batch_whitelist_page(id,1);
            });

            dom.append(itemFirst);
        }


        var range=[];
        for(var i=pages.from;i<pages.end+1;i++){
            range=range.concat(i);
        }

        $.each(range, function (index, item) {
            if(item==pages.current){
                var temp=$("<li></li>").addClass("active").append($("<a></a>").attr("href","#").append(item));
                dom.append(temp);
            }else{
                var temp=$("<li></li>").append($("<a></a>").attr("href","#").append(item));

                temp.click(function () {
                    to_batch_whitelist_page(id,item);
                });
                dom.append(temp);
            }
        });

        if(pages.is_next == 1){
            var itemLast=$("<li></li>").append(($("<a></a>")).attr("href","#").append(($("<span></span>")).append("尾页")));

            itemLast.click(function () {
                to_batch_whitelist_page(id,pages.total_pages);
            });

            dom.append(itemLast);
        }
    }
}

$(".wrap_batch_whitelist_search .search").click(function () {
    var id = $("#name_batch_whitelist_id").val();
    // console.log(id);
    to_batch_whitelist_page(id,1);
});

function to_batch_adminlist_page(id,pageNum) {

    var tagID=$('#batch_adminlist_tag_id').val();
    var dept=$('#batch_id_dept').val();
    var no=$('#batch_id_no').val();
    var name=$('#batch_id_name').val();

    var data = {
        tagID: tagID,
        id: id,
        dept: dept,
        no: no,
        name: name,
        p:pageNum
    };

    $.ajax({
        url: common_ops.buildUrl("/venue/getAdminList"),
        data:data,
        type: "POST",
        dataType: "json",
        success: function (data) {
            //解析并显示数据表
            build_table(data);
            //解析并显示分页数据
            build_page_nav(data);
        },fail:function(err){
            console.log(err);
        }
    })

    function build_table(data) {
        $("#batch_adminlist_table tbody").empty();
        var whitelist = data.list;

        if(whitelist.length==0){
            var item=$("<td></td>").attr("colspan","4").append("暂无数据");
            $("<tr></tr>").append(item).appendTo("#batch_adminlist_table tbody");
            return;
        }
        var offset = (data.pages.current-1)*data.pages.page_size
        //遍历元素
        $.each(whitelist, function (index, item) {

            var seq = $("<td></td>").append(index+1+offset);
            var dept = $("<td></td>").append(item.dept);
            var no = $("<td></td>").append(item.no);
            var name = $("<td></td>").append(item.name);

            $("<tr></tr>").append(seq).append(dept).append(no).append(name).appendTo("#batch_adminlist_table tbody");
        })
    }

    function build_page_nav(data) {
        var pages=data.pages;
        $("#pagination_batch_adminlist .col-lg-12 span").empty();
        $("#pagination_batch_adminlist .col-lg-12 span").append("共"+pages.total +"条记录 | 每页"+pages.page_size+"条");
        var dom=$("#pagination_batch_adminlist .col-lg-12 ul");
        dom.empty();

        if(pages.is_prev == 1){
            var itemFirst=$("<li></li>").append(($("<a></a>")).attr("href","#").append(($("<span></span>")).append("首页")));

            itemFirst.click(function () {
                to_batch_adminlist_page(id,1);
            });

            dom.append(itemFirst);
        }


        var range=[];
        for(var i=pages.from;i<pages.end+1;i++){
            range=range.concat(i);
        }

        $.each(range, function (index, item) {
            if(item==pages.current){
                var temp=$("<li></li>").addClass("active").append($("<a></a>").attr("href","#").append(item));
                dom.append(temp);
            }else{
                var temp=$("<li></li>").append($("<a></a>").attr("href","#").append(item));

                temp.click(function () {
                    to_batch_adminlist_page(id,item);
                });
                dom.append(temp);
            }
        });

        if(pages.is_next == 1){
            var itemLast=$("<li></li>").append(($("<a></a>")).attr("href","#").append(($("<span></span>")).append("尾页")));

            itemLast.click(function () {
                to_batch_adminlist_page(id,pages.total_pages);
            });

            dom.append(itemLast);
        }
    }
}

$(".wrap_batch_adminlist_search .search").click(function () {
    var id = $("#name_batch_adminlist_id").val();
    // console.log(id);
    to_batch_adminlist_page(id,1);
});
