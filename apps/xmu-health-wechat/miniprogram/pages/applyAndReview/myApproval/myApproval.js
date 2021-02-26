// pages/applyAndReview/myApprove/myApprove.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    MyApprove:{
      type:Object,
      value: '0'
    },
    selColor:{
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
    tabs: ["待处理", "已处理"],
    activeIndex: 0,
    sliderOffset: 0,
    sliderLeft: 0,
    delBtnWidth: 150,
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
    var todo = 0
    for(var i=0;i<this.data.MyApprove.length;i++){
      if(this.data.MyApprove[i].state==0){
        todo += 1;
      }
    }
    if (this.data.iconStatu) {
      let selArr = this.data.selList;
      let selId = e.target.dataset.id || e.currentTarget.dataset.id;
      // console.log("currentseliTarget"+e.currentTarget.dataset.id)
      let dataList = this.properties.MyApprove;
      // console.log("selArr:"+selArr+" selId:"+selId+" dataList[0]:"+dataList[0].id)
      let index = selArr.indexOf(selId);
      // console.log("selArr:"+selArr+" selId:"+selId+" dataList[0]:"+dataList[0].id+" index:"+index);
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
        MyApprove: dataList
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
    for(var i=0;i<this.data.MyApprove.length;i++){
      if(this.data.MyApprove[i].state==0){
        todo += 1;
      }
    }
    if(todo == 0 && this.data.iconStatu == false){
      wx.showModal({
        content: "无待处理审批\r\n no pending approval",
        showCancel: false,
        confirmColor: '#16ABFE',
      })
      return;
    }
     this.setData({
       iconStatu: !this.data.iconStatu
     })
     if (this.data.iconStatu == false){
      this.data.selList = [],
      this.properties.MyApprove.map((value) => {
          value.selStatu = false
      })
     }
     console.log("点击编辑"+this.data.iconStatu)
   },
  selALL(){
    this.setData({
      selAllFlag: !this.data.selAllFlag
    })
    var that = this;
    let selArr = [];
    let dataList = this.properties.MyApprove;
    if(this.data.selAllFlag){
      for(var i=0;i<that.data.MyApprove.length;i++){
        if (that.data.MyApprove[i].state == 0){
          selArr.push(that.data.MyApprove[i].id)
          dataList.map((value) => {
            if (value.id == that.data.MyApprove[i].id) {
              value.selStatu = true
             }
          })
        }
      }
    }
    else{
      for(var i=0;i<that.data.MyApprove.length;i++){
        if (that.data.MyApprove[i].state == 0){
          selArr.pop(that.data.MyApprove[i].id)
          dataList.map((value) => {
            if (value.id == that.data.MyApprove[i].id) {
              value.selStatu = false
             }
          })
        }
      }
    }
    this.setData({
      selList: selArr,
      MyApprove: dataList
    })
    console.log(this.data.selList)
  },
   // 多选审批
  checkItems(res){
    console.log("多选审批")
    var that = this;
    var userid = "";
    var userinfo = wx.getStorageSync('userinfo') || ""
    if (userinfo != '') {
      userid = userinfo.userid //唯一标识符
    }
    var estate = 0;
    if(res.currentTarget.dataset.state=="1"){
      estate = 1;
    }
    else{
      estate = -1;
    }
    var ids = ''
    for(var i=0;i<that.data.selList.length;i++){
      ids += that.data.selList[i]
      ids += ","
    }
    ids = ids.substring(0,ids.lastIndexOf(','))
    console.log("ids:"+ids)
    console.log("estate"+estate)
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
      url: 'https://passport.xmu.edu.cn/wechat/approveBatch',
      data: {            
        ids: ids,
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
            content: "操作成功\r\nOperation succeeded",
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
    this.setData({
      iconStatu: !this.data.iconStatu
    })
    if (this.data.iconStatu == false){
     this.data.selList = [],
     this.properties.MyApprove.map((value) => {
         value.selStatu = false
     })
    }
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
            content: "操作成功\r\nOperation succeeded",
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
  }
})
