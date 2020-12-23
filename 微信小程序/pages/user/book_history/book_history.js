import Toast from '../../../miniprogram/miniprogram_npm/@vant/weapp/toast/toast';
import Dialog from '../../../miniprogram/miniprogram_npm/@vant/weapp/dialog/dialog';
Page({
  data: {
    // 预定信息
    booking_list:[],
    // 当前页面
    current_type:0,
    // 请求参数
    queryList:[
      { leave:true },
      { has_comments:false, leave:true },
      { has_comments:true },
      { cancel:true },
    ],
    statusList:[
      '已完成','待评论','已评论','已取消'
    ],
    // 当前状态
    curStat:0,
    // 当前分页
    curPage:1,
    // 到达底部
    toBottom:false,
  },

  onLoad:function() {
    this.reqBookInfo(0)
  },

  // 页面卸载
  onUnload:function() {
    wx.switchTab({
      url: '/pages/user/index/user',
    })
  },

  // 页面下拉分页
  onReachBottom:function() {
    if(this.data.toBottom) {
      return
    }
    const newPage = this.data.curPage+1
    this.setData({curPage:newPage})
    this.reqBookInfo(this.data.curStat,true)
  },

  // 设置预约记录
  setBookingList:function(res, statId, add = false) {
    var newList = []
    if(add) {
      newList = this.data.booking_list
    }
    var status = ''
    var stat = this.data.statusList[statId]

    for(var info of res.data.results) {
      if(statId !== 0) {
        // 固定筛选某个状态，不需要判断
        status = stat
      } 
      else {
        if(info.cancel === true) {
          status = '已取消'
        }
        else if(info.payment === false) {
          status = '待付款'
          continue
        } 
        else if(info.checked === false) {
          status = '已付款'
          continue
        } 
        else if(info.leave === false) {
          status = '进行中'
          continue
        } 
        else if(info.has_comments === false) {
          status = '待评论'
        } 
        else {
          status = '已评论'
        }
      }
    
      newList.push({
        id:info.id,
        stadium_id:info.stadium_id,
        stadium_name:info.stadium,
        court_name:info.court,
        book_time:info.date+' '+info.startTime+'-'+info.endTime,
        price:info.price+'.00',
        status:status,
        imgPath:info.image,
        pay:info.payment,
        checked:info.checked,
        leave:info.leave,
        comment:info.has_comments,
        cancel:info.cancel,
      })
    }
    this.setData({
      booking_list:newList,
      empty:(newList.length === 0)
    })
  },

  // 切换筛选条件
  onChangeTab:function(e) {
    const idx = e.detail.index
    this.setData({
      curStat:idx,
    })
    this.reqBookInfo(idx)
  },

  // 从列表中移除某项
  removeBookInfo:function(idx) {
    let newList = this.data.booking_list
    newList.splice(idx,1)
    this.setData({
      booking_list:newList,
      empty:(newList.length === 0),
    })
  },

  /*----------------------------------
    按钮功能函数
  -----------------------------------*/
  // 删除记录
  deleteRecord:function(e) {
    const bookId = e.currentTarget.dataset.bookid
    const idx = e.currentTarget.dataset.idx
    const _this = this
    // 弹出提示
    Dialog.confirm({
      title:'温馨提示',
      message:'删除记录操作无法恢复，是否确认继续？',
    })
    .then(()=>{
      // 确认
      _this.reqDeleteRecord(bookId, idx)
    })
  },

  /*----------------------------------
    页面跳转函数
  -----------------------------------*/
  // 跳转到详细信息
  jmpInfo:function(e) {
    const stadiumId = e.currentTarget.dataset.stadiumid
    wx.navigateTo({
      url: '/pages/stadium/info/stadium?id='+stadiumId,
    })
  },

  // 跳转到付款
  jmpPay:function(e) {
    const bookId = e.currentTarget.dataset.bookid
    wx.navigateTo({
      url: '/pages/book/pay/pay?'+'id='+bookId,
    })
  },

  // 跳转到评论
  jmpComment:function(e) {
    const bookId = e.currentTarget.dataset.bookid
    wx.navigateTo({
      url: '/pages/stadium/comment/comment?'+'id='+bookId+'&type=comment',
    })
  },

  // 跳转到查看评论
  jmpViewComment:function(e) {
    const bookId = e.currentTarget.dataset.bookid
    wx.navigateTo({
      url: '/pages/stadium/comment/comment?'+'id='+bookId+'&type=view',
    })
  },

  /*----------------------------------
    网络请求函数
  -----------------------------------*/
  reqBookInfo:function(statusId, add=false) {
    Toast.loading({
      message: '加载中...',
      forbidClick: true,
    })
    const _this = this
    const app = getApp()
    const queryData = Object.assign(this.data.queryList[statusId], 
      {page:this.data.curPage})
    wx.request({
      method: "GET",
      url: app.globalData.reqUrl + '/api/user/reserve/',
      data: queryData,
      header: {
        'content-type': 'application/json',
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          _this.setBookingList(res, statusId, add)
        } else {
          app.reqFail("获取信息失败")
        }
      },
      fail() {
        app.reqFail("获取信息失败")
      },
      complete() {
        Toast.clear()
        wx.stopPullDownRefresh({
          success: (res) => {},
        })
      },
    })
  },

  // 删除历史记录
  reqDeleteRecord:function(bookId, idx) {
    Toast.loading({
      message: '删除中...',
      forbidClick: true,
    })

    const _this = this
    const app = getApp()
    wx.request({
      method: "DELETE",
      url: app.globalData.reqUrl + '/api/user/reserve/',
      data:{
        id:bookId
      },
      header: {
        'content-type': 'application/json',
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          _this.removeBookInfo(idx)
          app.reqSuccess("删除成功")
        }  
        else if(res.data.error.detail === 'Invalid page.') {
          _this.setData({ toBottom:true })
        }
        else {
          app.reqFail("获取信息失败")
        }
      },
      fail() {
        app.reqFail("操作失败")
      },
      complete() {
        Toast.clear()
      },
    })
  }
})