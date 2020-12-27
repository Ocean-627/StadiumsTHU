Page({
  data: {
    // 地图相关
    scale: 16,
    latitude: "",
    longitude: "",
    markers: [],
    // 显示切换
    showmap:true,
    // 地点
    stadium:[],
    // 用户位置
    user_la:"",
    user_lo:"",
    // 图片资源
    search_img:getApp().globalData.imgUrl+'/res/imgs/map_search.png',
    mypos_img:getApp().globalData.imgUrl+'/res/imgs/map_mypos.png',
  },
  
  onLoad: function (options) {
    var _this = this;
    // 获取用户位置 
    wx.getLocation({
      type: 'gcj02',
      success: function (res) {
        _this.setData({
          latitude: res.latitude,
          longitude: res.longitude,
          user_la:res.latitude,
          user_lo:res.longitude,
        })
      }
    })
    // 设置搜索栏函数
    this.setData({
      search: this.search.bind(this)
    })
  },

  onShow:function() {
    this.reqStadiumInfo()
  },

  // 回到自己的定位点
  back_to_mypos:function() {
    var _this = this
    wx.getLocation({
      type: 'gcj02',
      success: function (res) {
        _this.setData({
          latitude: res.latitude,
          longitude: res.longitude,
          user_la:res.latitude,
          user_lo:res.longitude,
          scale:16
        })
      }
    })
  },

  search: function (value) {
    if(value === '') {
      return
    }
    var resultArr = []
    for(var i=0; i<this.data.stadium.length; i++) {
      var info = this.data.stadium[i]
      if(info.name.indexOf(value) !== -1 || info.pinyin.indexOf(value) !== -1) {
        resultArr.push({
          text:info.name,
          value:i,
        })
      }
    }
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve(resultArr)
        }, 200)
    })
  },

  selectResult: function (e) {
    var place = e.detail.item.value
    if(place >= 0) {
      this.show_marker(this.data.stadium[place])
    }
  },

  show_marker:function(info) {
    const _this = this
    try{
      wx.serviceMarket.invokeService({
        service: 'wxc1c68623b7bdea7b',
        api: 'directionWalking',
        data:{
          "from":_this.data.user_la+','+_this.data.user_lo,
          "to":info.latitude+','+info.longitude,
        }
      }).then(ret => {
        console.log(ret)
        if(ret.data.status !== 0) {
          wx.showToast({
            title: '查询路线失败',
            icon:'none',
            duration:1000,
          })
        } else {
          var coors = ret.data.result.routes[0].polyline;
          //坐标解压（返回的点串坐标，通过前向差分进行压缩）
          for (var i = 2; i < coors.length; i++) {
            coors[i] = Number(coors[i - 2]) + Number(coors[i]) / 1000000;
          }
          //解压后，用小程序map组件的polyline，绘制到图上上
          var pl=[];  
          for (var i = 0; i < coors.length; i += 2) {
            //以polyline的points对象规范创建
            pl.push({ latitude: coors[i], longitude: coors[i + 1] })
          }
          //设置polyline属性，将路线显示出来（关于地图容器的使用可另行参见小程序组件的开发文档）
          _this.setData({
            polyline: [{
                points: pl,
                color: '#07c160',
                width: 4
            }]
          })
        }
      })
    } catch(e) {
      wx.showToast({
        title: '无法获取地图导航服务，请检查您的小程序版本是否过低',
        icon:'none',
        duration:2000,
      })
    }

    this.setData({
      latitude: info.latitude,
      longitude: info.longitude,
      scale:16,
      markers:[{
        id: 1,
        latitude: info.latitude,
        longitude: info.longitude,
        iconPath: getApp().globalData.imgUrl+'/res/imgs/map_dest.png',
        width:20,
        height:20
      }]
    })
  },

  show_search:function() {
    this.setData({showmap:false})
  },

  show_map:function() {
    this.setData({showmap:true})
  },

  // 设置场馆位置信息
  setStadiumPosInfo:function(res) {
    var posArr = []
    for(var info of res.data) {
      var newLaLo = this.bdMap_to_txMap(info.latitude, info.longitude)
      posArr.push({
        id:info.id,
        name:info.name,
        pinyin:(info.pinyin === null?info.name:info.pinyin),
        latitude:newLaLo.latitude,
        longitude:newLaLo.longitude
      })
    }
    this.setData({
      stadium:posArr,
    })
    //设置搜索结果
    var seek = getApp().globalData.seekStadiumId
    if(seek > 0) {
      for(var info of posArr) {
        if(info.id === parseInt(seek)) {
          this.show_marker(info)
        }
      }
      getApp().globalData.seekStadiumId = 0
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
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        if((res.statusCode === 200) && (res.data.error === undefined || res.data.error === null)) {
          _this.setStadiumPosInfo(res)
        } else {
          app.reqFail("获取信息失败")
        }
      },
      fail() {
        app.reqFail("获取信息失败")
      },
      complete() {
        wx.stopPullDownRefresh({
          success: (res) => {},
        })
      },
    })
  },
})