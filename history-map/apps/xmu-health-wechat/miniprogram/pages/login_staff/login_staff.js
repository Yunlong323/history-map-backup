const app = getApp()

Page({
  data: {
    name: "",
    phone:""
  },
  // 页面加载
  onLoad: function (options) {

  },

  bindInputName: function (res) {
    this.setData({
      name: res.detail.value
    })
  },
  bindInputPhone: function (res) {
    this.setData({
      phone: res.detail.value
    })
  },

  login: function () {
    // console.log("提交了 "+this.data.name+" "+this.data.phone);
    if (this.data.name == "" || this.data.phone == ""){
      wx.showModal({
        content: "请输入完整信息",
        showCancel: false,
        confirmColor: '#16ABFE',
      })
      return;
    }

    //ajax
    wx.showLoading();
    wx.request({
      url: 'https://passport.xmu.edu.cn/wechat/login',
      data: {
        username: this.data.name,
        userno: this.data.phone
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded',
      },
      method: 'POST',
      enableHttp2: true,
      enableCache: true,
      success: function (res) {
        // console.log(res)
        if (res.data.code != 200) {
          wx.hideLoading()
          wx.showModal({
            content: res.data.msg,
            showCancel: false,
            confirmColor: '#16ABFE',
          })
        }else{
          wx.hideLoading()
          wx.navigateBack()
          app.setChangedData(res.data.data);
        }
      },
      fail: function (err) {
        wx.hideLoading()
        wx.showModal({
          content: "请稍后再试",
          showCancel: false,
          confirmColor: '#16ABFE',
        })
      }
    })


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