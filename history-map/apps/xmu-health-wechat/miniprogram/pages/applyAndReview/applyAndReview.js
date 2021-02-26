// pages/app/app.js
let dateYear, dateMonth, dateDay, dateHour, dateMinute; //全是变量   年，月，日，小时，分钟。
Page({

  /**
   * 页面的初始数据
   */
  data: {
    tabClickTime:0,
    currentTab: 1,
    items :[],
    venueList :[],
    venueNameList : [],
    venueIdList :[],
    reviewerList: [],
    reviewerNameList:[],
    reviewerNoList : [],
    myApply : [],
    MyApprove :[],
    pageNum:0,
    pageSize:10,
    pageBigSize:10000,    
    selList: []
  },
  getCurrentDate() {
    let currentDate = new Date();
    //年
    dateYear = currentDate.getFullYear();
    dateMonth = currentDate.getMonth() + 1;
    dateDay = currentDate.getDate();
    dateHour = currentDate.getHours();
    dateMinute = currentDate.getMinutes();
    console.log("当前时间是：" + dateYear + '/' + dateMonth + '/' + dateDay + ' ' + dateHour + ':' + dateMinute);
    //因为是全局变量，不用返回
  },
  getVenueAndReviewer(){
    var that = this;
    that.setData({
      venueList :[],
      venueNameList : [],
      venueIdList :[],
      reviewerList: [],
      reviewerNameList:[],
      reviewerNoList : [],
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
    wx.request({
      url: 'https://passport.xmu.edu.cn/wechat/getVenueAndReviewer',
      data: {
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
        that.data.venueList = that.data.venueList.concat(res.data.venueList);
        that.data.reviewerList = that.data.reviewerList.concat(res.data.reviewerList);
        console.log("reviewerList");
        console.log(res.data.reviewerList);
        var cl = that.data.venueList;
        var rl = that.data.reviewerList;
        for (var i = 0, len = cl.length; i < len; i++) {
          that.data.venueNameList = that.data.venueNameList.concat(cl[i].name);
          that.data.venueIdList = that.data.venueIdList.concat(cl[i].id);
        }
        for (var i = 0, len = rl.length; i < len; i++) {
          if (rl[i].name != null){
            that.data.reviewerNameList = that.data.reviewerNameList.concat(rl[i].name);
          }
          else{
            that.data.reviewerNameList = that.data.reviewerNameList.concat(rl[i].no);
          }
          that.data.reviewerNoList = that.data.reviewerNoList.concat(rl[i].no);
        }
        that.setData({
          venueList: that.data.venueList,
          venueNameList: that.data.venueNameList,
          venueIdList: that.data.venueIdList,
          reviewerList: that.data.reviewerList,
          reviewerNameList: that.data.reviewerNameList,
          reviewerNoList: that.data.reviewerNoList,
        })
        console.log("reviewerList:");
        console.log(that.data.reviewerNameList);
        console.log("venueList:");
        console.log(that.data.venueNameList);
        wx.hideLoading()
      },
      fail: function (err) {
        wx.hideLoading()
        console.log(err);
      }
    })
  },
  getMyApply(){
    console.log("______________________getMyApply____________________")
    var that = this;
    // that.setData({
    //   myApply: [],
    // })
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
        pageNum: this.data.pageNum,
        pageSize: this.data.pageSize
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
  getMyApplyFirstPage(){
    console.log("______________________getMyApplyFirstPage____________________")
    var that = this;
    // that.setData({
    //   myApply: [],
    // })
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
    wx.request({
      url: 'https://passport.xmu.edu.cn/wechat/getMyApply',
      data: {
        pageNum: 0,
        pageSize: this.data.pageSize
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
  getMyApprove(){
    console.log("______________________getMyApprove____________________")
    var that = this;
    // that.setData({
    //   MyApprove: [],
    // })
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
    wx.request({
      url: 'https://passport.xmu.edu.cn/wechat/getMyApprove',
      data: {
        // pageNum: this.data.pageNum,
        // pageSize: this.data.pageSize
        pageNum:0,
        pageSize:10000
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
        that.data.MyApprove = that.data.MyApprove.concat(res.data.data);
        that.setData({
          MyApprove: that.data.MyApprove,
        })
        console.log("MyApprove:");
        console.log(that.data.MyApprove);
        wx.hideLoading()
      },
      fail: function (err) {
        wx.hideLoading()
        console.log(err);
      }
    })
  },
  getMyApproveFirstPage(){
    console.log("______________________getMyApproveFirstPage____________________")
    var that = this;
    // that.setData({
    //   MyApprove: [],
    // })
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
    wx.request({
      url: 'https://passport.xmu.edu.cn/wechat/getMyApprove',
      data: {
        pageNum: 0,
        pageSize: this.data.pageSize
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded',
        'userid': userid
      },
      method: 'POST',
      enableHttp2:true,
      enableCache:true,
      success: function (res) {
        // console.log(res)
        if (res.data.code != 200) {
          wx.showModal({
            content: "请稍后再试",
            showCancel: false,
            confirmColor: '#16ABFE',
          })
          return;
        }

        //拼接
        that.data.MyApprove = that.data.MyApprove.concat(res.data.data);
        that.setData({
          MyApprove: that.data.MyApprove,
        })
        console.log("MyApprove:");
        console.log(that.data.MyApprove);
        wx.hideLoading()
      },
      fail: function (err) {
        wx.hideLoading()
        console.log(err);
      }
    })
  },
  checkLogin(){
    var that = this;
    var userid = "";
    var userinfo = wx.getStorageSync('userinfo') || ""
    if (userinfo != '') {
      userid = userinfo.userid //唯一标识符
    } else {
      wx.switchTab({
        url: '../../pages/my/my',
      }),
      wx.showModal({
        content: "请先绑定账号",
        showCancel: false,
        confirmColor: '#16ABFE',
      })
      return
    }  
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;    
    that.data.tabClickTime = that.data.tabClickTime + 1,
    console.log("onload次数：  "+ that.data.tabClickTime);
    console.log(that.data.tabClickTime);
    that.setData({
      tabClickTime: that.data.tabClickTime,
      venueList :[],
      venueNameList : [],
      venueIdList :[],
      reviewerList: [],
      reviewerNameList:[],
      reviewerNoList : [],    
      myApply : [],
      MyApprove :[],
    })
    console.log('applyAndReview');
    this.checkLogin();
    this.getCurrentDate();
    console.log("______________________onLoad____________________")
    this.getMyApply();
    this.getMyApprove();
    this.getVenueAndReviewer();
    this.setData({ currentTab: 1 });


    let dataList = this.data.myApply;
    dataList.map(function (value) {
      value.selStatu = false;
    })


  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },
  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function (e) {   
    // var that = this;
    // that.setData({
    //   venueList :[],
    //   venueNameList : [],
    //   venueIdList :[],
    //   reviewerList: [],
    //   reviewerNameList:[],
    //   reviewerNoList : [],
    // }) 
    // console.log('applyAndReview')
    // this.checkLogin();
    // this.getCurrentDate();
    // this.getMyApply();
    // this.getMyApprove();
    // this.getVenueAndReviewer();
    // this.setData({ currentTab: 1 });
    // var that =this;
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
  * 点击底栏tab事件
  */
  onTabItemTap (item) {
    var that = this;
    that.data.tabClickTime = that.data.tabClickTime + 1,
    that.setData({
      tabClickTime: that.data.tabClickTime,
      venueList :[],
      venueNameList : [],
      venueIdList :[],
      reviewerList: [],
      reviewerNameList:[],
      reviewerNoList : [],    
      myApply : [],
      MyApprove :[],
    })
    console.log("点击tab"+item.pagePath+"次数：  "+ that.data.tabClickTime);
    console.log(that.data.tabClickTime);
    if (that.data.tabClickTime > 2){
      // this.checkLogin();
      // this.getCurrentDate();
      this.getMyApplyFirstPage();
      // this.getMyApproveFirstPage();
      this.getMyApprove();
      this.getVenueAndReviewer();
    }
  },
  /**
  * 顶部下拉事件
  */
  onPullDownRefresh: function() {
    var that = this;
    if(that.currentTab==1){
      that.setData({
        MyApprove: [],
      })
      this.getMyApproveFirstPage();
      // this.getMyApprove();//获取全部
    }
    if(that.data.currentTab==2){
      that.setData({
        myApply: [],
      })
      this.getMyApplyFirstPage();
    }
  },
  /**
  * 页面触底事件
  */
  onReachBottom: function () {
     var that = this;
    if(that.currentTab==1){
      console.log("触底1"+this.selectComponent("#myApprove"));
      // this.selectComponent("#myApprove").getMyApprove();
      this.getMyApprove();
    }
    if(that.data.currentTab==2){
      console.log("触底2"+this.selectComponent("#myApply"));
      // this.selectComponent("#myApply").getMyApply();
      this.getMyApply();
    }
  },
  /**
  * 切换底部tab
  */
  switchTab(e) {
    console.log(e.currentTarget.dataset.current)
    this.setData({ currentTab: e.currentTarget.dataset.current });
    if(e.currentTarget.dataset.current == 1){
      this.setData({
        MyApprove:[],
      })
      this.getMyApprove()
    }
    if(e.currentTarget.dataset.current == 2){
      this.setData({
        myApply:[],
      })
      this.getMyApplyFirstPage()
    }
  },

  // 选中
  toggleSel(e) {
    if (this.data.iconStatu) {
      let selArr = this.data.selList;
      let selId = e.target.dataset.id || e.currentTarget.dataset.id;
      let dataList = this.data.list;
      let index = this.data.selList.indexOf(selId);
      if (index < 0) {
        selArr.push(e.target.dataset.id);
        dataList.map((value) => {
          if (value.id == selId) {
            value.selStatu = true
           }
        })
      } else {
        dataList.map((value) => {
          if (value.id == selId) {
            value.selStatu = false
          }
        })
        selArr.splice(index, 1)
      }
      this.setData({
        selList: selArr,
        list: dataList
      })
    }
  },
   showSelIcon() {
     this.setData({
      iconStatu: !this.data.iconStatu
     })
   },
   // 删除错题
   delItem() {
     let arr = this.data.list;
     let selArr = this.data.selList;
     for (let i = 0; i < selArr.length; i++) {
       arr = arr.filter((value,index) => {
         return value.id != selArr[i]
       })
     }
     for (let i = 0; i < arr.length; i++) {
       arr[i].selStatu = false
     }
     this.setData({
       list: arr,
       selList: [],
     })
   }

})