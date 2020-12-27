// pages/stadium/stadium.js
import Toast from '../../../miniprogram/miniprogram_npm/@vant/weapp/toast/toast';
Page({
  data: {
    // 场馆id
    stadium_id:Number,
    stadium_name:'',
    // 滚动图片test
    gallery_imgs: [
      
    ],
    // 评论列表
    comment_list: [],
    empty_comment:false,
    // 图片资源
    map_select_img:getApp().globalData.imgUrl+'/res/imgs/tab_map_select.png',
    info_img:getApp().globalData.imgUrl+'/res/imgs/stadium_info.png',
    notice_img:getApp().globalData.imgUrl+'/res/imgs/stadium_notice.png',
    comment_img:getApp().globalData.imgUrl+'/res/imgs/stadium_comment.png',
    star_img:getApp().globalData.imgUrl+'/res/imgs/info_star.png',
    isfavor_img:getApp().globalData.imgUrl+'/res/imgs/info_isfavor.png',
    notfavor_img:getApp().globalData.imgUrl+'/res/imgs/info_notfavor.png',
  },

  onLoad:function(options) {
    this.setData({stadium_id:options.id})
    this.reqStadiumDetail()
  },

  onShow:function() {
    this.reqCommentInfo()
  },

  // 设置场馆信息
  setStadiumInfo:function(res) {
    var info = res.data[0]
    var newLaLo = this.bdMap_to_txMap(info.latitude, info.longitude)
    var dis = 0
    var imgList = []
    for (var imgInfo of info.images) {
      imgList.push(imgInfo.image)
    }

    this.setData({
      stadium_name:info.name,
      intro:info.information,
      notice:info.notice,
      open_time:info.openTime+" - "+info.closeTime,
      phone:info.contact,
      pos:info.location,
      collect:info.collect,
      la:newLaLo.latitude,
      lo:newLaLo.longitude,
      dis:dis,
      gallery_imgs:imgList
    })

    // 距离信息  
    const _this = this
    wx.getLocation({
      type: 'gcj02',
      success: function (res) {
        _this.setData({
          dis: parseInt(1000 * _this.calDistance(res.latitude, res.longitude, _this.data.la, _this.data.lo))
        })
      }
    })
  },

  // 设置评论信息
  setCommentInfo:function(res) {
    var newList = []
    for(var info of res.data.results) {
      var imgList = []
      for(var img of info.images) {
        imgList.push(img.image)
      }
      var date = new Date(info.createTime)
      var dateText = date.getFullYear()+'-'+date.getMonth()+'-'+date.getDay()+' '+date.getHours()
      +':'+date.getMinutes()
      newList.push({
        headerPath:info.userImage,
        name:info.userName,
        date:dateText,
        score:info.score,
        content:info.content,
        imgs:imgList
      })
    }

    this.setData({
      comment_list:newList,
      empty_comment:(newList.length === 0),
    })
  },

   // 添加收藏
   addFavor:function(e) {
    this.reqAddFavor()
   },

   // 删除收藏
   removeFavor:function(e) {
    this.reqRemoveFavor()
   },

  /*--------------------------------------------------
    地理位置计算函数
  ---------------------------------------------------*/
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
       let newDis = parseInt(this.calDistance(la, lo, info.la, info.lo)*1000)
       let updateItem = 'stadium_list[' + i + '].dis'
       this.setData({[updateItem]: newDis})
     }
     this.filterStadium()
   },

   // 百度地图经纬度转腾讯地图
   bdMap_to_txMap:function($lat,$lng){
    var $x_pi = 3.14159265358979324 * 3000.0 / 180.0
    var $x = $lng - 0.0065
    var $y = $lat - 0.006
    var $z = Math.sqrt($x * $x + $y * $y) - 0.00002 * Math.sin($y * $x_pi)
    var $theta = Math.atan2($y, $x) - 0.000003 * Math.cos($x * $x_pi)
    var $lng = $z * Math.cos($theta)
    var $lat = $z * Math.sin($theta)
    return {'longitude':$lng,'latitude':$lat}
  },

  /*--------------------------------------------------
    页面跳转函数
  ---------------------------------------------------*/
  jmpBooking:function() {
    // 请求推送通知权限
    try {
      wx.requestSubscribeMessage({
        tmplIds: ['FLIjh95XJrOzgWWImzmXttYhs4eoCf9e6VAid0QjHbI',
        'PdZ2sYAT_HXIkmho2wjfIbMS822H1f4d0xqiKFI6qgs', 'hf9hHSc8OEHfmwicqL4rqLGaDwwJ5NRG4usDQwEJ7Mc'],
        success (res) { 
          console.log(res)
        }
      })
   } catch(e) {
     wx.showToast({
       title: '无法启动通知服务，请检查您的小程序版本是否过低',
       icon:'none',
       duration:2000,
     })
   }
    wx.navigateTo({
      url: '/pages/book/book/book?id='+this.data.stadium_id,
    })
  },

  jmpMap:function() {
    getApp().globalData.seekStadiumId = this.data.stadium_id
    wx.switchTab({
      url: '/pages/map/map',
    })
  },

  jmpAllcomment:function() {
    wx.navigateTo({
      url: '/pages/stadium/allcomment/allcomment?id='+this.data.stadium_id,
    })
  },

  /*--------------------------------------------------
    网络请求函数
  ---------------------------------------------------*/
  // 请求场馆具体信息
  reqStadiumDetail:function() {
    Toast.loading({
      message: '加载中...',
      forbidClick: true,
    })
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
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          _this.setStadiumInfo(res,false)
        } else {
          app.reqFail('获取信息失败')
        }
      },
      fail() {
        app.reqFail('获取信息失败')
      },
      complete() {
        setTimeout(()=>{
          Toast.clear()
        },100)
      },
    })
  },

  // 收藏/取消收藏
  reqAddFavor:function() {
    const _this = this
    const app = getApp()
    wx.request({
      method: "POST",
      url: app.globalData.reqUrl + '/api/user/collect/',
      data: {
        'stadium_id':_this.data.stadium_id,
      },
      header: {
        'content-type': 'application/json',
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          app.reqSuccess("收藏成功")
          _this.setData({collect:res.data.id})
        } else {
          app.reqFail("收藏失败")
        }
      },
      fail() {
        app.reqFail("收藏失败")
      },
    })
  },

  reqRemoveFavor:function() {
    const _this = this
    const app = getApp()
    wx.request({
      method: "DELETE",
      url: app.globalData.reqUrl + '/api/user/collect/',
      data: {
        'collect_id':_this.data.collect,
      },
      header: {
        'content-type': 'application/json',
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          app.reqSuccess("取消收藏成功")
          _this.setData({collect:null})
        } else {
          app.reqFail("取消收藏失败")
        }
      },
      fail() {
        app.reqFail("取消收藏失败")
      },
    })
  },

  // 请求评论信息
  reqCommentInfo:function() {
    const _this = this
    const app = getApp()
    wx.request({
      method: "GET",
      url: app.globalData.reqUrl + '/api/user/comment/',
      data: {
        'stadium_id':_this.data.stadium_id,
      },
      header: {
        'content-type': 'application/json',
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          _this.setCommentInfo(res)
        } else {
          app.reqFail("获取评论信息失败")
        }
      },
      fail() {
        app.reqFail("获取评论信息失败")
      },
    })
  },
})