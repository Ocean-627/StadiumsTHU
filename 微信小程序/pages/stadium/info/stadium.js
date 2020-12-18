// pages/stadium/stadium.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    // 场馆id
    stadium_id:Number,
    stadium_name:'',
    // 滚动图片test
    gallery_imgs: [
      getApp().globalData.imgUrl+'/res/test/stadium_1.jpg',
      getApp().globalData.imgUrl+'/res/test/stadium_2.jpg',
      getApp().globalData.imgUrl+'/res/test/stadium_3.jpeg'
    ],
    // 评论列表
    comment_list: [{
      headerPath:'/res/imgs/header_test.jpg',
      name:'hhy',
      date:'2020年11月11日 15:00',
      score:4,
      content:'很好的场馆，下次还来',
      imgs:[
        getApp().globalData.imgUrl+'/res/test/stadium_1.jpg',
        getApp().globalData.imgUrl+'/res/test/stadium_2.jpg',
        getApp().globalData.imgUrl+'/res/test/stadium_1.jpg',
        getApp().globalData.imgUrl+'/res/test/stadium_2.jpg',
        getApp().globalData.imgUrl+'/res/test/stadium_1.jpg'
      ]
    },{
      headerPath:'/res/imgs/header_test.jpg',
      name:'hhy',
      date:'2020年11月11日 15:00',
      score:4,
      content:'很好的场馆，下次还来',
      imgs:[
        getApp().globalData.imgUrl+'/res/test/stadium_1.jpg',
        getApp().globalData.imgUrl+'/res/test/stadium_2.jpg',
        getApp().globalData.imgUrl+'/res/test/stadium_1.jpg',
        getApp().globalData.imgUrl+'/res/test/stadium_2.jpg',
        getApp().globalData.imgUrl+'/res/test/stadium_1.jpg'
      ]
    }],
    // 图片资源
    map_select_img:getApp().globalData.imgUrl+'/res/imgs/tab_map_select.png',
    info_img:getApp().globalData.imgUrl+'/res/imgs/stadium_info.png',
    notice_img:getApp().globalData.imgUrl+'/res/imgs/stadium_notice.png',
    comment_img:getApp().globalData.imgUrl+'/res/imgs/stadium_comment.png',
    star_img:getApp().globalData.imgUrl+'/res/imgs/info_star.png',
    isfavor_img:getApp().globalData.imgUrl+'/res/imgs/info_isfavor.png',
    notfavor_img:getApp().globalData.imgUrl+'/res/imgs/info_notfavor.png',
  },

  onLoad:function(options) {
    this.setData({stadium_id:options.id})
    this.reqStadiumDetail()
  },

  // 设置场馆信息
  setStadiumInfo:function(res) {
    var data = res.data[0]
    this.setData({
      stadium_name:data.name,
      intro:data.info,
      open_time:data.openTime+" - "+data.closeTime,
      phone:data.contact,
      pos:data.location,
      collect:data.collect
    })
  },

   // 添加收藏
   addFavor:function(e) {
    this.reqAddFavor()
   },

   // 删除收藏
   removeFavor:function(e) {
    this.reqRemoveFavor()
   },

  /*--------------------------------------------------
    页面跳转函数
  ---------------------------------------------------*/
  jmpBooking:function() {
    wx.navigateTo({
      url: '/pages/book/book/book?id='+this.data.stadium_id,
    })
  },

  jmpMap:function() {
    getApp().globalData.seekStadiumId = this.data.stadium_id
    wx.switchTab({
      url: '/pages/map/map',
    })
  },

  /*--------------------------------------------------
    网络请求函数
  ---------------------------------------------------*/
  // 请求场馆具体信息
  reqStadiumDetail:function() {
    const _this = this
    const app = getApp()
    wx.request({
      method: "GET",
      url: app.globalData.reqUrl + '/api/user/stadiumdetail/',
      data: {
        'id': _this.data.stadium_id
      },
      header: {
        'content-type': 'application/json',
        'loginToken': 1,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          _this.setStadiumInfo(res,false)
        } else {
          app.reqFail('获取信息失败')
        }
      },
      fail() {
        app.reqFail('获取信息失败')
      },
      complete() {
      },
    })
  },

  // 收藏/取消收藏
  reqAddFavor:function() {
    const _this = this
    const app = getApp()
    wx.request({
      method: "POST",
      url: app.globalData.reqUrl + '/api/user/collect/',
      data: {
        'stadium_id':_this.data.stadium_id,
      },
      header: {
        'content-type': 'application/json',
        'loginToken': 1,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          app.reqSuccess("收藏成功")
          _this.setData({collect:res.data.id})
        } else {
          app.reqFail("操作失败")
        }
      },
      fail() {
        app.reqFail("操作失败")
      },
    })
  },

  reqRemoveFavor:function() {
    const _this = this
    const app = getApp()
    wx.request({
      method: "DELETE",
      url: app.globalData.reqUrl + '/api/user/collect/',
      data: {
        'collect_id':this.data.collect,
      },
      header: {
        'content-type': 'application/json',
        'loginToken': 1,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          app.reqSuccess("取消收藏成功")
          _this.setData({collect:null})
        } else {
          app.reqFail("操作失败")
        }
      },
      fail() {
        app.reqFail("操作失败")
      },
    })
  },
})