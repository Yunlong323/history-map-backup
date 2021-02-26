// miniprogram/pages/myinfo/myinfo.js
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var userinfo = wx.getStorageSync('userinfo') || ""
    if (userinfo != '') {
      if (userinfo.usertype == 1)
        userinfo.usertype = '学生';
      else if (userinfo.usertype == 2)
        userinfo.usertype = '教职工';
      else
        userinfo.usertype = '校内员工';

      this.setData({
        _isLogin: 1,
        userno: userinfo.userno,
        userorg: userinfo.userorg,
        username: userinfo.username,
        usertype: userinfo.usertype,
      });
    }else{
      console.log("请登录");
    }
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
    if(this.data._isLogin==0){
      wx.reLaunch({
        url: '/pages/my/my'
      })
    }
  }, 

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  logout:function(){
    var userinfo = wx.getStorageSync('userinfo') || ""
    if (userinfo != '') {
      if (userinfo.usertype == 3)//校内员工
        wx.reLaunch({
          url: '../my/my',
        })
      else
        wx.navigateTo({
          url: '../logout/logout',
        })

      wx.setStorageSync('userinfo', '');
      this.setData({
        _isLogin: 0,
        userno: '',
        userorg: '',
        username: '',
        usertype: '',
      });
    }

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