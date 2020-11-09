// pages/user/user.js
Page({
  data: {

  },

  jmpinfo:function() {
    wx.navigateTo({
      url: '/pages/user/info/info',
    })
  },

  jmpMyBook:function() {
    wx.navigateTo({
      url: '/pages/user/book/book',
    })
  }
})