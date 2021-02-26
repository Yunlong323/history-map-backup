// pages/scanVenue/scanVenue.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    _isLogin: 0,
    _pass: 0,
    venue_id:"",
    venueid:'',
    timer: 'colorBlockingTimer',//定时器名字
    currentTime: '',
    isWaiting: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (query) {
    // console.log("onload_scanVenue进来了:");
    // console.log(query.venueid);
    this.onBtn(query.venueid);
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  onTabItemTap() {

  },

  scanCode: function (userid,venueid) {    
    console.log("进入scancode:");
    wx.showLoading();
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
    console.log("开始请求后台:");
    wx.request({
      url: 'https://passport.xmu.edu.cn/wechat/addTrackByAdmin',
      header: {
        'content-type': 'application/x-www-form-urlencoded',
        // 'userid': userid
        'venueid' : venueid
      },
      enableHttp2: true,
      enableCache: true,
      data: { userid: userid },
      success: function (res) {

        console.log("后台返回成功咯:");

        if (res.data.code == -1) {//没传用户id
          wx.showModal({
            content: "用户不存在",
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

  onBtn:function(venueidByAd){
    var venueidByAdmin = venueidByAd
    // console.log("venueidByAdmin: "+venueidByAdmin)
    wx.scanCode({
      success: (res) => {
        try {
          var useridQR = res.result
          console.log("扫描用户二维码，识别出用户ID："+"useridQR="+useridQR+" venueidByAdmin"+venueidByAdmin)

          // wx.reLaunch({
          //   url: '../my/my?useridQR='+useridQR+ '&venueidByAdmin=' + venueidByAdmin,
          // })
          wx.reLaunch({
            url: '../showVenue/showVenue?useridQR='+useridQR+ '&venueidByAdmin=' + venueidByAdmin,
          })
        } catch (err) {
          wx.reLaunch({
            url: '../my/my?useridQR=0&venueidByAdmin=0',
          })
        }
      }, fail: (err) => {
        console.log(err);
      }
    })
  },

  // formatTime:function(date) {
  //   var year = date.getFullYear()
  //   var month = date.getMonth() + 1
  //   var day = date.getDate()
  
  //   var hour = date.getHours()
  //   var minute = date.getMinutes()
  //   var second = date.getSeconds()
  
  //   return [year, month, day].map(this.formatNumber).join('/') + ' ' + [hour, minute, second].map(this.formatNumber).join(':')
  // },
  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
    return {
      // title: '厦门大学通行码',
      path: "/pages/my/my",
      imageUrl: '/images/share.png'
    }
  }
})