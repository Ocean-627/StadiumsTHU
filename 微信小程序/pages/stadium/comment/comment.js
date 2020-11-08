// pages/stadium/comment/comment.js
Page({
  data: {
    // 上传图片文件
    files: [],
    // 打分
    star_list:[1,1,1,1,1],
    score:5,
    // 场馆信息
    stadium_img:'/res/test/stadium_1.jpg',
    stadium_name:'综合体育馆',
    court_name:'羽毛球馆1号场地'
  },

  onLoad() {
    this.setData({
      selectFile: this.selectFile.bind(this),
      uplaodFile: this.uplaodFile.bind(this)
    })
  },

  // 图片选择函数
  chooseImage: function (e) {
    var that = this;
    wx.chooseImage({
      sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
      success: function (res) {
        // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片
        that.setData({
            files: that.data.files.concat(res.tempFilePaths)
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
      console.log('files', files)
      // 返回false可以阻止某次文件上传
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
    console.log('upload error', e.detail)
  },

  uploadSuccess(e) {
    console.log('upload success', e.detail)
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
  }
});