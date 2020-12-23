// pages/stadium/allcomment/allcomment.js
Page({
  data: {
    // 场馆id
    stadium_id:Number,
    // 评论列表
    comment_list: [],
    // 当前分页
    curPage:1,
    // 到达底部
    toBottom:false,
    // 图片资源
    comment_img:getApp().globalData.imgUrl+'/res/imgs/stadium_comment.png',
    star_img:getApp().globalData.imgUrl+'/res/imgs/info_star.png',
  },

  onLoad:function(options) {
    this.setData({stadium_id:options.id})
    this.reqCommentInfo(1)
  },

  // 页面下拉分页
  onReachBottom:function() {
    if(this.data.toBottom) {
      return
    }
    const newPage = this.data.curPage+1
    this.setData({curPage:newPage})
    this.reqCommentInfo(this.data.curStat,true)
  },

  // 设置评论信息
  setCommentInfo:function(res, add=false) {
    var newList = []
    if(add) {
      newList = this.data.comment_list
    }
    for(var info of res.data.results) {
      var imgList = []
      for(var img of info.images) {
        imgList.push(img.image)
      }
      newList.push({
        headerPath:info.userImage,
        name:info.userName,
        date:info.createTime,
        score:info.score,
        content:info.content,
        imgs:imgList
      })
    }

    this.setData({comment_list:newList})
  },

  /*--------------------------------------------------
    网络请求函数
  ---------------------------------------------------*/
  // 请求评论信息
  reqCommentInfo:function(page, add=false) {
    const _this = this
    const app = getApp()
    wx.request({
      method: "GET",
      url: app.globalData.reqUrl + '/api/user/comment/',
      data: {
        'stadium_id':_this.data.stadium_id,
        'page':page,
      },
      header: {
        'content-type': 'application/json',
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          _this.setCommentInfo(res, add)
        } 
        else if(res.data.error.detail === 'Invalid page.') {
          _this.setData({ toBottom:true })
        }
        else {
          app.reqFail("获取信息失败")
        }
      },
      fail() {
        app.reqFail("获取评论信息失败")
      },
    })
  },
})