const app = getApp()
// miniprogram/pages/scan/scan.js
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
    
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  onTabItemTap() {
    this.onBtn();
  },



  onBtn:function(){

    wx.scanCode({
      success: (res) => {
        try {
          // var url = res.path.substr(0, 18)
          var param = res.path.substr(18, 16)
          console.log("res.path:  "+res.path)

          wx.reLaunch({
            url: '../my/my?scene=' + param,
          })
        } catch (err) {
          wx.reLaunch({
            url: '../my/my?scene=0',
          })
        }
      }, fail: (err) => {
        console.log(err);
      }
    })
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
  // onTabItemTap (item) {
  //   console.log(item.index)
  //   console.log(item.pagePath)
  //   console.log(item.text)
  // },
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