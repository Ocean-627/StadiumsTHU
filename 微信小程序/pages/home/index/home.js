Page({
  data: {
    // 滚动图片
    gallery_imgs: [
      getApp().globalData.imgUrl+'/res/test/stadium_1.jpg',
      getApp().globalData.imgUrl+'/res/test/stadium_2.jpg',
      getApp().globalData.imgUrl+'/res/test/stadium_3.jpeg'
    ],
    // 筛选
    active_sports:0,
    filter:"all",
    sort_key:"id",
    filter_opt:[
      {text:'所有场馆', value:'all'},
      {text:'我收藏的',value:'collect'},
      {text:'当前开放的',value:'open'},
    ],
    sort_opt:[
      {text:'默认排序', value:'id'},
      {text:'距我最近',value:'dis'},
      {text:'评分最高',value:'star'},
      {text:'人气最高',value:'comment_num'}
    ],
    // 场馆信息
    stadium_list:[],
    filter_list:[],
    // 运动项目
    sports_list:[
      '全部',
      '羽毛球',
      '乒乓球',
      '篮球',
      '足球'
    ],
    // 图片资源
    scan_img:getApp().globalData.imgUrl+'/res/imgs/home_scan.png',
    star_img:getApp().globalData.imgUrl+'/res/imgs/info_star.png',
  },

  // 变更筛选条件
  onSportsChange:function(e) {
    this.setData({
      active_sports:e.detail
    })
    this.filterStadium()
  },

  onFilterChange:function(e) {
    this.setData({
      filter:e.detail
    })
    this.filterStadium()
  },

  onSortChange:function(e) {
    this.setData({
      sort_key:e.detail
    })
    this.filterStadium()
  },

  // 设置场馆信息
  setStadiumInfo:function(res) {
    var newList = []
    for(var info of res.data) {
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
        pinyin:info.pinyin,
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
      })
    }
    this.data.stadium_list = newList
    this.setData({
      filter_list:this.data.stadium_list,
      active_sports:0,
      filter:"all",
      sort_key:"id",
    })
    this.filterStadium()
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
    wx.onLocationChange((result) => {_this.updateDis(result.latitude, result.longitude)})
    this.setData({stadiumSearch: this.stadiumSearch.bind(this)})
  },

  // 下拉刷新页面
  onPullDownRefresh:function() {
    this.reqStadiumInfo()
  },

  // 场馆筛选函数
  filterStadium:function(e) {
    var showList = []
    var sport_seg = ''
    var filter_seg = 'id'
    var sort_key = 'id'
    if(this.data.active_sports !== 0) {
      sport_seg = this.data.sports_list[this.data.active_sports]
    }
    if(this.data.filter !== 'all') {
      filter_seg = this.data.filter
    }
    sort_key = this.data.sort_key
    for(var stadium of this.data.stadium_list) {
      if( (stadium.sports.indexOf(sport_seg) >= 0) && (stadium[filter_seg])) {
        showList.push(stadium)
      }
    }
    this.setData({filter_list:showList})
    if(sort_key === 'id' || sort_key === 'dis') {
      this.sortStadium(sort_key, false)
    } else {
      this.sortStadium(sort_key, true)
    }
  },

  // 排序函数
  sortStadium(key, desc) {
    let oldList = this.data.filter_list
    oldList.sort(function(a,b) {
    　return desc ? ((parseInt(a[key]) < parseInt(b[key]))?1:((parseInt(a[key]) > parseInt(b[key]))?-1:0)):((parseInt(a[key]) < parseInt(b[key]))?-1:((parseInt(a[key]) > parseInt(b[key]))?1:0))  //杠杠的，注意括号就是！
    })
    this.setData({filter_list:oldList})
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

   // 场馆搜索函数，每隔一段时间会调用
   stadiumSearch:function(value) {
      var resultArr = []
      console.log(value)
      if(value !== '') {
        for(var info of this.data.stadium_list) {
          if(info.name.indexOf(value) !== -1 || info.pinyin.indexOf(value) !== -1) {
            resultArr.push({
              text:info.name,
              value:{
                id:info.id,
                content:'',
              }
            })
          }
        }
      }
      var resultNum = resultArr.length
      if(resultNum > 4) {
        resultArr = resultArr.slice(0,5)
        resultArr[4] = {
          text:'查看全部的' + resultNum + '条结果',
          value:{
            id:-1,
            content:value,
          }
        }
      }
      return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve(resultArr)
        }, 200)
      })
   },

   // 选择搜索结果
   selectResult:function(e) {
     if(e.detail.item.value.id > 0) {
      wx.navigateTo({
        url: '/pages/stadium/info/stadium?'+'id='+e.detail.item.value.id
      })
     }
     else {
      wx.navigateTo({
        url: '/pages/home/result/result?'+'search='+e.detail.item.value.content
      })
     }
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
        if((res.statusCode === 200) && (res.data.error === undefined || res.data.error === null)) {
          app.reqSuccess("获取信息成功")
          _this.setStadiumInfo(res)
        } else {
          app.reqFail("操作失败")
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

/*--------------------------------------------------
   页面跳转函数
---------------------------------------------------*/
  jmpInfo:function(e) {
    // 设置历史记录
    const app = getApp()
    var oldHis = JSON.parse(wx.getStorageSync('visitHistory'))
    oldHis.push({
      type:'浏览',
      target:{
        name:e.currentTarget.dataset.name,
        id:e.currentTarget.dataset.stadiumid,
      },
      time:app.getCurrentTime()
    })
    oldHis = oldHis.slice(-app.globalData.maxRecordNum)
    wx.setStorageSync('visitHistory', JSON.stringify(oldHis))

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