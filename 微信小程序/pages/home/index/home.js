Page({
  data: {
    // 滚动图片
    gallery_imgs: [
      '/res/imgs/camera.png',
      '/res/imgs/header_test.jpg',
      '/res/imgs/home_search.png'
    ],
    // 是否筛选
    sort_dis:'nosort',
    sort_score:'nosort',
    sort_pop:'nosort',
    // 场馆信息
    stadium_list:[
      {
        name:'综合体育馆',
        star:5,
        comment_num:1911,
        opentime:'8:00-19:00',
        sports:'羽毛球，乒乓球',
        pos:'新民路',
        dis:890,
        favor:true,
        imgpath:'/res/imgs/header_test.jpg'
      }
    ]
  },

  // 排序键按下
  sortdis:function() {
    if(this.data.sort_dis==='nosort') {
      this.setData({sort_dis:'sort', sort_score:'nosort', sort_pop:'nosort'})
    } else {
      this.setData({sort_dis:'nosort'})
    }
  },

  sortscore:function() {
    if(this.data.sort_score==='nosort') {
      this.setData({sort_dis:'nosort', sort_score:'sort', sort_pop:'nosort'})
    } else {
      this.setData({sort_score:'nosort'})
    }
  },

  sortpop:function() {
    if(this.data.sort_pop==='nosort') {
      this.setData({sort_dis:'nosort', sort_score:'nosort', sort_pop:'sort'})
    } else {
      this.setData({sort_pop:'nosort'})
    }
  },

  // 跳转到详细信息
  jmpInfo:function(e) {
    console.log(e.currentTarget.dataset.stadiumid)
    wx.navigateTo({
      url: '/pages/stadium/info/stadium',
    })
  }
})