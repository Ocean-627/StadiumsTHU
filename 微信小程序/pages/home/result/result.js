Page({
  data:{
    stadium_list:[],
    filter_text:'',
    star_img:getApp().globalData.imgUrl+'/res/imgs/info_star.png',
  },

  // 设置场馆信息
  setStadiumInfo:function(res, updatePos=true) {
    var newList = []
    var value = this.data.filter_text
    
    for(var info of res.data) {
      if(info.name.indexOf(value) !== -1 || 
      (info.pinyin !== null && info.pinyin.indexOf(value) !== -1)) {
        var sports = ''
        var dis = 0
        var imgPath = ''
        for(var sport of info.courtTypes) {
          sports = sports + sport.type + ' '
        }
        if(info.images.length > 0) {
          imgPath = info.images[0].image
        }
        var newLaLo = this.bdMap_to_txMap(info.latitude, info.longitude)

        newList.push({
          id:info.id,
          name:info.name,
          star:info.score,
          comment_num:info.comments,
          opentime:info.openTime + '-' + info.closeTime,
          sports:sports,
          pos:info.location,
          la:newLaLo.latitude,
          lo:newLaLo.longitude,
          dis:dis,
          collect:info.collect,
          imgpath:imgPath,
          open:info.openState
        });
      }
    }
    this.setData({stadium_list:newList})

    // 更新位置信息
    var _this = this
    if(updatePos) {
      wx.getLocation({
        type: 'gcj02',
        success: function (res) {
          wx.showToast({
            title: '获取位置信息成功',
            icon: 'none',
            duration:1000
          })
          _this.updateDis(res.latitude, res.longitude)
        },
        fail: function() {
          wx.showToast({
            title: '获取位置信息失败',
            icon: 'none',
            duration:1000
          })
        }
      })
    }
  },

  // 创建时请求信息
  onLoad: function (options) {
    this.data.filter_text = options.search
    this.reqStadiumList()
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

   updateDis:function(la, lo) {
     var len = this.data.stadium_list.length
     for(var i=0; i<len; i++) {
       let info = this.data.stadium_list[i]
       let newDis = parseInt(this.calDistance(la, lo, info.la, info.lo)*1000)
       let updateItem = 'stadium_list[' + i + '].dis'
       this.setData({[updateItem]: newDis})
     }
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

   jmpInfo:function(e) {
    wx.navigateTo({
      url: '/pages/stadium/info/stadium?'+'id='+e.currentTarget.dataset.stadiumid,
    })
  },

  /*-------------------------------
    网络请求函数
  -------------------------------*/
  reqStadiumList:function() {
    const _this = this
    const app = getApp()
    wx.request({
      method: "GET",
      url: 'https://cbx.iterator-traits.com/api/user/stadium/',
      data: {},
      header: {
        'content-type': 'application/json',
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        if((res.statusCode === 200) && (res.data.error === undefined || res.data.error === null)) {
          _this.setStadiumInfo(res)
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