const app = getApp();
var page = {
  /**
   * 页面的初始数据
   */
  data: {
    /**
     * 标识：是否切换成地图视角。
     */
    view: false,
    queryResult: [],
    markers: []
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    this.initialize();
  },
initialize()
{ 
  var temp1=[];
  var temp2=[];
  for(var i=0;i<app.globalData.isvisited.length;i++)
  {
    if(app.globalData.isvisited[i])
    { var t = new Object;
     t=app.globalData.markers[i];
     temp1.push(t);
     temp2.push({school:"厦门大学"+t.callout.content,date:JSON.stringify(app.globalData.Timeset[i]),lat:t.latitude,lng:t.longitude})
    }
  }
  this.setData({markers:temp1,queryResult:temp2})
},
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function() {
    this.mapCtx = wx.createMapContext('myMap');
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function() {
    this.initialize();
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function() {
    this.initialize();
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {
    this.initialize();
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function() {

  },
  changeView: function(e) {
    this.setData({
      view: !this.data.view
    });
    if (this.data.view) {
      this.mapCtx.includePoints({
        padding: [40, 40, 40, 40],
        points: this.data.markers,
        success: res => { }
      });
    }
  },
};

Page(page);
