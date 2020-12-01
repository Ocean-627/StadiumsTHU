// pages/user/user.js
Page({
  data: {
    nickname:'昵称',
    userId:'2017013594',
    user_img:'/res/imgs/header_test.jpg',
  },

  onLoad: function (options) {
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

  reqUserInfo:function() {
    var _this = this
    wx.request({
      method: "GET",
      url: 'https://cbx.iterator-traits.com/api/user/user/',
      data: {},
      header: {
        'content-type': 'application/json',
        'loginToken': 1,
      },
      success(res) {
        console.log('Get Info success!')
        _this.setUserData(res)
      },
      fail() {
        console.log('Get Info fail!')
      },
      complete() {
        wx.stopPullDownRefresh({
          success: (res) => {},
        })
      }
    })
  },

  // 页面跳转
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
  }
})