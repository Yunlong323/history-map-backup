// pages/applyAndReview/check/c.js
Component({
  /**
   * 组件的属性列表
   */

  properties: {
    MyApprove:{
      type:Object,
      value:0
    }
  },

  /**
   * 组件的初始数据
   */
  data: {
    MyApprove: [],
    tabs: ["待处理", "已处理"],
    activeIndex: 0,
    sliderOffset: 0,
    sliderLeft: 0,
  },

  /**
   * 组件的方法列表
   */
  methods: {
    
    getMyApprove(){
      var that = this;
      that.setData({
        MyApprove: [],
      })
      var userid = "";
      var userinfo = wx.getStorageSync('userinfo') || ""
      if (userinfo != '') {
        userid = userinfo.userid //唯一标识符
      } else {
        return;
      }

      wx.showLoading({ title: '加载中' });
      wx.request({
        url: 'https://passport.xmu.edu.cn/wechat/getMyApprove',
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
    tabClick: function (e) {
      this.setData({
          sliderOffset: e.currentTarget.offsetLeft,
          activeIndex: e.currentTarget.id
      });
    },
    check(event){
      console.log('开始审核')
      var that = this;
      var userid = "";
      var userinfo = wx.getStorageSync('userinfo') || ""
      if (userinfo != '') {
        userid = userinfo.userid //唯一标识符
      }
      var estate = 0;
      if(event.currentTarget.dataset.state=="1"){
        estate = 1;
      }
      else{
        estate = -1;
      }
      wx.showLoading({ title: '加载中' });
      wx.request({
        url: 'https://passport.xmu.edu.cn/wechat/approve',
        data: {            
          id: event.currentTarget.dataset.id,
          state:estate,
        },
        header: {
          'content-type': 'application/x-www-form-urlencoded',
          'userid': userid,
        },
        method: 'POST',
        enableHttp2:true,
        enableCache:true,
        success: function (res) {
          console.log(res)
          if (res.data.code != 200) {
            wx.showModal({
              content: res.data.msg,
              showCancel: false,
              confirmColor: '#16ABFE',
            })
            wx.hideLoading();
            return;
            return;
          }
          else{
            wx.showModal({
              content: res.data.msg,
              showCancel: false,
              confirmColor: '#16ABFE',
            })
            wx.switchTab({
              url: '../../pages/applyAndReview/applyAndReview',
              success:function(e){
                console.log("审批审核操作成功，跳转到本页面刷新");
                const pages = getCurrentPages();
                const perpage = pages[pages.length - 1];
                perpage.onLoad() 
              }
            })
          }
          wx.hideLoading()
        },
        fail: function (err) {
          wx.hideLoading()
          console.log(err);
        }
      })
    },
    getMyApprove(){
      console.log("______________________getMyApply____________________")
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
    lower:function(){
      getMyApprove()
    }
  }
})
