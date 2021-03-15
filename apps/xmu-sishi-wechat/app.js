// app.js
App({
  onLaunch() {
    wx.cloud.init({
      env:"sishimap-6gv4iiy402fa8f89"
    })
 
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
      }
    })
    // 获取用户信息
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
          wx.getUserInfo({
            success: res => {
              // 可以将 res 发送给后台解码出 unionId
              this.globalData.userInfo = res.userInfo
              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }
      }
    })
  },
  globalData: {
    userInfo: null,
    points:0,
    isvisited:[false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,],
    Timeset:["","","","","","","","","","","","","","","","","","","","","","","","","","","","",""],
    markers: [
      {
        id: 0,
        latitude: 24.436898368148537,
        longitude: 118.09497474239731,
        width: "40",
        height: "38",
        iconPath:"../../image/location.png",
        callout: {
          content: "厦门大学革命史展览馆",
          padding: 8,
          display: 'ALWAYS',
          textAlign: 'center',
          borderRadius: 10,
          width: "40",
          height: "40"
        }
      },
      {
        id: 1,
        latitude: 24.43667276773748,
        longitude: 118.09536645767209,
        width: "40",
        height: "38",
        iconPath:"../../image/location.png",
        callout: {
          content: "厦门大学校史馆",
          padding: 8,
          display: 'ALWAYS',
          textAlign: 'center',
          width: "20",
          height: "20"
        }
      },
      {
        id: 2,
        latitude: 24.43770399555001,
        longitude: 118.09470989451216,
        width: "40",
        height: "38",
        iconPath:"../../image/location.png",
        callout: {
          content: "卢嘉锡半身像",
          padding: 8,
          display: 'ALWAYS',
          textAlign: 'center',
          width: "20",
          height: "20"
        }
      },
      {
        id: 3,
        latitude: 24.438724718850573,
        longitude: 118.09436218650818,
        width: "40",
        height: "38",
        iconPath:"../../image/location.png",
        callout: {
          content: "王亚南全身像",
          padding: 8,
          display: 'ALWAYS',
          textAlign: 'center',
          width: "20",
          height: "20"
        }
      },
      {
        id: 4,
        latitude: 24.438728835072965,
        longitude: 118.09530327116394,
        width: "40",
        height: "38",
        iconPath:"../../image/location.png",
        callout: {
          content: "萨本栋全身像",
          padding: 8,
          display: 'ALWAYS',
          textAlign: 'center',
          width: "20",
          height: "20"
        }
      },
      {
        id: 5,
        latitude: 24.438387883802143,
        longitude: 118.09584804662704,
        width: "40",
        height: "38",
        iconPath:"../../image/location.png",
        callout: {
          content: "林文庆亭",
          padding: 8,
          display: 'ALWAYS',
          textAlign: 'center',
          width: "20",
          height: "20"
        }
      },
      {
        id: 6,
        latitude: 24.439064090027795,
        longitude: 118.09749127710725,
        width: "40",
        height: "38",
        iconPath:"../../image/location.png",
        callout: {
          content: "厦门大学大南校门",
          padding: 8,
          display: 'ALWAYS',
          textAlign: 'center',
          width: "20",
          height: "20"
        }
      },
      {
        id: 7,
        latitude: 24.443207233840322,
        longitude: 118.09686910052487,
        width: "40",
        height: "38",
        iconPath:"../../image/location.png",
        callout: {
          content: "防空洞旧址",
          padding: 8,
          display: 'ALWAYS',
          textAlign: 'center',
          width: "20",
          height: "20"
        }
      },
      {
        id: 8,
        latitude: 24.437073263787862,
        longitude: 118.09888612170407,
        width: "40",
        height: "38",
        iconPath:"../../image/location.png",
        callout: {
          content: "湖心岛",
          padding: 8,
          display: 'ALWAYS',
          textAlign: 'center',
          width: "20",
          height: "20"
        }
      },
      {
        id: 9,
        latitude: 24.436589761421832,
        longitude: 118.10029159922787,
        width: "40",
        height: "38",
        iconPath:"../../image/location.png",
        callout: {
          content: "芙蓉二",
          padding: 8,
          display: 'ALWAYS',
          textAlign: 'center',
          width: "20",
          height: "20"
        }
      },
      {
        id: 10,
        latitude: 24.435627423941227,
        longitude: 118.10079723879241,
        width: "40",
        height: "38",
        iconPath:"../../image/location.png",
        callout: {
          content: "芙蓉四",
          padding: 8,
          display: 'ALWAYS',
          textAlign: 'center',
          width: "20",
          height: "20"
        }
      },
      {
        id: 11,
        latitude: 24.435343,
        longitude: 118.100182,
        width: "40",
        height: "38",
        iconPath:"../../image/location.png",
        callout: {
          content: "三家村广场",
          padding: 8,
          display: 'ALWAYS',
          textAlign: 'center',
          width: "20",
          height: "20"
        }
      },
      {
        id: 12,
        latitude: 24.435236710622043,
        longitude: 118.09934348150634,
        width: "40",
        height: "38",
        iconPath:"../../image/location.png",
        callout: {
          content: "芙蓉一",
          padding: 8,
          display: 'ALWAYS',
          textAlign: 'center',
          width: "20",
          height: "20"
        }
      },
      {
        id: 13,
        latitude: 24.435131,
        longitude: 118.098167,
        width: "40",
        height: "38",
        iconPath:"../../image/location.png",
        callout: {
          content: "人类学博物馆",
          padding: 8,
          display: 'ALWAYS',
          textAlign: 'center',
          width: "20",
          height: "20"
        }
      },
      {
        id: 14,
        latitude: 24.43504156460516,
        longitude: 118.09740017790982,
        width: "40",
        height: "38",
        iconPath:"../../image/location.png",
        callout: {
          content: "鲁迅雕像",
          padding: 8,
          display: 'ALWAYS',
          textAlign: 'center',
          width: "20",
          height: "20"
        }
      },
      {
        id: 15,
        latitude: 24.434801,
        longitude: 118.09774,
        width: "40",
        height: "38",
        iconPath:"../../image/location.png",
        callout: {
          content: "罗扬才烈士墓",
          padding: 8,
          display: 'ALWAYS',
          textAlign: 'center',
          width: "20",
          height: "20"
        }
      },
      {
        id: 16,
        latitude: 24.43416224275248,
        longitude: 118.09594244047545,
        width: "40",
        height: "38",
        iconPath:"../../image/location.png",
        callout: {
          content: "萨本栋携夫人墓",
          padding: 8,
          display: 'ALWAYS',
          textAlign: 'center',
          width: "20",
          height: "20"
        }
      },
      {
        id: 17,
        latitude: 24.43429,
        longitude: 118.09787,
        width: "40",
        height: "38",
        iconPath:"../../image/location.png",
        callout: {
          content: "建南大会堂",
          padding: 8,
          display: 'ALWAYS',
          textAlign: 'center',
          width: "20",
          height: "20"
        }
      },
      {
        id: 18,
        latitude: 24.433185445837157,
        longitude: 118.09945076986693,
        width: "40",
        height: "38",
        iconPath:"../../image/location.png",
        callout: {
          content: "涉台文物古迹",
          padding: 8,
          display: 'ALWAYS',
          textAlign: 'center',
          width: "20",
          height: "20"
        }
      }
    ]

  },
  addListener: function (callback) {
    this.callback = callback;
  }
})
