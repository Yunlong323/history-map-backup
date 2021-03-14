var app=getApp()
Page({
  data: {
    latitude: 24.436751,
    longitude: 118.0970009,
    markers:[],
    customCalloutMarkerIds: [],
    num: 1,
    choose: {}
  },
  onLoad:function(e){
    this.setData({markers:app.globalData.markers})
  },
  onReady: function (e) {
    this.mapCtx = wx.createMapContext('myMap')
  },
  markertap(e) {
    wx.navigateTo({
      url: '/pages/desc/desc?identity=' + e.detail.markerId,
      success: function (res) {},
      fail: function (res) {},
      complete: function (res) {},
    })
  },
  callouttap(e) {
    wx.navigateTo({
      url: '/pages/desc/desc?identity=' + e.detail.markerId,
      success: function (res) {},
      fail: function (res) {},
      complete: function (res) {},
    })
  },
  labeltap(e) {
    wx.navigateTo({
      url: '/pages/desc/desc?identity=' + e.detail.markerId,
      success: function (res) {},
      fail: function (res) {},
      complete: function (res) {},
    })
  },
})