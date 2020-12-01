Page({
  data: {
    // 滚动图片
    gallery_imgs: [
      '/res/test/stadium_1.jpg',
      '/res/test/stadium_2.jpg',
      '/res/test/stadium_3.jpeg'
    ],
    // 是否筛选
    sort_dis:'nosort',
    sort_score:'nosort',
    sort_pop:'nosort',
    // 场馆信息
    stadium_list:[],
  },

  // 设置场馆信息
  setStadiumInfo:function(res, add=true) {
    const _this = this
    const app = getApp()
    console.log(res.data)
    var newList = []
    for(var info of res.data) {
      console.log(info)
      var sports = ''
      var dis = 0
      var imgPath = ''
      for(var sport of info.courtTypes) {
        sports = sports + sport.type + ' '
      }
      if(info.images.length > 0) {
        imgPath = app.globalData.reqUrl + info.images[0].image
      }
      newList.push({
        id:info.id,
        name:info.name,
        star:info.score,
        comment_num:info.comments,
        opentime:info.openTime + '-' + info.closeTime,
        sports:sports,
        pos:info.location,
        la:info.latitude,
        lo:info.longitude,
        dis:dis,
        favor:info.collect,
        imgpath:imgPath,
      });
    }
    if(add) {
      let oldList = this.data.stadium_list;
      oldList.push(...newList);
      this.setData({
        stadium_list:oldList
      })
    } else {
      this.setData({
        stadium_list:newList
      })
    }
  },

  // 创建时请求信息
  onLoad: function (options) {
    const _this = this
    this.reqStadiumInfo()
    wx.startLocationUpdate({
      success: (res) => {},
      fail:() => {
        wx.showToast({
          title: '无法获取位置信息,请检查是否开启定位功能',
          icon:'none',
        })
      }
    })
    wx.onLocationChange((result) => {this.updateDis(result.latitude, result.longitude)})
  },

  // 下拉刷新页面
  onPullDownRefresh:function() {
    this.reqStadiumInfo()
    this.setData({
      sort_dis:'nosort',
      sort_score:'nosort',
      sort_pop:'nosort',
    })
  },

  // 排序键按下
  sortdis:function() {
    if(this.data.sort_dis==='nosort') {
      this.setData({sort_dis:'sort', sort_score:'nosort', sort_pop:'nosort'})
      this.sortStadium('dis', false)
    } else {
      this.setData({sort_dis:'nosort'})
      this.sortStadium('id', false)
    }
  },

  sortscore:function() {
    if(this.data.sort_score==='nosort') {
      this.setData({sort_dis:'nosort', sort_score:'sort', sort_pop:'nosort'})
      this.sortStadium('star', true)
    } else {
      this.setData({sort_score:'nosort'})
      this.sortStadium('id', false)
    }
  },

  sortpop:function() {
    if(this.data.sort_pop==='nosort') {
      this.setData({sort_dis:'nosort', sort_score:'nosort', sort_pop:'sort'})
      this.sortStadium('comment_num', true)
    } else {
      this.setData({sort_pop:'nosort'})
      this.sortStadium('id', false)
    }
  },

  // 排序函数
  sortStadium(key, desc) {
    let oldList = this.data.stadium_list
    oldList.sort(function(a,b) {
    　return desc ? ((parseInt(a[key]) < parseInt(b[key]))?1:((parseInt(a[key]) > parseInt(b[key]))?-1:0)):((parseInt(a[key]) < parseInt(b[key]))?-1:((parseInt(a[key]) > parseInt(b[key]))?1:0))  //杠杠的，注意括号就是！
    })
    this.setData({stadium_list:oldList})
  },

  // 计算距离
  calDistance:function(la1, lo1, la2, lo2) {
    var La1 = la1 * Math.PI / 180.0;
    var La2 = la2 * Math.PI / 180.0;
    var La3 = La1 - La2;
    var Lb3 = lo1 * Math.PI / 180.0 - lo2 * Math.PI / 180.0;
    var s = 2 * Math.asin(Math.sqrt(Math.pow(Math.sin(La3 / 2), 2) + Math.cos(La1) * Math.cos(La2) * Math.pow(Math.sin(Lb3 / 2), 2)));
       s = s * 6378.137;//地球半径
       s = Math.round(s * 10000) / 10000;
    return s
   },

   // 更新距离
   updateDis:function(la, lo) {
     var len = this.data.stadium_list.length
     for(var i=0; i<len; i++) {
       let info = this.data.stadium_list[i]
       let newDis = parseInt(this.calDistance(la, lo, info.la, info.lo))
       let updateItem = 'stadium_list[' + i + '].dis'
       this.setData({[updateItem]: newDis})
     }
   },

   // 添加收藏
   addFavor:function(e) {
    const targetId = e.currentTarget.dataset.stadiumid
    this.reqAddFavor(targetId)
   },

   // 删除收藏
   removeFavor:function(e) {
    const targetId = e.currentTarget.dataset.stadiumid
    this.reqRemoveFavor(targetId)
   },

/*--------------------------------------------------
   网络请求函数
---------------------------------------------------*/

  // 请求场馆信息
  reqStadiumInfo:function() {
    const _this = this
    const app = getApp()
    wx.request({
      method: "GET",
      url: app.globalData.reqUrl + '/api/user/stadium/',
      data: {},
      header: {
        'content-type': 'application/json',
        'loginToken': 1,
      },
      success(res) {
        if(res.data.error === null || res.data.error === undefined) {
          _this.reqSuccess("获取信息成功")
          _this.setStadiumInfo(res)
        } else {
          _this.reqFail("操作失败")
        }
      },
      fail() {
        _this.reqFail("获取信息失败")
      },
      complete() {
        wx.stopPullDownRefresh({
          success: (res) => {},
        })
      },
    })
  },

  // 收藏/取消收藏
  reqAddFavor:function(stadiumId) {
    const _this = this
    const app = getApp()
    var updateItem = 'stadium_list[' + stadiumId + '].favor'
    wx.request({
      method: "POST",
      url: app.globalData.reqUrl + '/api/user/collect/',
      data: {
        'stadium_id':stadiumId,
      },
      header: {
        'content-type': 'application/json',
        'loginToken': 1,
      },
      success(res) {
        if(res.data.error === null || res.data.error === undefined) {
          _this.reqSuccess("收藏成功")
          _this.setData({[updateItem]:true})
        } else {
          _this.reqFail("操作失败")
        }
      },
      fail() {
        _this.reqFail("操作失败")
      },
    })
  },

  reqRemoveFavor:function(stadiumId) {
    const _this = this
    const app = getApp()
    var updateItem = 'stadium_list[' + stadiumId + '].favor'
    wx.request({
      method: "DELETE",
      url: app.globalData.reqUrl + '/api/user/collect/',
      data: {
        'stadium_id':stadiumId,
      },
      header: {
        'content-type': 'application/json',
        'loginToken': 1,
      },
      success(res) {
        if(res.data.error === null || res.data.error === undefined) {
          _this.reqSuccess("取消收藏成功")
          _this.setData({[updateItem]:false})
        } else {
          _this.reqFail("操作失败")
        }
      },
      fail() {
        _this.reqFail("操作失败")
      },
    })
  },

  // 请求成功/失败时的行为
  reqSuccess:function(message) {
    console.log('Get Info success!')
    if(message !== "") {
      wx.showToast({
        title: message,
        icon:'none',
        duration:1000
      })
    }
  },

  reqFail:function(message) {
    console.log('Get Info fail!')
    if(message !== "") {
      wx.showToast({
        title: message,
        icon:'none',
        duration:1000
      })
    }
  },

/*--------------------------------------------------
   页面跳转函数
---------------------------------------------------*/
  jmpInfo:function(e) {
    console.log(e.currentTarget.dataset.stadiumid)
    wx.navigateTo({
      url: '/pages/stadium/info/stadium?'+'id='+e.currentTarget.dataset.stadiumid,
    })
  },

  jmpSearch:function(e) {
    wx.navigateTo({
      url: '/pages/home/result/result',
    })
  },
})