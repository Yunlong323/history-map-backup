// pages/desc/desc.js
const plugin = requirePlugin('WechatSI');
const db=wx.cloud.database()
var app=getApp()
const htmlget=
`<div class="div_class">
  <h1>Title</h1>
  <p class="p">
    这是一段<b>富文本嵌入</b>的测试文本。
  </p>
</div>
`

Page({
  data: {
    text: "",
    htmlget,
    identity:-1,
    title:"",
    src:"",
    isplay:false,
    status_text:"播放文字"
  },
  makecards() {
     wx.navigateTo({
       url: '/pages/sign/sign?identity='+this.data.identity,
     })
  },
  wordYun:function (e) {
    if(this.data.isplay)
    {
      this.end();
      this.setData({isplay:false,status_text:"播放文字"});
      return ;
    }
    var that = this;
    var content;
    if(this.data.text.length>333) content=this.data.text.substring(0,333)
    else content=this.data.text
    plugin.textToSpeech({
      lang: "zh_CN",
      tts: true,
      content: content,
      success: function (res) {
        console.log(res);
        that.setData({
          src: res.filename
        })
        that.yuyinPlay();
      },
      fail: function (res) {
        console.log("fail tts", res)
      }
    })
  },
  
  yuyinPlay: function (e) {
    this.innerAudioContext.src = this.data.src //设置音频地址
    this.innerAudioContext.play(); //播放音频
    this.setData({isplay:true,status_text:"取消播放"})
  },
  end: function (e) {
    this.innerAudioContext.pause();//暂停音频
  },

  onLoad: function (options) {
    var infor=app.globalData.markers[options.identity];
    this.setData({identity:options.identity,title:app.globalData.markers[options.identity].callout.content});
    db.collection("newtext").where({num:JSON.stringify(infor.id+1)}).get({
      success: res => {
        console.log("success", res), 
        this.setData({
          text: res.data[0].introduction
        })
      },
      fail: res => {
        console.log("fail", res)
      }
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    this.innerAudioContext = wx.createInnerAudioContext();
    this.innerAudioContext.onError(function (res) {
      console.log(res);
      wx.showToast({
        title: '语音播放失败',
        icon: 'none',
      })
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
       this.end()
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
  /* 调整视频大小适应手机的函数
  videometa:function (e) {
    var that = this;
    //获取系统信息
    wx.getSystemInfo({
      success (res) {
        //视频的高
        var height = e.detail.height;
        
        //视频的宽
        var width = e.detail.width;
 
        //算出视频的比例
        var proportion = height / width;
 
        //res.windowWidth为手机屏幕的宽。
        var windowWidth = res.windowWidth;
 
        //算出当前宽度下高度的数值
        height = proportion * windowWidth;
        that.setData({
          height,
          width:windowWidth
        });
      }
    })
  },
  */
  videoErrorCallback(e) {
    console.log('视频错误信息:')
    console.log(e.detail.errMsg)
  },
})