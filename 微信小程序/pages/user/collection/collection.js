// pages/user/collection/collection.js
import Toast from '../../../miniprogram/miniprogram_npm/@vant/weapp/toast/toast';
Page({
  data: {
    // 收藏列表
    collect_list:[],
    // 图片资源url
    starUrl:getApp().globalData.imgUrl+'/res/imgs/info_star.png',
    // 是否为空
    empty:false,
  },

  onLoad: function (options) {
    Toast.loading({
      message: '加载中...',
      forbidClick: true,
    });
    this.reqCollectInfo()
  },

  // 设置收藏信息
  setCollectInfo:function(res) {
    var newList = []
    for(var info of res.data) {
      if(info.collect !== null && info.collect !== undefined) {
        var sports = ''
        var imgPath = ''
        for(var sport of info.courtTypes) {
          sports = sports + sport.type + ' '
        }
        if(info.images.length > 0) {
          imgPath = info.images[0].image
        }
        newList.push({
          id:info.id,
          name:info.name,
          star:info.score,
          comment_num:info.comments,
          opentime:info.openTime + '-' + info.closeTime,
          sports:sports,
          pos:info.location,
          imgpath:imgPath,
          open:info.openState,
          collect:info.collect
        })
      }
    }
    this.setData({
      collect_list:newList,
      empty:(newList.length === 0),
    })
  },

  // 取消收藏
  cancelCollect:function(e) {
    const collectid = e.currentTarget.dataset.collectid
    const idx = e.currentTarget.dataset.idx
    this.reqRemoveFavor(collectid, idx)
  },

  // 移除列表项
  rmListItem:function(idx) {
    let curList = this.data.collect_list
    curList.splice(idx,1)
    this.setData({
      collect_list:curList,
      empty:(curList.length === 0),
    })
  },

  // 下拉刷新页面
  onPullDownRefresh:function() {
    this.reqCollectInfo(true)
  },

  /*------------------------------------------
  网络请求函数
  -------------------------------------------*/
  reqCollectInfo:function(refresh=false) {
    const _this = this
    const app = getApp()
    wx.request({
      method: "GET",
      url: app.globalData.reqUrl + '/api/user/stadium/',
      data: {},
      header: {
        'content-type': 'application/json',
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        Toast.clear()
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          _this.setCollectInfo(res)
          if(refresh) {
            app.reqSuccess('刷新成功')
          }
        } else {
          app.reqFail('获取收藏信息失败')
        }
      },
      fail() {
        Toast.clear()
        app.reqFail('获取收藏信息失败')
      },
      complete() {
        // 结束下拉刷新
        wx.stopPullDownRefresh({
          success: (res) => {},
        })
      },
    })
  },

  // 取消收藏
  reqRemoveFavor:function(collectId, idx) {
    const _this = this
    const app = getApp()
    wx.request({
      method: "DELETE",
      url: app.globalData.reqUrl + '/api/user/collect/',
      data: {
        'collect_id':collectId,
      },
      header: {
        'content-type': 'application/json',
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          app.reqSuccess("取消收藏成功")
          _this.rmListItem(idx)
        } else {
          app.reqFail("操作失败")
        }
      },
      fail() {
        app.reqFail("操作失败")
      },
    })
  },

  /*------------------------------------------
  页面跳转函数
  -------------------------------------------*/
  jmpInfo:function(e) {
    wx.navigateTo({
      url: '/pages/stadium/info/stadium?'+'id='+e.currentTarget.dataset.stadiumid,
    })
  },

  jmpMain:function(e) {
    wx.switchTab({
      url: '/pages/home/index/home',
    })
  }
})