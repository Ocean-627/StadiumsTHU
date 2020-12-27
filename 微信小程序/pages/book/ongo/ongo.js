import Toast from '../../../miniprogram/miniprogram_npm/@vant/weapp/toast/toast';
import Dialog from '../../../miniprogram/miniprogram_npm/@vant/weapp/dialog/dialog';
Page({
  data:{
    // 预定编号
    bookId:Number,
    // 剩余时间百分比
    remain_percent:Number,
    // 剩余时间
    remain_time:1*60*60*1000,
    // 总时间
    total_time:1*60*60*1000,
    timeData:{},
    // 是否已经签到
    checked:true,
    // 是否正在签到
    checkingIn:false,
    // 是否正在签退
    leaveIn:false,
    // 是否已经签退
    leave:false,
  },

  onLoad:function(options) {
    Toast.loading({
      message: '加载中...',
      forbidClick: true,
    })
    this.setData({
      bookId:options.id
    })
    this.reqBookInfo()
  },

  // 设置预约信息
  setBookInfo:function(res) {
    const info = res.data.results[0]
    this.setData({
      stadium_img:info.image,
      stadium_name:info.stadium,
      court_name:info.court,
      start_time:info.startTime,
      end_time:info.endTime,
      checked:info.checked,
      leave:info.leave
    })
    const startTimeText = info.date+' '+info.startTime
    const endTimeText = info.date+' '+info.endTime
    // 获取活动时间戳
    const startStamp = new Date(startTimeText.replace(/-/g,"/")).getTime()
    const endStamp = new Date(endTimeText.replace(/-/g,"/")).getTime()
    const curStamp = getApp().getCurrentStamp()
    const percent = parseInt(100*(endStamp-curStamp)/(endStamp-startStamp))
    this.setData({
      total_time:endStamp-startStamp,
      remain_time:endStamp-curStamp,
      remain_percent:percent,
    })
  },

  // 倒计时触发事件
  onCountDown:function(e) {
    this.setData({
      timeData: e.detail,
    })
    const remain = (((e.detail.hours*60+e.detail.minutes)*60)+e.detail.seconds)*1000
    this.setData({
      remain_percent:parseInt(100*remain/this.data.total_time),
    })
  },

  /*----------------------------------
    按钮处理函数
  -----------------------------------*/
  // 签到
  onCheckIn:function() {
    this.setData({checkingIn:true})
    this.reqCheckIn({
      checked:true,
      id:this.data.bookId,
    })
  },

  // 签退
  onCheckOut:function() {
    const _this = this
    this.setData({
      leaveIn:true
    })
    Dialog.confirm({
      title:'操作确认',
      message:'请确认是否要签退',
    })
    .then(()=>{
      // 确认
      _this.reqCheckOut({
        leave:true,
        id:this.data.bookId,
      })
    })
    .catch(()=>{
      _this.setData({
        leaveIn:false
      })
    })
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
      url: '/pages/user/book_history/book_history',
    })
  },


  /*----------------------------------
    网络请求函数
  -----------------------------------*/
  // 获取预约信息
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
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          _this.setBookInfo(res)
        } else {
          app.reqFail("获取信息失败")
        }
      },
      fail() {
        app.reqFail("获取信息失败")
      },
      complete() {
        Toast.clear()
      }
    })
  },

  // 签到签退
  reqCheckIn:function(param) {
    const _this = this
    const app = getApp()
    wx.request({
      method: "PUT",
      url: app.globalData.reqUrl + '/api/user/reserve/',
      data:param,
      header: {
        'content-type': 'application/json',
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          _this.setData({checked:true})
          app.reqSuccess("签到成功")
        } else {
          app.reqFail("签到失败")
        }
      },
      fail() {
        app.reqFail("签到失败")
      },
      complete() {
        _this.setData({
          checkingIn:false
        })
      }
    })
  },

  reqCheckOut:function(param) {
    const _this = this
    const app = getApp()
    wx.request({
      method: "PUT",
      url: app.globalData.reqUrl + '/api/user/reserve/',
      data:param,
      header: {
        'content-type': 'application/json',
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          _this.setData({
            leave:true,
          })
        } else {
          app.reqFail("签退失败")
        }
      },
      fail() {
        app.reqFail("签退失败")
      },
    })
  },
})