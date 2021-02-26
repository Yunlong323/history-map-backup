Page({

  /**
   * 页面的初始数据
   */
  data: {
    items: [], // 数据列表
    userInfo: {},

    pageNum:0,
    pageSize:15
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function () {
    this.getTrack();
  },

  //页面上拉触底事件的处理函数
  onReachBottom(e) {
    this.getTrack();
  },


  getTrack:function(){
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
    this.data.pageNum = this.data.pageNum + 1;
    wx.request({
      url: 'https://passport.xmu.edu.cn/wechat/getMyTrack',
      data: {
        pageNum: this.data.pageNum,
        pageSize: this.data.pageSize
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
        that.data.items = that.data.items.concat(res.data.data);
        that.setData({
          items: that.data.items,
        })
        // console.log(that.data.items.length);
        wx.hideLoading()
      },
      fail: function (err) {
        wx.hideLoading()
        console.log(err);
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