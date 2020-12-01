Page({
  data:{
    stadium_list:[],
    filtered_list:[],
  },

  // 设置场馆信息
  setStadiumInfo:function(res, updatePos=true) {
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

    var newList = []
    for(var info of res.data) {
      var sports = ''
      var dis = 0
      for(var sport of info.courtType) {
        sports = sports + sport + ' '
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
        favor:true,
        imgpath:'/res/test/stadium_2.jpg',
      });
    }
    this.setData({stadium_list:newList})
  },

  // 创建时请求信息
  onShow: function (options) {
    var _this = this;
    wx.request({
      method: "GET",
      url: 'https://cbx.iterator-traits.com/api/user/stadium/',
      data: {},
      header: {
        'content-type': 'application/json',
        'loginToken': 1,
      },
      success(res) {
        console.log('Get Info success!')
        _this.setStadiumInfo(res)
      },
      fail() {
        console.log('Get Info fail!')
      }
    })
  },

  // 搜索函数
  startSearch:function(e) {
    var value = e.detail.value
    var resultArr = []
    if(value !== '') {
      for(var info of this.data.stadium_list) {
        if(info.name.indexOf(value) !== -1 || info.sports.indexOf(value) !== -1) {
          resultArr.push(info)
        }
      }
      this.setData({filtered_list:resultArr})
    }
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
       let newDis = parseInt(this.calDistance(la, lo, info.la, info.lo))
       let updateItem = 'stadium_list[' + i + '].dis'
       this.setData({[updateItem]: newDis})
     }
   }
})