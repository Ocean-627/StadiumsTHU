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

    console.log(1)

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

    console.log(2)
    // 查看token
    try {
      var token = wx.getStorageSync('loginToken')
      if(!token) {
        wx.setStorageSync('loginToken', JSON.stringify(''))
      } else {
        const loginToken = JSON.parse(token)
        if(loginToken !== '') {
          this.globalData.loginToken = JSON.parse(token)
          wx.switchTab({
            url: '/pages/home/index/home',
          })
        }
      }
    } catch (error) {
      console.log(error)
    }
    console.log(3)
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
    var date = new Date(this.getCurrentStamp())
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

  getCurrentStamp() {
    // 东8区时间
    const targetTimezone = -8
    const dif = new Date().getTimezoneOffset()
    const curStamp = new Date().getTime() + dif * 60 * 1000 - (targetTimezone * 60 * 60 * 1000)
    return curStamp
  },

  globalData: {
    userInfo: null,
    reqUrl:'https://cbx.iterator-traits.com',
    imgUrl:'https://cbx.iterator-traits.com/media/miniprogram',
    seekStadiumId:0,    // 跳转地图页面的参数
    maxRecordNum:300,   // 最大历史记录条数
    loginToken:'',      // 登录token
  }
})