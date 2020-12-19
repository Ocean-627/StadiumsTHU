// pages/login/login.js
Page({
  data: {
    loginStat: 'active',
    logonStat: 'sleep',
    islogon:false,
    btn_text:'登录',
    hasload:false,

    // 图片url
    bg_src:getApp().globalData.imgUrl + '/res/sports/home-background.jpg',
    title_src:getApp().globalData.imgUrl + '/res/imgs/login_title.png',
  },

  onShow:function() {
  },

  onBgLoad:function(e) {
    console.log(e)
    this.setData({
      hasload:true
    })
    this.animate('#title',[
      {opacity:0.0, top:"100rpx"},
      {opacity:0.5, top:"80rpx"},
      {opacity:1.0, top:"60rpx"},
    ],1000,function(){})
  },

  jmpVerifyApp:function() {
    wx.navigateToMiniProgram({
      "appId": "wx1ebe3b2266f4afe0",
      "path": "pages/index/index",
      "envVersion": "trial",
      "extraData": {
        "origin": "miniapp",
        "type": "id.tsinghua"
      }
    })

    const _this = this
    wx.onAppShow((result) => {
      var token = result.referrerInfo.extraData.token
      _this.reqVerify(token)
    })
  },

  // 跳转到主页面
  jmpHome:function() {
    wx.switchTab({
      url: '/pages/home/index/home',
    })
  },

  // 认证请求
  reqVerify:function(token) {
    const _this = this
    const app = getApp()
    wx.request({
      method:'POST',
      url: app.globalData.reqUrl + '/api/user/login/',
      data:{
        'token':token,
      },
      header:{
        'content-type': 'application/json',
      },
      success(res) {
        console.log(res)
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          app.reqSuccess("登录成功")
          _this.jmpHome()
        } else {
          app.reqFail("操作失败")
        }
      },
      fail() {
        app.reqFail("获取信息失败")
      },
    })
  }
})