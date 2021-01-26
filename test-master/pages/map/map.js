Page({
  data: {
    latitude: 24.436751,
    longitude: 118.0970009,
    markers: [{
      id: 0,
      latitude: 24.436898368148537,
      longitude: 118.09497474239731,
      callout: {
        content: "厦门大学革命史展览馆",
        padding: 10,
        display: 'ALWAYS',
        textAlign: 'center',
        borderRadius: 10,
        // borderColor:'#ff0000',
        // borderWidth: 2,
      }

    },
    {
      id: 1,
      latitude:24.43667276773748,
      longitude: 118.09536645767209,
      callout: {
        content: "厦门大学校史馆",
        padding: 10,
        display: 'ALWAYS',
        textAlign: 'center'
      }

    },
    {
      id: 2,
      latitude: 24.43770399555001,
      longitude:118.09470989451216,
      callout: {
        content: "卢嘉锡半身像",
        padding: 10,
        display: 'ALWAYS',
        textAlign: 'center'
      }

    },
    {
      id: 3,
      latitude: 24.438724718850573,
      longitude:118.09436218650818,
      callout: {
        content: "王亚南全身像",
        padding: 10,
        display: 'ALWAYS',
        textAlign: 'center'
      }

    },
    {
      id: 4,
      latitude:24.438728835072965,
      longitude:118.09530327116394,
      callout: {
        content: "萨本栋全身像",
        padding: 10,
        display: 'ALWAYS',
        textAlign: 'center'
      }

    },
    {
      id: 5,
      latitude: 24.438387883802143,
      longitude: 118.09584804662704,
      callout: {
        content: "林文庆亭",
        padding: 10,
        display: 'ALWAYS',
        textAlign: 'center'
      }

    },
    {
      id: 6,
      latitude: 24.439064090027795,
      longitude: 118.09749127710725,
      callout: {
        content: "厦门大学大南校门",
        padding: 10,
        display: 'ALWAYS',
        textAlign: 'center'
      }

    },
    {
      id:7,
      latitude: 24.443207233840322,
      longitude: 118.09686910052487,
      callout: {
        content: "防空洞旧址",
        padding: 10,
        display: 'ALWAYS',
        textAlign: 'center'
      }

    },
    {
      id: 8,
      latitude: 24.437073263787862,
      longitude:118.09888612170407,
      callout: {
        content: "湖心岛",
        padding: 10,
        display: 'ALWAYS',
        textAlign: 'center'
      }

    },
    {
      id: 9,
      latitude:24.436589761421832,
      longitude:118.10029159922787,
      callout: {
        content: "芙蓉二",
        padding: 10,
        display: 'ALWAYS',
        textAlign: 'center'
      }

    },
  ],
    customCalloutMarkerIds: [],
    num: 1
  },
  onReady: function (e) {
    this.mapCtx = wx.createMapContext('myMap')
  },
  markertap(e) {
    console.log('@@@ markertap', e)
    var id = e.detail.markerId
    var url='/pages/desc'+(id+1)+'/desc'+(id+1)
    wx.navigateTo({
      url: url,
      success: function (res) {},
      fail: function (res) {},
      complete: function (res) {},
    })
  },
  callouttap(e) {
    var id = e.detail.markerId
    var url='/pages/desc'+(id+1)+'/desc'+(id+1)
    wx.navigateTo({
      url:url,
      success: function (res) {},
      fail: function (res) {},
      complete: function (res) {},
    })
  },
})