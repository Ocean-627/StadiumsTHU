// pages/stadium/book.js
Page({
  data: {
    // 步骤
    steps: [
      {
        text: '步骤一',
        desc: '选择场地',
      },
      {
        text: '步骤二',
        desc: '确认预定',
      },
      {
        text: '步骤三',
        desc: '付款',
      },
    ],

    //场地 
    activeName: '1',

    stadium_id:Number,
    stadium_name:'综合体育馆',
    court_iconlist: [
      '/res/sports/tabletennis.png',
      '/res/sports/gym.png',
      '/res/sports/billiard.png',
      '/res/sports/archery.png',
      '/res/sports/badminton.png',
      '/res/sports/tabletennis.png',
      '/res/sports/gym.png',
      '/res/sports/billiard.png',
      '/res/sports/archery.png',
      '/res/sports/badminton.png',
    ],
    court_time_disable:[
      false, false, true, false
    ],

    court_time_choose:[
      true, true, false, false
    ],
    
    // 运动->图标映射
    sportsIconTable:{
      '乒乓球':'/res/sports/tabletennis.png',
      '体操':'/res/sports/gym.png',
      '台球':'/res/sports/billiard.png',
      '射箭':'/res/sports/archery.png',
      '羽毛球':'/res/sports/badminton.png',
      '篮球':'/res/sports/basketball.png',
      '足球':'/res/sports/football.png',
      '游泳':'/res/sports/swim.png',
      '排球':'/res/sports/volleyball.png',
      '保龄球':'/res/sports/bowling.png',
    }
  },

  onLoad:function(options) {
    this.setData({stadium_id:options.id})
    this.reqCourtInfo()
    var arr = new Array(this.data.stamps_num).fill(0);
    for(var i=0; i<this.data.court_num;i++) {
      this.setData({
        ['court_time[' + i +'].status_list']: arr
      })
    }
  },

  onChangeCourt:function(event) {
    this.setData({
      activeName: event.detail,
    });
  },

  onChangeTime:function(e) {
    var updateItem = "court_time_choose[" + e.currentTarget.dataset.time + "]"
    this.setData({
      [updateItem]: e.detail,
    });
  },

  reqCourtInfo:function() {
    
  },
})