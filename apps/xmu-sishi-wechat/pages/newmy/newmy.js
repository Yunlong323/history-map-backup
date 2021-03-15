// pages/my/index.js
const app = getApp()
Page({
  data: {
    _isLogin: 0,
    _pass: 0,
    venue_name:"",
    currentTime: '',
    isWaiting: false,
    points:0
  },
  showPoints(){
    var app=getApp();
    this.setData({points:app.globalData.points})
  },
  // 页面加载
  onLoad: function (query) {
    //若之前登录过则直接取出个人信息
    var userinfo = wx.getStorageSync('userinfo') || ""
    if (userinfo != '') {
      this.setData({
        _isLogin: 1,
        userid: userinfo.userid //唯一标识符
      });
    }
    const venueid = decodeURIComponent(query.scene)
    if (venueid != 'undefined') {
      this.scanCode(venueid);
    }
    const useridQR = decodeURIComponent(query.useridQR)
    const venueidByAdmin = decodeURIComponent(query.venueidByAdmin)
    console.log("userid:"+useridQR+"  venueidByAdmin:" + venueidByAdmin)
    if (useridQR != 'undefined' && venueidByAdmin != 'undefined') {
      this.scanUserCode(useridQR,venueidByAdmin);
    }
    // console.log("开始注册回调事件:" + this.formatTime(new Date()));
    //注册统一身份认证的callback回调
    var that = this;
    app.addListener(function (changedData) {
      
      wx.setStorageSync('userinfo', changedData)//将userinfo缓存
      if (changedData.userno != '') {

        wx.showToast({
          title: '登录成功',
        })

        if (changedData.usertype == 1)
          changedData.usertype = '学生';
        else if (changedData.usertype == 2)
          changedData.usertype = '教职工';
        else
          changedData.usertype = '校内员工';

        that.setData({
          _isLogin: 1,
          userno: changedData.userno,
          userorg: changedData.userorg,
          username: changedData.username,
          usertype: changedData.usertype,
          userid: changedData.userid //唯一标识符
        });
      }
    });

    // console.log("回调事件注册好了:" + this.formatTime(new Date()));
  },
  onShow:function(){
  this.showPoints();
  },
  showDetail: function () {
    //未登录-绑定账号
    var userinfo = wx.getStorageSync('userinfo') || ""
    if (userinfo == '') {
      //登录选项框
      this.setData({
        typeT: true
      })
    } else {
      //已登录-个人信息
      wx.navigateTo({
        url: '../userinfo/userinfo'
      })
    }
  },

  xmu_login:function(){
    wx.navigateTo({
      url: '../login/login'
    }),
    this.setData({
      typeT: false
    })
  },

  staff_login:function(){
    wx.navigateTo({
      url: '../login_staff/login_staff'
    }),
    this.setData({
      typeT: false
    })
  },


  //我的轨迹
  showTrack: function () {
    /*//未登录-绑定账号
    var userinfo = wx.getStorageSync('userinfo') || ""
    if (userinfo == '') {
      wx.showModal({
        content: "请先绑定账号",
        showCancel: false,
        confirmColor: '#16ABFE',
      })
    } else {
      //已登录-个人信息
      wx.navigateTo({
        url: '../track/track'
      })
    }*/
    wx.navigateTo({
      url: '../../pages/track/track',
    })
  },
  showQRCode: function () {
    wx.navigateTo({
      url: '../showQRCode/showQRCode',
    })
  },

  //我的场所
  showVenue: function () {
     //未登录-绑定账号
      var userinfo = wx.getStorageSync('userinfo') || ""
      if (userinfo == '') {
        wx.showModal({
          content: "请先绑定账号",
          showCancel: false,
          confirmColor: '#16ABFE',
        })
      } else {
        //已登录-个人信息
        wx.navigateTo({
          url: '../showVenue/showVenue'
        })
      }
    },
  showAbout: function () {
    wx.navigateTo({
      url: '../about/about',
    })
  },



  scanCode: function (venueid) {
    // console.log("进入scancode:" + this.formatTime(new Date()));

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
      url: 'https://passport.xmu.edu.cn/wechat/addTrack',
      header: {
        'content-type': 'application/x-www-form-urlencoded',
        'userid': userid
      },
      enableHttp2: true,
      enableCache: true,
      data: { venueid: venueid },
      success: function (res) {

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


  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
    return {
      // title: '厦门大学通行码',
      path: "/pages/my/my",
      imageUrl: '/images/share.png'
    }
  },
})