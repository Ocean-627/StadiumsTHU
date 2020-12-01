// pages/stadium/stadium.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    // 场馆id
    stadium_id:Number,
    // 滚动图片test
    gallery_imgs: [
      '/res/test/stadium_1.jpg',
      '/res/test/stadium_2.jpg',
      '/res/test/stadium_3.jpeg'
    ],
    // 评论列表
    comment_list: [{
      headerPath:'/res/imgs/header_test.jpg',
      name:'hhy',
      date:'2020年11月11日 15:00',
      score:4,
      content:'很好的场馆，下次还来',
      imgs:[
        '/res/test/stadium_1.jpg',
        '/res/test/stadium_2.jpg',
        '/res/test/stadium_1.jpg',
        '/res/test/stadium_2.jpg',
        '/res/test/stadium_1.jpg'
      ]
    },{
      headerPath:'/res/imgs/header_test.jpg',
      name:'hhy',
      date:'2020年11月11日 15:00',
      score:4,
      content:'很好的场馆，下次还来',
      imgs:[
        '/res/test/stadium_1.jpg',
        '/res/test/stadium_2.jpg',
        '/res/test/stadium_1.jpg',
        '/res/test/stadium_2.jpg',
        '/res/test/stadium_1.jpg'
      ]
    }]
  },

  onLoad:function(options) {
    this.setData({stadium_id:options.id})
  },

  // 请求场馆具体信息
  reqStadiumDetail:function() {
    const _this = this
    const app = getApp()
    wx.request({
      method: "GET",
      url: app.globalData.reqUrl + '/api/user/stadium/',
      data: {},
      header: {
        'content-type': 'application/json',
        'loginToken': 1,
      },
      success(res) {
        _this.reqSuccess()
        _this.setStadiumInfo(res,false)
      },
      fail() {
        _this.reqFail()
      },
      complete() {
        wx.stopPullDownRefresh({
          success: (res) => {},
        })
      },
    })
  },

  // 跳转页面
  jmpBooking:function() {
    wx.navigateTo({
      url: '/pages/stadium/book/book?id='+this.data.stadium_id,
    })
  },

})