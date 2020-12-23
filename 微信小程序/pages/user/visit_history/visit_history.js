import Dialog from '../../../miniprogram/miniprogram_npm/@vant/weapp/dialog/dialog'
Page({
  data:{
    records: [],
    localData: [],
  },

  onLoad:function() {
    this.data.localData = JSON.parse(wx.getStorageSync('visitHistory'))
    const num = this.data.localData.length
    var recordList = []
    for(var i=num-1; i>=0; i--) {
      let info = this.data.localData[i]
      recordList.push({
        'text':info.time,
        'desc':'['+info.type+'] '+info.target.name
      })
    }
    this.setData({
      records:recordList
    })
  },

  // 跳转到对应的记录
  jmpRecord:function(e) {
    const num = this.data.localData.length
    const info = this.data.localData[num - e.detail - 1]
    wx.navigateTo({
      url: '/pages/stadium/info/stadium?'+'id='+info.target.id,
    })
  },

  // 清空记录
  onClearRecord() {
    const _this = this

    Dialog.confirm({
      title:'温馨提示',
      message:'清空操作无法进行撤销，是否确认继续？'
    }).then(()=>{
      // 确认
      wx.setStorageSync('visitHistory',JSON.stringify([]))
      _this.setData({
        localData:[],
        records:[],
      })
    })
  }
})