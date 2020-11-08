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
    stadium:[
      {
        name:"综合体育馆",
        longitude:116.33237779,
        latitude:40.0044594
      }
    ],
  },
  
  onLoad: function () {
    var _this = this;
    // 获取用户位置 
    wx.getLocation({
      type: 'gcj02',
      success: function (res) {
        _this.setData({
          latitude: res.latitude,
          longitude: res.longitude,
        })
      }
    })
    // 设置搜索栏函数
    this.setData({
      search: this.search.bind(this)
    })
  },

  back_to_mypos:function() {
    var _this = this;
    wx.getLocation({
      type: 'gcj02',
      success: function (res) {
        _this.setData({
          latitude: res.latitude,
          longitude: res.longitude,
          scale:16
        })
      }
    })
  },

  search: function (value) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve([{text: '综合体育馆', value: 0}])
        }, 200)
    })
  },

  selectResult: function (e) {
    console.log('select result', e.detail.item.value)
    var place = e.detail.item.value
    if(place >= 0) {
      this.setData({
        latitude: this.data.stadium[place].latitude,
        longitude: this.data.stadium[place].longitude,
        scale:16,
        markers:[{
          id: 1,
          latitude: this.data.stadium[place].latitude,
          longitude: this.data.stadium[place].longitude,
          iconPath: '/res/imgs/map_dest.png',
          width:20,
          height:20
        }]
      })
    }
  },

  show_search:function() {
    this.setData({showmap:false})
  },

  show_map:function() {
    this.setData({showmap:true})
  }
})