// pages/stadium/comment/comment.js
import Dialog from '../../../miniprogram/miniprogram_npm/@vant/weapp/dialog/dialog';
Page({
  data: {
    // 预约订单id
    bookId:Number,
    // 评论/查看评论
    view:true,
    // 上传图片文件
    files: [],
    // 查看评论时的图片列表
    imgList:[],
    // 查看评论时的评论id
    commentId:Number,
    // 打分
    star_list:[1,1,1,1,1],
    score:5,
    // 评价文字
    comment_text:'',
    // 字数限制
    minTextNum:5,
    maxTextNum:300,
    // 错误输入提示
    wrong_input:true,
    input_tip:'评论的内容有点少哦，再说点什么吧。',
    // 正在发送评论
    post_comment:false,
    // 场馆信息
    stadium_img:'',
    stadium_name:'',
    court_name:'',
    // 图片资源
    isfavor_img:getApp().globalData.imgUrl+'/res/imgs/info_isfavor.png',
    notfavor_img:getApp().globalData.imgUrl+'/res/imgs/info_notfavor.png',
    comment_placeholder:"说点什么。。"
  },

  onLoad(options) {
    const holder = this.data.comment_placeholder+'('+this.data.minTextNum+'-'+this.data.maxTextNum+'字)'
    const isView = options.type === 'view'
    this.setData({
      bookId:options.id,
      selectFile: this.selectFile.bind(this),
      uplaodFile: this.uplaodFile.bind(this),
      comment_placeholder: holder,
      view:isView,
    })
    this.reqBookInfo(isView)
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
    if(e.detail.value.length < this.data.minTextNum) {
      this.setData({
        wrong_input:true,
        input_tip:'评论的内容有点少哦，再说点什么吧。'
      })
    }
    else {
      this.setData({
        wrong_input:false,
      })
    }
  },

  // 点击发表按钮
  makeComment() {
    this.setData({
      post_comment:true
    })
    this.reqPostComment()
  },

  // 撤销评论
  deleteComment(e) {
    const _this = this
     // 弹出提示
     Dialog.confirm({
      title:'温馨提示',
      message:'撤销评论操作无法恢复，是否确认继续？',
    })
    .then(()=>{
      // 确认
      _this.reqDeleteComment()
    })
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
  setBookInfo:function(res, isView=false) {
    const info = res.data.results[0]
    this.setData({
      stadium_img:info.image,
      stadium_name:info.stadium,
      court_name:info.court
    })
    if(isView && info.comments.length > 0) {
      const commentInfo = info.comments[0]
      // 设置图片
      var imgList = []
      for(var img of commentInfo.images) {
        imgList.push(img.image)
      }
      console.log(imgList)
      // 设置评分
      var scoreList = []
      for(var i=0; i<5; i++) {
        if(i<commentInfo.score) {
          scoreList.push(1)
        } else {
          scoreList.push(0)
        }
      }
      this.setData({
        imgList:imgList,
        commentId:commentInfo.id,
        comment_text:commentInfo.content,
        star_list:scoreList
      })
    }
  },

  /*----------------------------------
    网络请求函数
  -----------------------------------*/
  // 获取预约信息
  reqBookInfo:function(isView=false) {
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
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          _this.setBookInfo(res, isView)
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
        score:_this.data.score,
      },
      header: {
        'content-type': 'application/json',
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          // 上传文字成功后上传图片
          _this.reqUploadCommentImg(res.data.id)
        } else {
          app.reqFail("发表失败")
          _this.setData({post_comment:false})
        }
      },
      fail() {
        app.reqFail("发表失败")
        _this.setData({post_comment:false})
      },
    })
  },

  // 上传评价图片
  reqUploadCommentImg:function(commentId) {
    const _this = this
    const app = getApp()
    // 图片列表为空，直接返回
    if(this.data.filesUrl === undefined) {
      app.reqSuccess("发表成功")
      setTimeout(()=>{
        wx.navigateBack({
          delta: 0,
        })
      },1000)
      return
    }

    var promiseArr = []
    for(var imgPath of this.data.filesUrl) {
      let promise = new Promise((resolve, reject) => {
        wx.uploadFile({
          filePath: imgPath,
          name: 'image',
          url: app.globalData.reqUrl + '/api/user/commentimage/',
          formData: {
            comment_id:commentId,
          },
          header: {
            'loginToken': app.globalData.loginToken,
            'content-type': 'multipart/form-data',
          },
          success(res) {
            if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
              resolve(res)
            } 
            else {
              reject()
            }
          },
          fail() {
            reject()
          },
        })
        promiseArr.push(promise)
      })
    }
    // 一次性发出所有图片上传请求
    Promise.all(promiseArr).then((result)=>{
      app.reqSuccess("发表成功")
      setTimeout(()=>{
        wx.navigateBack({
          delta: 0,
        })
      },1000)
    }).catch((error)=>{
      app.reqFail("上传失败")
      _this.setData({post_comment:false})
    })
  },

  // 撤销评论
  reqDeleteComment:function() {
    const _this = this
    const app = getApp()
    wx.request({
      method: "DELETE",
      url: app.globalData.reqUrl + '/api/user/comment/',
      data:{
        comment_id:_this.data.commentId
      },
      header: {
        'content-type': 'application/json',
        'loginToken': app.globalData.loginToken,
      },
      success(res) {
        if((res.statusCode.toString().startsWith("2")) && (res.data.error === undefined || res.data.error === null)) {
          app.reqSuccess("撤销成功")
          setTimeout(()=>{
          wx.navigateBack({
            delta: 0,
          })
      },1000)
        } else {
          app.reqFail("撤销失败")
        }
      },
      fail() {
        app.reqFail("撤销失败")
      },
    })
  },
});