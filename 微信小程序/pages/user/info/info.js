// pages/user/info/info.js
Page({
  data: {
    // 用户信息
    pic_path:"/res/imgs/header_test.jpg",  // 头像
    usr_nickname:"一个大萝卜",
    usr_name:"",
    usr_id:"",
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
    buttons: [{text: '确定'}],
    // 顶部提示信息
    tip:"",
    tip_type:"",
    tip_show:false,
    // 前后端变量映射(后端->前端)
    varReflectTable:{
      email:"usr_mail",
      phone:"usr_phone",
      userId:"user_id",
      nickName:"usr_nickname",
      name:"usr_name",
    },
  },

  onLoad:function(options) {
    this.reqUserInfo()
  },

  onPullDownRefresh:function() {
    this.reqUserInfo()
  },

  //
  reqUserInfo:function() {
    var _this = this;
    wx.request({
      method: "GET",
      url: 'https://cbx.iterator-traits.com/api/user/user/',
      data: {},
      header: {
        'content-type': 'application/json',
        'loginToken': 1,
      },
      success(res) {
        console.log('Get Info success!')
        _this.setUserData(res)
      },
      fail() {
        console.log('Get Info fail!')
      },
      complete() {
        wx.stopPullDownRefresh({
          success: (res) => {},
        })
      }
    })
  },

  // 设置用户信息
  setUserData:function(res) {
    this.setData({
      usr_id:res.data.userId,
      usr_name:res.data.name,
      usr_phone:res.data.phone,
      usr_mail:res.data.email,
      usr_nickname:res.data.nickName,
    })
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
    this.setData({tmpInput:this.data.usr_nickname})
  },

  showPhDialog:function() {
    this.setData({dia_mPhone:true})
    this.setData({input_phone:this.data.usr_phone})
    this.setData({tmpInput:this.data.usr_phone})
  },

  showMailDialog:function() {
    this.setData({dia_mMail:true})
    this.setData({input_mail:this.data.usr_mail})
    this.setData({tmpInput:this.data.usr_mail})
  },

  // 修改信息
  modifyNickname:function() {
    this.postModifyMsg('nickName',this.data.tmpInput)
    this.setData({dia_mNickname:false})
  },

  modifyPhone:function() {
    this.postModifyMsg('phone',this.data.tmpInput)
    this.setData({dia_mPhone:false})
  },

  modifyMail:function() {
    this.postModifyMsg('email',this.data.tmpInput)
    this.setData({dia_mMail:false})
  },

  // 修改输入内容
  mInput:function(e) {
    this.setData({tmpInput:e.detail.value})
  },

  // 发送修改req
  postModifyMsg:function(key, value) {
    var _this = this
    wx.request({
      method: "POST",
      url: 'https://cbx.iterator-traits.com/api/user/user/',
      data: {
        [key]:value,
      },
      header: {
        'content-type': 'application/json',
        'loginToken': 1,
      },
      success(res) {
        console.log('Modify User Info success!')
        var varName = _this.data.varReflectTable[key]
        _this.setData({[varName]:value})
        _this.modifySuccess()
      },
      fail() {
        console.log('Modify User Info fail!')
        _this.modifyFail()
      }
    })
  },

  // 修改成功/失败时顶部弹窗消息
  modifyFail:function() {
    this.setData({
      tip:"修改信息失败",
      tip_show:true,
      tip_type:"error",
      navi_show:false,
    })
  },

  modifySuccess:function() {
    this.setData({
      tip:"修改信息成功",
      tip_show:true,
      tip_type:"success",
      navi_show:false,
    })
  },
})