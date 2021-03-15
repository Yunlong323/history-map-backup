$(function () {
    
    var myChart1 = echarts.init(document.getElementById('open-count-chart'));
    myChart1.setOption(
    {
        tooltip: {
            trigger: 'axis',
        },
        xAxis: [{
            type: 'category',
            splitLine: {
                show: false
            },
            data: []
        }],
        yAxis: [{
            type: 'value',
            splitLine: {
                show: false
            },
            // name: '人次',
        }],
        series: [{
            type: 'line',
            smooth: true,
            data: []
        }, ]
    });
    myChart1.showLoading();
    var names1=[];    //数组 X坐标值
    var nums1=[];    //数组 Y坐标值



    var myChart2 = echarts.init(document.getElementById('visit-people-count-chart'));
    myChart2.setOption(
    {
        tooltip: {
            trigger: 'axis',
        },
        xAxis: [{
            type: 'category',
            splitLine: {
                show: false
            },
            data: []
        }],
        yAxis: [{
            type: 'value',
            splitLine: {
                show: false
            },
            // name: '人次',
        }],
        series: [{
            type: 'line',
            smooth: true,
            data: []
        }, ]
    });
    myChart2.showLoading();

    var names2=[];    //数组 X坐标值
    var nums2=[];    //数组 Y坐标值


    var myChart3 = echarts.init(document.getElementById('people-stay-time-chart'));
    myChart3.setOption(
    {
        tooltip: {
            trigger: 'axis',
        },
        xAxis: [{
            type: 'category',
            splitLine: {
                show: false
            },
            data: []
        }],
        yAxis: [{
            type: 'value',
            splitLine: {
                show: false
            },
            // name: '人次',
        }],
        series: [{
            type: 'line',
            smooth: true,
            data: []
        }, ]
    });
    myChart3.showLoading();

    var names3=[];    //数组 X坐标值
    var nums3=[];    //数组 Y坐标值



    var myChart4 = echarts.init(document.getElementById('count-stay-time-chart'));
    myChart4.setOption(
    {
        tooltip: {
            trigger: 'axis',
        },
        xAxis: [{
            type: 'category',
            splitLine: {
                show: false
            },
            data: []
        }],
        yAxis: [{
            type: 'value',
            splitLine: {
                show: false
            },
            // name: '人次',
        }],
        series: [{
            type: 'line',
            smooth: true,
            data: []
        }, ]
    });
    myChart4.showLoading();

    var names4=[];    //数组 X坐标值
    var nums4=[];    //数组 Y坐标值


    $.ajax({
        url: common_ops.buildUrl("/business/getStatistics"),
        type: "GET",
        dataType: "json",
        success: function (result) {
            myChart1.hideLoading();    //隐藏加载动画
            if (result.data1) {
                for(var i=0;i<result.data1.length;i++){
                    names1.push(result.data1[i].date);
                }
                for(var i=0;i<result.data1.length;i++){
                    nums1.push(result.data1[i].value);
                }
                myChart1.setOption({        //加载数据图表
                    xAxis: {
                        data: names1
                    },
                    series: [{
                        data: nums1
                    }]
                });
            }

            myChart2.hideLoading();    //隐藏加载动画
            if (result.data2) {
                for(var i=0;i<result.data2.length;i++){
                    names2.push(result.data2[i].date);
                }
                for(var i=0;i<result.data2.length;i++){
                    nums2.push(result.data2[i].value);
                }
                myChart2.setOption({        //加载数据图表
                    xAxis: {
                        data: names2
                    },
                    series: [{
                        data: nums2
                    }]
                });
            }


            myChart3.hideLoading();    //隐藏加载动画
            if (result.data3) {
                for(var i=0;i<result.data3.length;i++){
                    names3.push(result.data3[i].date);
                }
                for(var i=0;i<result.data3.length;i++){
                    nums3.push(result.data3[i].value);
                }
                myChart3.setOption({        //加载数据图表
                    xAxis: {
                        data: names3
                    },
                    series: [{
                        data: nums3
                    }]
                });
            }


            myChart4.hideLoading();    //隐藏加载动画
            if (result.data4) {
                for(var i=0;i<result.data4.length;i++){
                    names4.push(result.data4[i].date);
                }
                for(var i=0;i<result.data4.length;i++){
                    nums4.push(result.data4[i].value);
                }
                myChart4.setOption({        //加载数据图表
                    xAxis: {
                        data: names4
                    },
                    series: [{
                        data: nums4
                    }]
                });
            }
        },fail:function(err){
            myChart.hideLoading();
            console.log(errorMsg);
            common_ops.alert("图表请求数据失败");
        }
    })



});
