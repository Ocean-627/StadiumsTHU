Page({
  data: {
    // 预定信息
    booking_list:[
      {
        stadium_name:'综合体育馆',
        court_name:'羽毛球馆2号场地',
        book_time:'10月20日下午2:00-3:30',
        price:'30.00',
        status:'已付款',
        imgpath:'/res/test/stadium_1.jpg'
      }
    ]
  },

  // 跳转到详细信息
  jmpInfo:function(e) {
    console.log(e.currentTarget.dataset.stadiumid)
    wx.navigateTo({
      url: '/pages/stadium/info/stadium',
    })
  }
})