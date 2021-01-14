// pages/showVenue/showVenue.js
Page({
  /**
   * 页面的初始数据
   */
  data: {
    userInfo: {},
    MyVenue:[],
    // pageNum:0,
    // pageSize:15
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (query) {
    console.log("进入我的场所onload")
    this.getMyVenue();
    const useridQR = decodeURIComponent(query.useridQR)
    const venueidByAdmin = decodeURIComponent(query.venueidByAdmin)
    console.log("userid:"+useridQR+"  venueidByAdmin:" + venueidByAdmin)
    if (useridQR != 'undefined' && venueidByAdmin != 'undefined') {
      this.scanUserCode(useridQR,venueidByAdmin);
    }
  },
  scanUserCode: function (useridQR,venueidByAdmin) {
    console.log("进入scanUserCode:");
    console.log("userid:"+useridQR+"  venueidByAdmin:" + venueidByAdmin)

    wx.showLoading();
    // console.log(venueid);
    if (this.data.isWaiting == true) {
      wx.showModal({
        content: "请等待倒计时结束",
        showCancel: false,
        confirmColor: '#16ABFE',
      })
      wx.hideLoading();
      return;
    }
    this.data.isWaiting = true;

    var that = this;
    var userid = "";

    var userinfo = wx.getStorageSync('userinfo') || ""
    if (userinfo != '') {
      userid = userinfo.userid //唯一标识符
    } else {
      wx.showModal({
        content: "请先绑定账号",
        showCancel: false,
        confirmColor: '#16ABFE',
      })
      this.data.isWaiting = false;
      wx.hideLoading();
      return;
    }

    // console.log("开始请求后台:" + this.formatTime(new Date()));
    wx.request({
      url: 'https://passport.xmu.edu.cn/wechat/addTrackByAdmin',
      header: {
        'content-type': 'application/x-www-form-urlencoded',
        'userid': userid
      },
      enableHttp2: true,
      enableCache: true,
      data: { 
        venueid: venueidByAdmin, 
        userid: useridQR
      },
      success: function (res) {
        console.log("res:",res)

        // console.log("后台返回成功咯:" + that.formatTime(new Date()));

        if (res.data.code == -1) {//没传场所id
          wx.showModal({
            content: "场所不存在",
            showCancel: false,
            confirmColor: '#16ABFE',
          })
          that.data.isWaiting = false;
          wx.hideLoading();
          return;
        } else if (res.data.code == 1001) {//绿码通过
          that.setData({
            showModal: 1,
            _pass: 1,//通过
            venue_name: res.data.msg,
            userdept: res.data.data.userdept,
            username: res.data.data.username,
            countDownNum: "60",
          });
          that.countDown();//开始倒计时
          wx.hideLoading();
          return;
        } else if (res.data.code == 1002) {//黄码通过
          that.setData({
            showModal: 1,
            _pass: 2,//通过2
            venue_name: res.data.msg,
            userdept: res.data.data.userdept,
            username: res.data.data.username,
            countDownNum: "60",
          });
          that.countDown();//开始倒计时
          wx.hideLoading();
          return;
        } else if (res.data.code == 2000) {//红码禁入
          that.setData({
            showModal: 1,
            _pass: 0,//拒绝
            venue_name: res.data.msg,
            userdept: res.data.data.userdept,
            username: res.data.data.username,
            countDownNum: "60",
          });
          that.countDown();//开始倒计时
          wx.hideLoading();
          return;
        } else {
          wx.showModal({
            content: "请稍后再试",//有可能是接口不存在了或服务器内部出错，返回404或500
            showCancel: false,
            confirmColor: '#16ABFE',
          })
          wx.hideLoading();
          that.data.isWaiting = false;
        }
      },
      fail: function (err) {
        console.log(err);
        wx.showModal({
          content: "请稍后再试",//有可能是超时或URL失效，服务器挂了访问不到
          showCancel: false,
          confirmColor: '#16ABFE',
        })
        wx.hideLoading();
        that.data.isWaiting = false;
      }
    });
  },
  countDown: function () {
    let that = this;
    let countDownNum = 60;//倒计时初始值
    that.data.timer = setInterval(function () {
      console.log("working")
      if (countDownNum == 0) {
        clearInterval(that.data.timer);//删除定时器
        that.setData({
          showModal: 0,
          isWaiting: false
        });
      } else {
        countDownNum--;
        var countDownNumStr = countDownNum;
        if (countDownNum < 10) {
          countDownNumStr = '0' + countDownNum;
        }
        that.setData({
          countDownNum: countDownNumStr
        })
      }
    }, 1000)
  },
  hideModal(e) {
    clearInterval(this.data.timer);//删除定时器
    this.setData({
      showModal: 0,
      isWaiting: false
    })
  },
  getMyVenue:function(){
    var that = this;
    var userid = "";
    var userinfo = wx.getStorageSync('userinfo') || ""
    if (userinfo != '') {
      userid = userinfo.userid //唯一标识符
    } else {
      wx.showModal({
        content: "请先绑定账号",
        showCancel: false,
        confirmColor: '#16ABFE',
      })
      return;
    }

    wx.showLoading({ title: '加载中' });
    // this.data.pageNum = this.data.pageNum + 1;
    wx.request({
      url: 'https://passport.xmu.edu.cn/wechat/getMyVenue',
      data: {
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded',
        'userid': userid
      },
      method: 'POST',
      enableHttp2:true,
      enableCache:true,
      success: function (res) {
        console.log(res)
        if (res.data.code != 200) {
          wx.showModal({
            content: "请稍后再试",
            showCancel: false,
            confirmColor: '#16ABFE',
          })
          return;
        }
        //拼接
        if(res.data.venueList){
          that.data.MyVenue = that.data.MyVenue.concat(res.data.venueList);
          console.log(that.data.MyVenue);
          that.setData({
            MyVenue: that.data.MyVenue,
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
  onShareAppMessage: function () {
    return {
      // title: '厦门大学通行码',
      path: "/pages/my/my",
      imageUrl: '/images/share.png'
    }
  },
  scanVenue: function (t) {
    // console.log(t.currentTarget.dataset.venueid)
    wx.redirectTo({
      url: '../scanVenue/scanVenue?venueid='+t.currentTarget.dataset.venueid
    })
  },
  onPullDownRefresh: function() {
    var that = this;
    that.setData({
      MyVenue: [],
    })
    this.getMyVenue();
  },
  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
    var that = this;
    that.setData({
      MyVenue: [],
    })
    this.getMyVenue();
  },
})