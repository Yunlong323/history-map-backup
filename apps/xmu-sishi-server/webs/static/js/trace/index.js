
function visualize() {
    window.onload = init();
    var data = {
        no: $('#id_no').val(),
        begintime: $('#id_begintime').val(),
        endtime: $('#id_endtime').val(),
        minute: $('#id_minute').val(),
    };

    $.ajax({
        url: common_ops.buildUrl("/trace/getTrace"),
        data:data,
        type: "POST",
        dataType: "json",
        success: function (data) {
            window.onload = init(data.data);
            // console.log(data)
            //解析并显示数据表
            // build_table(data);
        },fail:function(err){
            console.log(err);
        }
    })

    // function init(data) {

    //     var neo4jd3 = new Neo4jd3('#neo4jd3', {
    //         images: {
    //             '场所': "https://passport.xmu.edu.cn/static/images/common/venue.svg",
    //             '目标人员': "https://passport.xmu.edu.cn/static/images/common/riskuser.svg",
    //             '人员': "https://passport.xmu.edu.cn/static/images/common/user.svg",
    //         },
    //         minCollision: 60,
    //         neo4jData:data,

    //         nodeRadius: 25,
    //         // onNodeDoubleClick: function(node) {
    //         //     switch(node.id) {
    //         //         case '25':
    //         //             // Google
    //         //             window.open(node.properties.url, '_blank');
    //         //             break;
    //         //         default:
    //         //             var maxNodes = 5,
    //         //                 data = neo4jd3.randomD3Data(node, maxNodes);
    //         //             neo4jd3.updateWithD3Data(data);
    //         //             break;
    //         //     }
    //         // },
    //         // onRelationshipDoubleClick: function(relationship) {
    //         //     console.log('double click on relationship: ' + JSON.stringify(relationship));
    //         // },
    //         // zoomFit: true
    //         });
    // }





    function build_table(data) {
        //清空table表格
        $("#track_table tbody").empty();
        var track = data.list;
        // console.log(users.length);
        if(track.length==0){
            var item=$("<td></td>").attr("colspan","6").append("暂无数据");
            $("<tr></tr>").append(item).appendTo("#track_table tbody");
            return;
        }
        var offset = (data.pages.current-1)*data.pages.page_size
        //遍历元素
        $.each(track, function (index, item) {

            var seq = $("<td></td>").append(index+1+offset);
            var venue = $("<td></td>").append(item.venue);
            var no = $("<td></td>").append(item.no);
            var name = $("<td></td>").append(item.name);

            if(item.type==1)
                var type = $("<td></td>").append("<div style='width:20px;height:20px;background-color:#36B44C'></div>");
            if(item.type==2)
                var type = $("<td></td>").append("<div style='width:20px;height:20px;background-color:#FABC18'></div>");

            var time = $("<td></td>").append(item.time);

            $("<tr></tr>").append(seq).append(venue).append(no).append(name).append(type).append(time).appendTo("#track_table tbody");

        })
    }
}


//搜索
$(".wrap_search .search").click(function () {
    visualize();
});
