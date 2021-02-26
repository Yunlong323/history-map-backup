//index.js
//获取应用实例
const app = getApp()
const QR = require('../../utils/weapp-qrcode.js')

Page({
  data: {
    motto: 'Hello World',
    qrcodeURL: "",
    userid: "",
  },
  onLoad: function () {
    var myQRCode = wx.getStorageSync('myQRCode');
    if (myQRCode != ''){
      console.log("个人二维码已缓存")
      this.setData({
        qrcodeURL: myQRCode
      })
      // wx.showModal({
      //   content: "缓存",
      // })
    }
    else{
      console.log("生成个人二维码")
      var userinfo = wx.getStorageSync('userinfo') || ""
      // console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!"+userinfo.userid)
      if (userinfo != '') {
        // this.data.userid = userinfo.userid //唯一标识符
        this.setData({
          userid: userinfo.userid
        })
      } else {
          console.log("用户名为空，重新登陆")
          this.data.userid = 'testID'             //testtesttest
      }
      this.drawImg();
      // wx.showModal({
      //   content: "新"+this.data.userid,
      // })
    }
  },
  setText: function (e) {
    this.setData({
      userid: e.detail.value
    })
  },
  drawImg: function () {
    console.log("drawImgthis: "+this.data.userid);
    var myQRCode = QR.drawImg(this.data.userid, {
      typeNumber: 4,
      errorCorrectLevel: 'M',
      size: 500
    })
    this.setData({
      qrcodeURL: myQRCode
    })
    wx.setStorageSync('myQRCode', myQRCode)//将userinfo缓存
  }
})
