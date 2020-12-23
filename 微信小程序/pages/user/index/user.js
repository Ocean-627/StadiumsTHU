// pages/user/user.js
Page({
  data: {
    nickname:'昵称',
    userId:'2017013594',
    // 图片资源文件
    user_img:getApp().globalData.imgUrl+'/res/imgs/header_test.jpg',
    favor_img:getApp().globalData.imgUrl+'/res/imgs/menu_favor.png',
    my_img:getApp().globalData.imgUrl+'/res/imgs/menu_my.png',
    history_img:getApp().globalData.imgUrl+'/res/imgs/menu_history.png',
    calindar_img:getApp().globalData.imgUrl+'/res/imgs/menu_calindar.png',
    info_img:getApp().globalData.imgUrl+'/res/imgs/hmenu_info.png',
    question_img:getApp().globalData.imgUrl+'/res/imgs/hmenu_question.png',
    settings_img:getApp().globalData.imgUrl+'/res/imgs/hmenu_settings.png',
  },

  onLoad: function (options) {
  },

  onShow:function() {
    this.reqUserInfo()
  },

  setUserData:function(res) {
    this.setData({
      nickname:res.data.nickName,
      userId:res.data.userId,
      user_img:res.data.image,
    })
  },

  onPullDownRefresh:function() {
    this.reqUserInfo();
  },

  // 登出
  logout:function() {

  },

  /*-------------------------------
    网络请求函数
  -------------------------------*/
  reqUserInfo:function() {
    var _this = this
    const app = getApp()
    wx.request({
      method: "GET",
      url: 'https://cbx.iterator-traits.com/api/user/user/',
      data: {},
      header: {
        'content-type': 'application/json',
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        if((res.statusCode === 200) && (res.data.error === undefined || res.data.error === null)) {
          _this.setUserData(res)
        } else {
          app.reqFail('获取信息失败')
        }
      },
      fail() {
        app.reqFail('获取信息失败')
      },
      complete() {
        wx.stopPullDownRefresh({
          success: (res) => {},
        })
      }
    })
  },

  /*-------------------------------
    页面跳转函数
  -------------------------------*/
  jmpinfo:function() {
    wx.navigateTo({
      url: '/pages/user/info/info',
    })
  },

  jmpMyBook:function() {
    wx.navigateTo({
      url: '/pages/user/book/book',
    })
  },

  jmpBookHis:function() {
    wx.navigateTo({
      url: '/pages/user/book_history/book_history',
    })
  },

  jmpCollect:function() {
    wx.navigateTo({
      url: '/pages/user/collection/collection',
    })
  },
  
  jmpVisitHistory:function() {
    wx.navigateTo({
      url: '/pages/user/visit_history/visit_history',
    })
  },

  jmpSetting:function() {
    wx.navigateTo({
      url: '/pages/user/setting/setting',
    })
  },

  jmpTutorial:function() {
    wx.navigateTo({
      url: '/pages/user/tutorial/tutorial',
    })
  }
})