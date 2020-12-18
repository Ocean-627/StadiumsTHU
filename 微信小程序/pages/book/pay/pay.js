Page({
  data:{
    // 预约订单id
    bookId:Number,
    // 步骤
    activeStep: 2,
    steps: [
      {
        text: '步骤一',
        desc: '选择场地',
      },
      {
        text: '步骤二',
        desc: '确认预定',
      },
      {
        text: '步骤三',
        desc: '付款',
      },
    ],
    // 当前付款方式
    payment_radio: '1',
    price:'',
    // 付款状态
    paying:false,
    pay_success:false,
    // 图片资源
    wepay_img:getApp().globalData.imgUrl+'/res/pay/wepay.png',
    alipay_img:getApp().globalData.imgUrl+'/res/pay/alipay.png',
    yinlian_img:getApp().globalData.imgUrl+'/res/pay/yinlian.png',
  },

  onLoad:function(options) {
    this.setData({
      bookId:options.id,
      stadiumId:options.stadium,
      directFrom:options.directFrom,
    })
    this.reqBookInfo()
  },

  // 切换付款方式
  onChangePay:function(e) {
    this.setData({
      payment_radio: e.currentTarget.dataset.name,
    });
  },

  // 点击付款按钮
  onPay:function(e) {
    this.setData({
      paying:true
    })
    this.reqPay()
  },

  /*---------------------------
    页面跳转函数
  ---------------------------*/
  jmpMain:function() {
    wx.switchTab({
      url: '/pages/home/index/home',
    })
  },

  jmpMyBook:function() {
    wx.redirectTo({
      url: '/pages/user/book/book',
    })
  },

  jmpStadium:function() {
    const _this = this
    console.log(this.data.directFrom)
    if(this.data.directFrom === 'history') {
      // 从预约记录跳转过来
      wx.redirectTo({
        url: '/pages/stadium/info/stadium?id='+_this.data.stadiumId,
      })
    }
    else if(this.data.directFrom === 'book') {
      // 从预定页面跳转过来，直接返回到之前的页面
      wx.navigateBack({
        delta: 0,
      })
    }
  },

  /*---------------------------
    网络请求函数
  ---------------------------*/
  reqPay:function() {
    const _this = this
    const app = getApp()
    wx.request({
      method: "PUT",
      url: app.globalData.reqUrl + '/api/user/reserve/',
      data:{
        id:_this.data.bookId,
        payment:true,
      },
      header: {
        'content-type': 'application/json',
        'loginToken': 1,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          _this.setData({
            pay_success:true,
          })
        } else {
          app.reqFail("付款失败")
        }
      },
      fail() {
        app.reqFail("付款失败")
      },
      complete() {
        _this.setData({
          paying:false
        })
      }
    })
  },

  reqBookInfo:function() {
    const _this = this
    const app = getApp()
    wx.request({
      method: "GET",
      url: app.globalData.reqUrl + '/api/user/reserve/',
      data:{
        id:_this.data.bookId
      },
      header: {
        'content-type': 'application/json',
        'loginToken': 1,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          _this.setData({
            price:res.data.results[0].price+'.00'
          })
        } else {
          app.reqFail("请求支付信息失败")
        }
      },
      fail() {
        app.reqFail("请求支付信息失败")
      },
      complete() {
        wx.stopPullDownRefresh({
          success: (res) => {},
        })
      },
    })
  }
})