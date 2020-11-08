// pages/stadium/stadium.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    // 滚动图片test
    gallery_imgs: [
      '/res/test/stadium_1.jpg',
      '/res/test/stadium_2.jpg',
      '/res/test/stadium_3.jpeg'
    ],
    
    // 评论列表
    comment_list: [{
      headerPath:'/res/imgs/header_test.jpg',
      name:'hhy',
      date:'2020年11月11日 15:00',
      score:4,
      content:'很好的场馆，下次还来',
      imgs:[
        '/res/test/stadium_1.jpg',
        '/res/test/stadium_2.jpg',
        '/res/test/stadium_1.jpg',
        '/res/test/stadium_2.jpg',
        '/res/test/stadium_1.jpg'
      ]
    },{
      headerPath:'/res/imgs/header_test.jpg',
      name:'hhy',
      date:'2020年11月11日 15:00',
      score:4,
      content:'很好的场馆，下次还来',
      imgs:[
        '/res/test/stadium_1.jpg',
        '/res/test/stadium_2.jpg',
        '/res/test/stadium_1.jpg',
        '/res/test/stadium_2.jpg',
        '/res/test/stadium_1.jpg'
      ]
    }]
  },

})