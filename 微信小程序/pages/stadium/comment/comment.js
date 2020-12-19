// pages/stadium/comment/comment.js
Page({
  data: {
    // 预约订单id
    bookId:Number,
    // 上传图片文件
    files: [],
    // 打分
    star_list:[1,1,1,1,1],
    score:5,
    // 评价文字
    comment_text:'',
    // 字数限制
    minTextNum:5,
    maxTextNum:300,
    // 场馆信息
    stadium_img:'/res/test/stadium_1.jpg',
    stadium_name:'综合体育馆',
    court_name:'羽毛球馆1号场地',
    // 图片资源
    isfavor_img:getApp().globalData.imgUrl+'/res/imgs/info_isfavor.png',
    notfavor_img:getApp().globalData.imgUrl+'/res/imgs/info_notfavor.png',
    comment_placeholder:"说点什么。。"
  },

  onLoad(options) {
    const holder = this.data.comment_placeholder+'('+this.data.minTextNum+'-'+this.data.maxTextNum+'字)'
    this.setData({
      bookId:options.id,
      selectFile: this.selectFile.bind(this),
      uplaodFile: this.uplaodFile.bind(this),
      comment_placeholder: holder
    })
    this.reqBookInfo()
  },

  // 图片选择函数
  chooseImage: function (e) {
    var _this = this
    wx.chooseImage({
      sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
      success: function (res) {
        // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片
        _this.setData({
            files: _this.data.files.concat(res.tempFilePaths)
        });
      }
    })
  },

  previewImage: function(e){
    wx.previewImage({
      current: e.currentTarget.id, // 当前显示图片的http链接
      urls: this.data.files // 需要预览的图片http链接列表
    })
  },

  selectFile(files) {
    
  },

  uplaodFile(files) {
    console.log('upload files', files)
    // 文件上传的函数，返回一个promise
    var _this = this
    return new Promise((resolve, reject) => {
      const tempFilePaths = files.tempFilePaths;
      _this.setData(
        {
          filesUrl: tempFilePaths
        }
      )
      var object = {};
      object['urls'] = tempFilePaths;
      resolve(object);
    })
  },

  uploadError(e) {
    wx.showToast({
      title: '图片导入失败',
      icon:'none',
      duration:1000,
    })
  },

  uploadSuccess(e) {
    
  },

  // 上传所有图片
  uploadAllImage() {
    console.log(this.data.filesUrl)
  },

  // 获取评论内容
  onModifyComment:function(e) {
    this.setData({
      comment_text:e.detail.value
    })
  },

  // 点击发表按钮
  makeComment() {
    console.log(this.data.bookId)
    console.log(this.data.comment_text)
    this.reqPostComment()
  },

  // 修改评分
  change_score:function(e) {
    var new_score = e.currentTarget.dataset.index
    var new_stars = [0,0,0,0,0]
    for(var i=0; i<=new_score; i=i+1) {
      new_stars[i] = 1;
    }
    this.setData({
      score: new_score + 1,
      star_list: new_stars
    })
  },

  // 设置场馆信息
  setBookInfo:function(res) {
    const info = res.data.results[0]
    this.setData({
      stadium_img:info.image,
      stadium_name:info.stadium,
      court_name:info.court
    })
  },

  /*----------------------------------
    网络请求函数
  -----------------------------------*/
  reqBookInfo:function() {
    const _this = this
    const app = getApp()
    wx.request({
      method: "GET",
      url: app.globalData.reqUrl + '/api/user/reserve/',
      data:{
        id:_this.data.bookId
      },
      header: {
        'content-type': 'application/json',
        'loginToken': 1,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          // 上传文字成功后上传图片
          _this.reqUploadCommentImg(res.data.id)
        } else {
          app.reqFail("获取信息失败")
        }
      },
      fail() {
        app.reqFail("获取信息失败")
      },
    })
  },

  // 场馆评价
  reqPostComment:function() {
    const _this = this
    const app = getApp()
    wx.request({
      method: "POST",
      url: app.globalData.reqUrl + '/api/user/comment/',
      data:{
        reserve_id:_this.data.bookId,
        content:_this.data.comment_text,
      },
      header: {
        'content-type': 'application/json',
        'loginToken': 1,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          app.reqSuccess("发表成功")
        } else {
          app.reqFail("发表失败")
        }
      },
      fail() {
        app.reqFail("发表失败")
      },
    })
  },

  // 上传评价图片
  reqUploadCommentImg:function(commentId) {
    const _this = this
    const app = getApp()
    if(this.data.filesUrl === undefined) {
      return
    }
    for(var imgPath of this.data.filesUrl) {
      wx.uploadFile({
        filePath: imgPath,
        name: 'image',
        url: app.globalData.reqUrl + '/api/user/commentimage/',
        formData: {
          comment_id:commentId,
        },
        header: {
          'loginToken': 1,
          'content-type': 'multipart/form-data',
        },
        success(res) {
          if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          } else {
            app.reqFail("发表失败")
          }
        },
        fail() {
          app.reqFail("发表失败")
        },
      })
    }
  }
});