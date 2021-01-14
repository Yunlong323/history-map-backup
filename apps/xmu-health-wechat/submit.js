let dateYear, dateMonth, dateDay, dateHour, dateMinute; //全是变量   年，月，日，小时，分钟。

var app=getApp();
Page({

  properties: {
    reviewerList:{
      type:Object,
      value:0
    },
    myApply:{
      type:Object,
      value: '0'
    }
  },

  /**
   * 页面的初始数据
   */
  data: {
    myApply:[],
  },

  getMyApply(){
    var that = this;
    that.setData({
      myApply: [],
    })
    var userid = "";
    var userinfo = wx.getStorageSync('userinfo') || ""
    if (userinfo != '') {
      userid = userinfo.userid //唯一标识符
    } else {
      // wx.showModal({
      //   content: "请先绑定账号",
      //   showCancel: false,
      //   confirmColor: '#16ABFE',
      // })
      return;
    }

    wx.showLoading({ title: '加载中' });
    this.data.pageNum = this.data.pageNum + 1;
    wx.request({
      url: 'https://passport.xmu.edu.cn/wechat/getMyApply',
      data: {
        pageNum: this.data.myApplyPageNum,
        pageSize: this.data.myApplyPageSize
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
        that.data.myApply = that.data.myApply.concat(res.data.data);
        that.setData({
          myApply: that.data.myApply,
        })
        console.log("myApply:");
        console.log(that.data.myApply);
        wx.hideLoading()
      },
      fail: function (err) {
        wx.hideLoading()
        console.log(err);
      }
    })
  },

  tabChange(e) {
    console.log('tab change', e)
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

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

  }
})