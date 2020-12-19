//app.js
App({
  onLaunch: function () {
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    // 设置历史记录缓存
    try {
      var history = wx.getStorageSync('visitHistory')
      if(!history) {
        wx.setStorageSync('visitHistory', JSON.stringify([]))
      }
    } catch (error) {
      console.log(error)
    }

    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
      }
    })
    // 获取用户信息
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
          wx.getUserInfo({
            success: res => {
              // 可以将 res 发送给后台解码出 unionId
              this.globalData.userInfo = res.userInfo

              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }
      }
    })
  },
  
  // 请求成功/失败时的行为
  reqSuccess:function(message) {
    if(message !== "") {
      wx.showToast({
        title: message,
        icon:'none',
        duration:1000
      })
    }
  },

  reqFail:function(message) {
    if(message !== "") {
      wx.showToast({
        title: message,
        icon:'none',
        duration:1000
      })
    }
  },

  // 获取当前时间
  getCurrentTime() {
    var date = new Date()
    //获取年份  
    var Y =date.getFullYear();
    //获取月份  
    var M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1);
    //获取当日日期 
    var D = date.getDate() < 10 ? '0' + date.getDate() : date.getDate();
    //获取当前时间
    var H = date.getHours() < 10? '0' + date.getHours() : date.getHours();
    var MI = date.getMinutes() < 10? '0' + date.getMinutes() : date.getMinutes();
    var result = Y+'-'+M+'-'+D+' '+H+':'+MI
    return result
  },

  globalData: {
    userInfo: null,
    reqUrl:'https://cbx.iterator-traits.com',
    imgUrl:'https://cbx.iterator-traits.com/media/miniprogram',
    seekStadiumId:0,    // 跳转地图页面的参数
    maxRecordNum:300,   // 最大历史记录条数
  }
})