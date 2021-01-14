// pages/applyAndReview/myApply/myApply.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    myApply:{
      type:Object,
      value: '0'
    },
    list:{
      type:Object,
      value:0
    },
    selColor:{
      type:Object,
      value:0
    },
    selList:{
      type:Object,
      value:0
    },
    iconStatu:{
      type:Boolean,
      value:0
    },

  },

  /**
   * 组件的初始数据
   */
  data: {
    selColor: '#999',
    selList: [],
    iconStatu: 0,
    tabs: ["已提交申请"],
    activeIndex: 0,
    sliderOffset: 0,
    sliderLeft: 0,
    delBtnWidth: 140,
    selAllFlag: false,
  },

  /**
   * 组件的方法列表
   */
  methods: {
  tabClick: function (e) {
      this.setData({
          sliderOffset: e.currentTarget.offsetLeft,
          activeIndex: e.currentTarget.id
      });
    },
  // 选中
  toggleSel(e) {
    var todo =  0;
    for(var i=0;i<this.data.myApply.length;i++){
      if(this.data.myApply[i].state==0){
        todo += 1;
      }
    }
    if (this.data.iconStatu) {
      let selArr = this.data.selList;
      let selId = e.target.dataset.id || e.currentTarget.dataset.id;
      let dataList = this.properties.myApply;
      let index = this.data.selList.indexOf(selId);
      if (index < 0) {
        selArr.push(selId);
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
        myApply: dataList
      })
      // console.log("selArr:"+selArr+" selId:"+selId+" dataList[0]:"+dataList[0].reviewer+" index:"+index);
      if(this.data.selList.length==todo&& todo!=0){
        this.setData({
          selAllFlag: true
        })
      }
      else{
        this.setData({
          selAllFlag: false
        })
      }
    }
  },
  showSelIcon() {
    var todo =  0;
    for(var i=0;i<this.data.myApply.length;i++){
      if(this.data.myApply[i].state==0){
        todo += 1;
      }
    }
    if(todo == 0 && this.data.iconStatu == false){
      wx.showModal({
        content: "无未审核申请\r\n no pending application",
        showCancel: false,
        confirmColor: '#16ABFE',
      })
      return;
    }
    // console.log("点击编辑")
     this.setData({
       iconStatu: !this.data.iconStatu
     })
     if (this.data.iconStatu == false){
      this.data.selList = [],
      this.properties.myApply.map((value) => {
          value.selStatu = false
      })
     }
     console.log("点击编辑"+this.data.iconStatu)
   },
  drawStart: function (e) {
    // console.log(e);  
    var touch = e.touches[0]
    let dataList = this.properties.myApply;

    // for(var index in this.data.list) {
    //   var item = this.properties.myApply[index]
      dataList.map((value) => {
          value.right = true
      }),
      // item.right = 0
    // }
    this.setData({
      // list: this.data.list,
      myApply: this.data.myApply,
      startX: touch.clientX,
    })

  },
  drawMove: function (e) {
    var touch = e.touches[0]  ;
    var item = this.properties.myApply[e.currentTarget.dataset.index];
    // console.log(item);
    var disX = this.data.startX - touch.clientX;
    
    if (disX >= 20) {
      if (disX > this.data.delBtnWidth) {
        disX = this.data.delBtnWidth
      }
      item.right = disX
      // console.log("disX:"+disX+" right:"+item.right);
      this.setData({
        isScroll: false,
        myApply: this.properties.myApply,
      })
    } else {
      item.right = 0
      this.setData({
        isScroll: true,
        myApply: this.properties.myApply,
      })
    }
  },  
  drawEnd: function (e) {
    // console.log(e.currentTarget.dataset.index);
    var item = this.properties.myApply[e.currentTarget.dataset.index];
    if (item.right >= this.data.delBtnWidth/2) {
      item.right = this.data.delBtnWidth
      this.setData({
        isScroll: true,
        myApply: this.properties.myApply,
      })
    } else {
      item.right = 0
      this.setData({
        isScroll: true,
        myApply: this.properties.myApply,
      })
    }
  },
  selALL(){
    this.setData({
      selAllFlag: !this.data.selAllFlag
    })
    var that = this;
    let selArr = [];
    let dataList = this.properties.myApply;
    if(this.data.selAllFlag){
      for(var i=0;i<that.properties.myApply.length;i++){   //遍历我的所有申请
        if (that.data.myApply[i].state == 0){         //未审核申请
          selArr.push(that.properties.myApply[i].id)
          dataList.map((value) => {
            if (value.id == that.properties.myApply[i].id) {
              value.selStatu = true
             }
          })
        }
      }
      this.setData({
        myApply: this.data.myApply,
      })
    }
    else{
      for(var i=0;i<that.properties.myApply.length;i++){
        if (that.properties.myApply[i].state == 0){
          selArr.pop(that.properties.myApply[i].id)
          dataList.map((value) => {
            if (value.id == that.properties.myApply[i].id) {
              value.selStatu = false
             }
          })
        }
      }
      this.setData({
        myApply: this.data.myApply,
      })
    }
    this.setData({
      selList: selArr,
      MyApprove: dataList
    })
    console.log(this.data.selList)
  },
  // 删除申請
  deleteItem(res){
   console.log("delItem"+res.currentTarget.dataset.id)
   if(res.currentTarget.dataset.state == 1){
      wx.showModal({
        content: "撤销失败，已审核通过\r\ncancel failed\r\nyour application has been approved",
        showCancel: false,
        confirmColor: '#16ABFE',
      })
      return;
   }
   if(res.currentTarget.dataset.state == -1){
    wx.showModal({
      content: "撤销失败，已审核拒绝\r\ncancel failed\r\nyour application has been refused",
      showCancel: false,
      confirmColor: '#16ABFE',
    })
    return;
   }
   var that = this;
   var userid = "";
   var userinfo = wx.getStorageSync('userinfo') || ""
   if (userinfo != '') {
     userid = userinfo.userid //唯一标识符
   }
   wx.showLoading({ title: '加载中' });
   wx.request({
     url: 'https://passport.xmu.edu.cn/wechat/cancel',
     data: {
       ids:res.currentTarget.dataset.id
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
           content: "请稍后再试\r\nPlease try again later",
           showCancel: false,
           confirmColor: '#16ABFE',
         })
         wx.hideLoading();
         return;
         return;
       }
       else{
         wx.showModal({
           content: "撤销申请成功\r\n cancle application successfully",
           showCancel: false,
           confirmColor: '#16ABFE',
         })
         wx.switchTab({
           url: '../../pages/applyAndReview/applyAndReview',
           success:function(e){
             console.log("撤销申请成功，跳转到本页面刷新");
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
   // 多选刪除
  deleteItems(res){
    console.log("多选撤销申请")
    var that = this;
    var userid = "";
    var userinfo = wx.getStorageSync('userinfo') || ""
    if (userinfo != '') {
      userid = userinfo.userid //唯一标识符
    }
    var ids = ''
    for(var i=0;i<that.data.selList.length;i++){
      ids += that.data.selList[i]
      ids += ","
    }
    ids = ids.substring(0,ids.lastIndexOf(','))
    console.log("ids:"+ids)
    if(ids == ''){
      wx.showModal({
        content: "请选择申请\r\n please select application",
        showCancel: false,
        confirmColor: '#16ABFE',
      })
      wx.hideLoading();
      return;
    }
    wx.showLoading({ title: '加载中' });
    wx.request({
      url: 'https://passport.xmu.edu.cn/wechat/cancel',
      data: {            
        ids: ids,
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
            content: "请稍后再试\r\nPlease try again later",
            showCancel: false,
            confirmColor: '#16ABFE',
          })
          wx.hideLoading();
          return;
          return;
        }
        else{
          wx.showModal({
            content: "撤销申请成功\r\n cancle application successfully",
            showCancel: false,
            confirmColor: '#16ABFE',
          })
          // this.setData({
          //   iconStatu: !this.data.iconStatu
          // })
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
  }
})
