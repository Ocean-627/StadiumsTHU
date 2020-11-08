// pages/user/info/info.js
Page({
  data: {
    // 用户信息
    pic_path:"/res/imgs/header_test.jpg",  // 头像
    usr_nickname:"一个大萝卜",
    usr_name:"",
    usr_id:Number,
    usr_phone:"123456789",
    usr_mail:"12345@126.com",
    // 弹窗
    dia_mNickname:false,  // 是否显示弹窗
    dia_mPhone:false,
    dia_mMail:false,
    input_nickname:"",    // 弹窗输入框内容
    input_phone:"",
    input_mail:"",
    tmpInput:"",
    buttons: [{text: '确定'}]
  },
  
  // 选择头像
  choosePic:function() {
    var _this = this
    wx.chooseImage({
      count: 1,
      sizeType: ['original', 'compressed'],
      sourceType: ['album', 'camera'],
      success (res) {
        _this.setData({pic_path: res.tempFilePaths[0]})
      }
    })
  },

  //弹出修改框
  showNicDialog:function() {
    this.setData({dia_mNickname:true})
    this.setData({input_nickname:this.data.usr_nickname})
  },

  showPhDialog:function() {
    this.setData({dia_mPhone:true})
    this.setData({input_phone:this.data.usr_phone})
  },

  showMailDialog:function() {
    this.setData({dia_mMail:true})
    this.setData({input_mail:this.data.usr_mail})
  },

  // 修改信息
  modifyNickname:function() {
    this.setData({usr_nickname:this.data.tmpInput})
    this.setData({dia_mNickname:false})
  },

  modifyPhone:function() {
    this.setData({usr_phone:this.data.tmpInput})
    this.setData({dia_mPhone:false})
  },

  modifyMail:function() {
    this.setData({usr_mail:this.data.tmpInput})
    this.setData({dia_mMail:false})
  },

  // 修改输入内容
  mInput:function(e) {
    this.setData({tmpInput:e.detail.value})
  }
})