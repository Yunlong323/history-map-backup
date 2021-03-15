$(function () {
    to_page(1);
});


function to_page(pageNum) {

    var data = {
        dept: $('#id_dept').val(),
        no: $('#id_no').val(),
        name: $('#id_name').val(),
        p:pageNum
    };

    $.ajax({
        url: common_ops.buildUrl("/user/getStudentList"),
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
        //清空table表格
        $("#student_table tbody").empty();
        var student = data.list;
        // console.log(users.length);
        if(student.length==0){
            var item=$("<td></td>").attr("colspan","5").append("暂无数据");
            $("<tr></tr>").append(item).appendTo("#student_table tbody");
            return;
        }
        var offset = (data.pages.current-1)*data.pages.page_size
        //遍历元素
        $.each(student, function (index, item) {

            var seq = $("<td></td>").append(index+1+offset);
            var dept = $("<td></td>").append(item.dept);
            var no = $("<td></td>").append(item.no);
            var name = $("<td></td>").append(item.name);

            var a1=$("<a></a>").attr("title","详情").addClass("detail").attr("dept", item.dept).attr("no", item.no).attr("name", item.name).append($("<i></i>")).addClass("fa fa-eye fa-lg");

            var op=$("<td></td>").append(a1);

            $("<tr></tr>").append(seq).append(dept).append(no).append(name).append(op).appendTo("#student_table tbody");

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



//用户详情Modal
$("#student_table").on("click",".detail",function(){
    var dept=$(this).attr("dept");
    var no=$(this).attr("no");
    var name=$(this).attr("name");

    $("#id_modal_dept").html("单位："+dept);
    $("#id_modal_no").html("学工号："+no);
    $("#id_modal_name").html("姓名："+name);

    //清空table表格
    $("#student_track_table tbody").empty();

    $("#DetailModal").modal();
    to_tracklist_page(no,1);
});


function to_tracklist_page(no,pageNum) {

    var data = {
        no: no,
        p:pageNum
    };

    $.ajax({
        url: common_ops.buildUrl("/track/getStudentTrackByNo"),
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
        $("#student_track_table tbody").empty();
        var tracklist = data.list;

        if(tracklist.length==0){
            var item=$("<td></td>").attr("colspan","4").append("暂无数据");
            $("<tr></tr>").append(item).appendTo("#student_track_table tbody");
            return;
        }
        var offset = (data.pages.current-1)*data.pages.page_size
        //遍历元素
        $.each(tracklist, function (index, item) {
            var seq = $("<td></td>").append(index+1+offset);
            var place = $("<td></td>").append(item.place);
            // var type = $("<td></td>").append(item.type);
            if(item.type==1)
                var type = $("<td></td>").append("<div style='width:20px;height:20px;background-color:#36B44C'></div>");
            if(item.type==2)
                var type = $("<td></td>").append("<div style='width:20px;height:20px;background-color:#FABC18'></div>");

            var time = $("<td></td>").append(item.time);
            
            $("<tr></tr>").append(seq).append(place).append(type).append(time).appendTo("#student_track_table tbody");
        })
    }

    function build_page_nav(data) {
        var pages=data.pages;
        $("#pagination_tracklist .col-lg-12 span").empty();
        $("#pagination_tracklist .col-lg-12 span").append("共"+pages.total +"条记录 | 每页"+pages.page_size+"条");
        var dom=$("#pagination_tracklist .col-lg-12 ul");
        dom.empty();

        if(pages.is_prev == 1){
            var itemFirst=$("<li></li>").append(($("<a></a>")).attr("href","#").append(($("<span></span>")).append("首页")));

            itemFirst.click(function () {
                to_tracklist_page(no,1);
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
                    to_tracklist_page(no,item);
                });
                dom.append(temp);
            }
        });

        if(pages.is_next == 1){
            var itemLast=$("<li></li>").append(($("<a></a>")).attr("href","#").append(($("<span></span>")).append("尾页")));

            itemLast.click(function () {
                to_tracklist_page(no,pages.total_pages);
            });

            dom.append(itemLast);
        }
    }
}
