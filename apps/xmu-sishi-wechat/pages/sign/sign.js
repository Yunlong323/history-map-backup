//index.js
const app = getApp();
const util = require('../../utils/util.js');
const QQMapWX = require('../../utils/qqmap-wx-jssdk1/qqmap-wx-jssdk.min.js');
const qqmapsdk = new QQMapWX({
  key: '5KIBZ-7R46W-NDPRF-R6RFN-RWXHO-M4B6F'
});
let choose_details;
var page = {
  /**
   * 页面的初始数据
   */
  data: {
    formatedDate: undefined,
    hasLocation: false,
    location_details: undefined,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.getAddress()
    choose_details = app.globalData.markers[options.identity]
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

  },
  chooseLocation: function (e) {
    wx.chooseLocation({
      success: res => {
        // 将通过 wx.chooseLocation() 方法获取到的地理坐标通过 qqmapsdk.reverseGeocoder() 接口获取详细位置信息
        qqmapsdk.reverseGeocoder({
          location: {
            latitude: res.latitude,
            longitude: res.longitude
          },
          get_poi: 1,
          success: res => { //成功后的回调
            console.log("getAddress: ", res);
            res = res.result;
            this.setData({ //设置markers属性和地图位置poi，将结果在地图展示
              location_details: res,
              hasLocation: true,
              formatedDate: util.formatTime(new Date),
            });
          },
          fail: error => {
            console.error(error);
          },
          complete: res => {
            console.log(res);
          }
        });
      },
    })
  },
  getAddress: function (e) {
    var _this = this;
    qqmapsdk.reverseGeocoder({
      get_poi: 1, //是否返回周边POI列表：1.返回；0不返回(默认),非必须参数
      success: (res) => { //成功后的回调
        console.log("getAddress: ", res);
        res = res.result;
        _this.setData({ //设置markers属性和地图位置poi，将结果在地图展示
          location_details: res,
          hasLocation: true,
          formatedDate: util.formatTime(new Date),
        });
      },
      fail: (error) => {
        console.error(error);
      },
      complete: (res) => {
        console.log(res);
      }
    });
    // 获取gcj02坐标
    wx.getLocation({
      type: 'gcj02',
      altitude: true,
      success: res => {
        console.log("Location-gcj02", res);
        app.globalData.gcj02 = res;
      },
      fail: function (res) {},
      complete: function (res) {},
    });
  },
  //打卡积分
  mark(){
    var app=getApp();
  console.log(choose_details)
  console.log(this.data.location_details)
  if(Math.abs(choose_details.latitude-this.data.location_details.location.lat)<100&&Math.abs(choose_details.longitude-this.data.location_details.location.lng)<100)
  {
    if(!app.globalData.isvisited[choose_details.id])
    {
     var date=util.formatTime(new Date());
     app.globalData.isvisited[choose_details.id]=true
     app.globalData.points=app.globalData.points+1;
     app.globalData.Timeset[choose_details.id]=date;
     wx.showToast({
     title: '打卡成功',
    })
    }
    //icon:"error" 仅在真机有效
    else{
      wx.showToast({
        title: '已在此地打卡',
        icon:"error"
      })
    }
  }
  else{
    wx.showToast({
      title: 'Wrong Location!',
      icon:"error"
    })
 }
  }
}
Page(page);
