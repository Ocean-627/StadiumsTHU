Page({
  data: {
    // 预定信息
    booking_list:[
      {
        stadium_name:'综合体育馆',
        court_name:'羽毛球馆2号场地',
        book_time:'10月20日下午2:00-3:30',
        price:'30.00',
        status:'待评价',
        hasReview:false,
        imgpath:'/res/test/stadium_1.jpg'
      }
    ]
  },

  jmpReview:function() {
    wx.navigateTo({
      url: '/pages/stadium/comment/comment',
    })
  },
})