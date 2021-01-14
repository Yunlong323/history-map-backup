  var app=getApp();
  Component({
      /**
     * 组件的属性列表
     */
    properties: {
      reviewerList:{
        type:Object,
        value:0
      },
      reviewerNameList:{
        type:Object,
        value:0
      },
      reviewerNoList:{
        type:Object,
        value:0
      },
      venueList:{
        type:Object,
        value:0
      },
      venueNameList:{
        type:Object,
        value:0
      },
      venueIdList:{
        type:Object,
        value:0
      },
      myApply:{
        type:Object,
        value: '0'
      }

    },
      
    data: {
        multiArray: [
          ['2021', '2022','2023','2024'],
          ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
          ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',
            '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24',
            '25', '26', '27', '28', '29', '30', '31'
          ],
          ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',
            '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'
          ],
          ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',
            '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25',
            '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38',
            '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51',
            '52', '53', '54', '55', '56', '57', '58', '59'
          ]
        ],
        // multiIndex1: [-1, 5, 15, 11, 29],
        // multiIndex2: [-1, 5, 15, 11, 30],
        // parseInt(multiArray[0][0])
        multiIndex1: [(app.globalData.dateYear == 2021 ? 0 : (app.globalData.dateYear == 2021) ? 1 : 2), (app.globalData.dateMonth - 1), (app.globalData.dateDay - 1), app.globalData.dateHour, app.globalData.dateMinute],
        multiIndex2: [(app.globalData.dateYear == 2021 ? 0 : (app.globalData.dateYear == 2021) ? 1 : 2), (app.globalData.dateMonth - 1), (app.globalData.dateDay - 1), app.globalData.dateHour, app.globalData.dateMinute],       
        // venueNameList : ['食堂','教室'], 
        venueIdList :['ab1','cd2'],
        venueIndex : null,
        // reviewerList : ['陈老师','李书记'],
        reviewerIndex : null,
        showTopTips: false,
  
        venueid:'',
        reviewer:'',
        // starttime:"2020-06-05 19:31:54",
        // endtime:"2020-06-10 14:31:54",  
        starttime:"",
        endtime:"",  
        reason:null,
        default: '请选择',
    },
    methods: {  
        formatNumber: function(n) {
          n = n.toString()
          return n[1] ? n : '0' + n
        },
        formatTime:function(date) {
          var year = date.getFullYear()
          var month = date.getMonth() + 1
          var day = date.getDate()
          var hour = date.getHours()
          var minute = date.getMinutes()
          var second = date.getSeconds()
          return [year, month, day].map(this.formatNumber).join('/') + ' ' + [hour, minute, second].map(this.formatNumber).join(':')
        },    
        bindStartTimeChange: function (e) {
          var that = this;
          console.log('picker发送选择改变，携带值为', e.detail.value)
          this.setData({
            multiIndex1: e.detail.value
          })   
        },
        bindEndTimeChange: function (e) {
          var that = this;
          console.log('picker发送选择改变，携带值为', e.detail.value)
          this.setData({
            multiIndex2: e.detail.value
          }) 
        },
        bindReasonChange: function(e){
          console.log('picker发送选择改变，携带值为', e.detail.value)
          this.setData({
            reason: e.detail.value
          })
        },
        bindVenueChange(e) {
          console.log('picker发送选择改变，携带值为', e.detail.value)
          this.setData({
              venueIndex: e.detail.value
          })
        },
        bindReviewerChange(e) {
          console.log('picker发送选择改变，携带值为', e.detail.value)
          this.setData({
            reviewerIndex: e.detail.value
          })
        },
        formInputChange(e) {
            const {field} = e.currentTarget.dataset
            this.setData({
                [`formData.${field}`]: e.detail.value
            })
        },
        submitForm() {
          var that = this;
          if (that.data.venueIndex==null) {
            wx.showModal({
              content: "请填写场所 \r\n Please select the venue ",
              showCancel: false,
              confirmColor: '#16ABFE',
            })
            return 
          }
          if (that.data.multiIndex1.toString()==that.data.multiIndex2.toString()) {
            wx.showModal({
              content: "请选择申请时间范围 \r\n Please select the startTime and endTime ",
              showCancel: false,
              confirmColor: '#16ABFE',
            })
            return 
          }
          if (that.data.reason==null) {
            wx.showModal({
              content: "请填写申请原因 \r\n Please enter the reason ",
              showCancel: false,
              confirmColor: '#16ABFE',
            })
            return 
          }
          if (that.data.reviewerIndex==null) {
            wx.showModal({
              content: "请选择审核人 \r\n Please select the reviewer ",
              showCancel: false,
              confirmColor: '#16ABFE',
            })
            return 
          }
          console.log('开始提交表单')
          this.addApply()
        },
        addApply(){
          console.log('开始提交申请', )
          var that = this;
          var userid = "";
          var userinfo = wx.getStorageSync('userinfo') || ""
          if (userinfo != '') {
            userid = userinfo.userid //唯一标识符
          } else {
            wx.switchTab({
              url: '../../pages/my/my',
            }),
            wx.showModal({
              content: "请先绑定账号",
              showCancel: false,
              confirmColor: '#16ABFE',
            })
            return
          }    
          that.data.starttime = that.data.multiArray[0][that.data.multiIndex1[0]]+'-'+that.data.multiArray[1][that.data.multiIndex1[1]]+'-'+that.data.multiArray[2][that.data.multiIndex1[2]]+' '+that.data.multiArray[3][that.data.multiIndex1[3]]+':'+that.data.multiArray[4][that.data.multiIndex1[4]]+':'+'00';
          that.data.endtime = that.data.multiArray[0][that.data.multiIndex2[0]]+'-'+that.data.multiArray[1][that.data.multiIndex2[1]]+'-'+that.data.multiArray[2][that.data.multiIndex2[2]]+' '+that.data.multiArray[3][that.data.multiIndex2[3]]+':'+that.data.multiArray[4][that.data.multiIndex2[4]]+':'+'59';  
          console.log("startTime"); 
          console.log(that.data.starttime);
          wx.showLoading({ title: '加载中' });
          wx.request({
            url: 'https://passport.xmu.edu.cn/wechat/addApply',
            data: {            
              venueid : that.data.venueIdList[that.data.venueIndex],
              reviewer : that.data.reviewerNoList[that.data.reviewerIndex],
              starttime: that.data.starttime,
              endtime :  that.data.endtime,
              reason : that.data.reason,
            },
            header: {
              'content-type': 'application/x-www-form-urlencoded',
              'userid': userid,
            },
            method: 'POST',
            enableHttp2:true,
            enableCache:true,
            success: function (res) {
              console.log(res)
              if (res.data.code != 200) {
                wx.showModal({
                  content: res.data.msg,
                  showCancel: false,
                  confirmColor: '#16ABFE',
                })
                wx.hideLoading();
                return;
                return;
              }
              else{
                wx.showModal({
                  content: res.data.msg,
                  showCancel: false,
                  confirmColor: '#16ABFE',
                })
                wx.switchTab({
                  url: '../../pages/applyAndReview/applyAndReview',
                  success:function(e){
                    const pages = getCurrentPages();
                    const perpage = pages[pages.length - 1];
                    perpage.onLoad()  
                    // var page = getCurrentPages().pop();
                    // if (page == undefined || page ==null) return;
                    // page.onload();
                  }
                })
              }
              // console.log(that.data.items.length);
              wx.hideLoading()
            },
            fail: function (err) {
              wx.hideLoading()
              console.log(err);
            }
          })
        },
        getCurrentDate() {
          let currentDate = new Date();
          //年
          dateYear = currentDate.getFullYear();
          dateMonth = currentDate.getMonth() + 1;
          dateDay = currentDate.getDate();
          dateHour = currentDate.getHours();
          dateMinute = currentDate.getMinutes();
          console.log("当前时间是：" + dateYear + '/' + dateMonth + '/' + dateDay + ' ' + dateHour + ':' + dateMinute);
          //因为是全局变量，不用返回
        },
        setCurrentTime(){
          //获取当前时间
          this.getCurrentDate();
          //设置默认下单时间
          this.setData({
            multiIndex1: [(dateYear == 2020 ? 0 : (dateYear == 2020) ? 1 : 2), (dateMonth - 1), (dateDay - 1), dateHour, dateMinute],
            multiIndex2: [(dateYear == 2020 ? 0 : (dateYear == 2020) ? 1 : 2), (dateMonth - 1), (dateDay - 1), dateHour, dateMinute],
          })
        }
    }
  });