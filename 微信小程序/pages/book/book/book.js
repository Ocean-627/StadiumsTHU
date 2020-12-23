// pages/stadium/book.js
import Toast from '../../../miniprogram/miniprogram_npm/@vant/weapp/toast/toast';
Page({
  data: {
    // 步骤
    activeStep: 0,
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

    //场地 
    activeName: '1',
    
    // 场馆信息
    stadium_id:Number,
    stadium_name:'',
    fore_day:Number,
    sports_list: [],
    date_list: [],

    // 用户选择信息
    choose_sport:'',
    choose_sport_idx:Number,
    choose_date:0,
    choose_court:'',

    // 场地信息
    court_list:[],
    duration_list:{},
    choose_duration_list:[],

    // 同时可选择的最多时间段
    max_duration_num:3,

    // 下方菜单提示
    show_error:true,
    error_text:'您还没有选择任何时间段',
    duration_text: '',
    court_desc:'',
    time_desc:'',

    // 确认时间
    show_verify:false,
    handlingBook:false,
    
    // 运动->图标映射
    sportsIconTable:{
      '乒乓球':getApp().globalData.imgUrl+'/res/sports/tabletennis.png',
      '体操':getApp().globalData.imgUrl+'/res/sports/gym.png',
      '台球':getApp().globalData.imgUrl+'/res/sports/billiard.png',
      '射箭':getApp().globalData.imgUrl+'/res/sports/archery.png',
      '羽毛球':getApp().globalData.imgUrl+'/res/sports/badminton.png',
      '篮球':getApp().globalData.imgUrl+'/res/sports/basketball.png',
      '足球':getApp().globalData.imgUrl+'/res/sports/football.png',
      '游泳':getApp().globalData.imgUrl+'/res/sports/swim.png',
      '排球':getApp().globalData.imgUrl+'/res/sports/volleyball.png',
      '保龄球':getApp().globalData.imgUrl+'/res/sports/bowling.png',
    }
  },

  onLoad:function(options) {
    Toast.loading({
      message: '加载中...',
      forbidClick: true,
    })
    this.setData({stadium_id:options.id})
    this.reqStadiumInfo()
  },

  // 下拉刷新页面
  onPullDownRefresh:function() {
    Toast.loading({
      message: '加载中...',
      forbidClick: true,
    })
    this.setData({
      choose_duration_list:[],
    })
    this.reqStadiumInfo()
    this.updateDuration()
  },

  // 切换场地
  onChangeCourt:function(e) {
    if(e.detail !== '') {
      var timeList = this.data.duration_list[e.detail]
      if(timeList !== undefined && timeList !== null) {
        for(var dur of timeList) {
          dur.choose = false
        }
        var updateItem = 'duration_list.' + e.detail
        this.setData({
          [updateItem]:timeList
        })
      }
    }
    this.setData({
      activeName: e.detail,
      choose_duration_list:[],
    });
    this.updateDuration()
  },

  // 切换日期
  onChangeDate:function(e) {
    Toast.loading({
      message: '加载中...',
      forbidClick: true,
    })
    this.setData({
      choose_date: e.detail,
      choose_duration_list:[],
    })
    this.updateDuration()
    this.reqDurationInfo()
  },

  // 选择时段
  onSelectTime:function(e) {
    var courtId = e.currentTarget.dataset.courtid
    var timeIndex = e.currentTarget.dataset.timeindex
    var updateItem = 'duration_list.' + courtId + '[' + timeIndex + '].choose'
    this.setData({[updateItem]:e.detail})
    if(e.detail) {
      this.data.choose_duration_list.push(this.data.duration_list[courtId][timeIndex])
    } else {
      var rmItem = this.data.choose_duration_list.findIndex((item,index)=>{
        return item.id === this.data.duration_list[courtId][timeIndex].id
      })
      this.data.choose_duration_list.splice(rmItem,1)
    }
    this.updateDuration()
  },

  // 切换运动项目
  onChangeSport:function(e) {
    Toast.loading({
      message: '加载中...',
      forbidClick: true,
    })
    var type = e.currentTarget.dataset.sport
    // 切换当前选中的运动项目
    var idx = e.currentTarget.dataset.idx
    var oldidx = this.data.choose_sport_idx
    var oldChooseItem = 'sports_list[' + oldidx + '].choose'
    var newChooseItem = 'sports_list[' + idx + '].choose'

    this.setData({
      choose_sport: type,
      activeName:'1',
      [oldChooseItem]:'',
      [newChooseItem]:'choose',
      choose_sport_idx:idx,
      choose_duration_list:[]
    })
    this.updateDuration()
    this.reqCourtInfo()
  },

  // 设置选择时间提示
  updateDuration:function() {
    if(this.data.choose_duration_list.length > this.data.max_duration_num) {
      this.setData({
        show_error:true,
        error_text:'单次预约的时间段不能超过'+this.data.max_duration_num+'个',
      })
    }
    else if(this.data.choose_duration_list.length <= 0) {
      this.setData({
        show_error:true,
        error_text:'您还未选择任何时间段',
      })
    }
    else {
      var dList = this.data.choose_duration_list
      dList.sort((a,b)=>a.id-b.id)
      for(var i=1; i<dList.length; i++) {
        if(dList[i-1].endTime !== dList[i].startTime) {
          this.setData({
            show_error:true,
            error_text:'请选择连续的时间段',
          })
          return
        }
      }
      var dText = dList[0].startTime + '-' + dList[dList.length-1].endTime
      this.setData({
        show_error:false,
        duration_text:dText,
      })
    }
  },

  // 设置场馆信息
  setStadiumInfo(res) {
    var sportsList = []
    this.setData({
      stadium_name:res.data[0].name,
      fore_day:res.data[0].foreDays,
    })
    // 设置日期选择栏
    var timestamp = Date.parse(new Date())
    var dateList = []
    for(var i=0; i<this.data.fore_day; i++) {
      dateList.push(this.stampToDate(timestamp+i*86400000))
    }
    this.setData({date_list:dateList})
    // 设置运动项目
    for(var sport of res.data[0].courtTypes) {
      sportsList.push({
        id:sport.id,
        type:sport.type,
        icon:this.data.sportsIconTable[sport.type],
        choose:''
      })
    }
    
    this.setData({sports_list:sportsList})
    if(this.data.choose_sport === '') {
      this.setData({
        choose_sport:this.data.sports_list[0].type,
        ['sports_list[0].choose']:'choose',
        choose_sport_idx:0,
      })
    }

    this.reqCourtInfo()
  },

  // 设置场地信息
  setCourtInfo:function(res) {
    var courtList = []
    for(var info of res.data) {
      courtList.push({
        id:info.id,
        name:info.name,
        openState:info.openState,
        price:info.price
      })
    }
    this.setData({court_list:courtList})
    this.reqDurationInfo()
  },

  // 设置时段信息
  setDurationInfo:function(res) {
    var newDurationList = {}
    for(var info of res.data) {
      if(newDurationList[info.court] === undefined) {
        newDurationList[info.court] = []
      }
      newDurationList[info.court].push({
        id:info.id,
        startTime:info.startTime,
        endTime:info.endTime,
        openState:info.openState,
        accessible:info.accessible,
        choose:false,
        courtId:info.court,
      })
    }
    this.setData({duration_list:newDurationList})
  },

  // 时间戳转日期
  stampToDate(stamp) {
    var date = new Date(stamp);
    //获取年份  
    var Y =date.getFullYear();
    //获取月份  
    var M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1);
    //获取当日日期 
    var D = date.getDate() < 10 ? '0' + date.getDate() : date.getDate();
    var result = {
      text:M+"月"+D+"日",
      param:Y+'-'+M+'-'+D
    }
    return result
  },

  // 中文日期转请求参数
  dateToParam(date) {
    var str = String(date).replace("月",".")
    str = str.replace("日","")
    return str
  },

  // 显示确认菜单
  showVerify:function() {
    // 寻找场地名称
    var courtName = ''
    for(var court of this.data.court_list) {
      if(parseInt(court.id) === parseInt(this.data.activeName)) {
        courtName = court.name
        break
      }
    }
    this.setData({
      show_verify:true,
      activeStep:1,
      court_desc:courtName,
      time_desc:this.data.date_list[this.data.choose_date].text+this.data.duration_text,
    })
  },

  // 确认菜单关闭点击
  on_bottom_close:function() {
    this.setData({
      show_verify:false,
      activeStep:0,
    })
  },

  // 用户决定预约
  onBookReq:function() {
    this.setData({
      handlingBook:true
    })
    // 设置历史记录
    const app = getApp()
    try{
      var oldHis = JSON.parse(wx.getStorageSync('visitHistory'))
      oldHis.push({
        type:'预定',
        target:{
          name:this.data.stadium_name+this.data.court_desc,
          id:this.data.stadium_id,
        },
        time:app.getCurrentTime()
      })
      oldHis = oldHis.slice(-app.globalData.maxRecordNum)
      wx.setStorageSync('visitHistory', JSON.stringify(oldHis))
    } catch(e) {}
    if(this.data.choose_duration_list.length === 1) {
      this.reqBooking()
    }
    else if(this.data.choose_duration_list.length > 1) {
      this.reqMulBooking()
    }
  },

  /*--------------------------------------------------
    页面跳转函数
  ---------------------------------------------------*/
  // 付款页面跳转
  jmpPay:function(id,stadiumId) {
    wx.redirectTo({
      url: '/pages/book/pay/pay?id='+id+'&stadium='+stadiumId+'&directFrom=book'
    })
  },

  /*--------------------------------------------------
    网络请求函数
  ---------------------------------------------------*/
  // 请求场地信息
  reqStadiumInfo:function() {
    const _this = this
    const app = getApp()
    wx.request({
      method: "GET",
      url: app.globalData.reqUrl + '/api/user/stadiumdetail/',
      data: {
        'id': _this.data.stadium_id
      },
      header: {
        'content-type': 'application/json',
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        if((res.statusCode === 200) && (res.data.error === undefined || res.data.error === null)) {
          _this.setStadiumInfo(res)
        } else {
          app.reqFail('获取信息失败')
        }
      },
      fail() {
        app.reqFail('获取信息失败')
      },
      complete() {
      },
    })
  },

  // 请求具体场地信息
  reqCourtInfo:function() {
    const _this = this
    const app = getApp()
    wx.request({
      method: "GET",
      url: app.globalData.reqUrl + '/api/user/court/',
      data: {
        'type':_this.data.choose_sport,
        'stadium_id':_this.data.stadium_id,
      },
      header: {
        'content-type': 'application/json',
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        if((res.statusCode === 200) && (res.data.error === undefined || res.data.error === null)) {
          _this.setCourtInfo(res)
        } else {
          app.reqFail('获取场地信息失败')
        }
      },
      fail() {
        app.reqFail('获取场地信息失败')
      },
      complete() {
      },
    })
  },

  // 请求时段信息
  reqDurationInfo:function() {
    const _this = this
    const app = getApp()
    const dateParam = this.data.date_list[this.data.choose_date].param
    wx.request({
      method: "GET",
      url: app.globalData.reqUrl + '/api/user/duration/',
      data: {
        'type':_this.data.choose_sport,
        'stadium_id':_this.data.stadium_id,
        'date':dateParam,
      },
      header: {
        'content-type': 'application/json',
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        Toast.clear()
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          _this.setDurationInfo(res)
        } else {
          app.reqFail('获取时段信息失败')
        }
      },
      fail() {
        Toast.clear()
        app.reqFail('获取时段信息失败')
      },
      complete() {
        // 结束下拉刷新
        wx.stopPullDownRefresh({
          success: (res) => {},
        })
      },
    })
  },

  // 发送预约请求
  reqBooking:function() {
    const _this = this
    const app = getApp()
    wx.request({
      method: "POST",
      url: app.globalData.reqUrl + '/api/user/reserve/',
      data: {
        'duration_id':_this.data.choose_duration_list[0].id
      },
      header: {
        'content-type': 'application/json',
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          _this.jmpPay(res.data.id, res.data.stadium_id)
        } else {
          _this.setData({
            show_verify:false,
            activeStep:0,
            handlingBook:false
          })
          app.reqFail('预定失败，请刷新页面后重试')
        }
      },
      fail() {
        _this.setData({
          show_verify:false,
          activeStep:0,
          handlingBook:false
        })
        app.reqFail('预定失败，请刷新页面后重试')
      },
      complete() {
      },
    })
  },

  // 发送多时段预约请求
  reqMulBooking:function() {
    const _this = this
    const app = getApp()
    wx.request({
      method: "POST",
      url: app.globalData.reqUrl + '/api/user/batchreserve/',
      data: {
        'duration_id':_this.data.choose_duration_list[0].id,
        'startTime':_this.data.choose_duration_list[0].startTime,
        'endTime':_this.data.choose_duration_list[_this.data.choose_duration_list.length-1].endTime,
      },
      header: {
        'content-type': 'application/json',
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          _this.jmpPay(res.data.id, res.data.stadium_id)
        } else {
          _this.setData({
            show_verify:false,
            activeStep:0,
            handlingBook:false
          })
          app.reqFail('预定失败，请刷新页面后重试')
        }
      },
      fail() {
        _this.setData({
          show_verify:false,
          activeStep:0,
          handlingBook:false
        })
        app.reqFail('预定失败，请刷新页面后重试')
      },
      complete() {
      },
    })
  }
})