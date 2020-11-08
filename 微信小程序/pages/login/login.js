// pages/login/login.js
Page({
  data: {
    loginStat: 'active',
    logonStat: 'sleep',
    islogon:false,
    btn_text:'登录'
  },

  onLaunch: function () {
    wx.hideTabBar()
  },

  jmplogin: function(e) {
    if(!this.data.islogon) {
      return;
    }
    this.setData ({
      loginStat: 'active',
      logonStat: 'sleep',
      islogon:false,
      btn_text:'登录'
    })
  },

  jmplogon: function(e) {
    if(this.data.islogon) {
      return;
    }
    this.setData ({
      loginStat: 'sleep',
      logonStat: 'active',
      islogon:true,
      btn_text:'注册'
    })
  }

})