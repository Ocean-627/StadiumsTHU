// pages/message/message.js
Page({
  data: {
    not_read_num:3,
    // 消息列表
    msg_list: [{
      icon_path:'/res/imgs/msg_index.png',
      discription:'预约成功',
      date:'2020年10月20日 12:22',
      content:'您已成功预约综合体育馆羽毛球馆2号场地，预约时间为10月23日(周六)15:30-16:30。',
    },{
      icon_path:'/res/imgs/msg_notice.png',
      discription:'预约变更提醒',
      date:'2020年10月20日 12:22',
      content:'您预约的综合体育馆羽毛球馆2号场地(10月22日(周五)15:30-16:30)，因xxxxx而被取消。',
    },{
      icon_path:'/res/imgs/msg_alert.png',
      discription:'预约时间即将开始',
      date:'2020年10月20日 12:22',
      content:'您预约的西体育馆乒乓球馆213室(10月10日(周三)15:30-16:30)即将开始，请按时履约。',
    },{
      icon_path:'/res/imgs/msg_alert.png',
      discription:'使用时间即将结束',
      date:'2020年10月20日 12:22',
      content:'您正在使用的西体育馆乒乓球馆213室(10月10日(周三)15:30-16:30)即将到达结束时间，请按时扫码结束使用。',
    }
  ],
  // 消息是否已读
  msg_read:[1,1,1,0]
  },

  mark_all:function() {
    var arr = new Array(this.data.msg_list.length).fill(0)
    this.setData({msg_read:arr})
  },
})