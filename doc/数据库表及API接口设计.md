## 清动家园——数据库表及API接口设计

### 数据库表设计

#### User 普通用户

```js
username    用户名
password    密码
userId      学号
email       邮箱        
loginToken  登录的令牌
phone		手机号
// 尚未加入
major       所在院系        
notice      未读通知列表
violations  违规次数        
```

#### Manager 场馆管理员

```js
username    用户名
password    密码
userId      工号
email       邮箱
workplace   所在场馆名称
workplaceId 所在场馆编号
loginToken  登录的令牌
// 尚未加入
notice      未读通知列表
```

#### Stadium 场馆

```js
name         场馆名称
information  场馆信息
openingHours 开放时间段划分情况
openTime     开馆时间
closeTime    闭馆时间
contact      联系方式            
openstate    是否开放        
foredays     可提前预约天数
durations    单位预定时间(比如羽毛球可能是以一小时为单位)
// 尚未加入
location	 位置
```

#### Court 场地

```js
stadium      所属场馆
type         场地类型(如羽毛球、网球)
name         场地名称
price        价格
openingHours 开放时间段划分情况
openState	 开放状态
floor        所在楼层
location     位置信息
// 尚未加入
duration     单次预订时常限制
closeTime    临时关闭时间
```

#### Duration 预约时段

```js
stadium       所属场馆
court		  所属场地
user		  预订者
date          日期
startTime     开始时间
endTime       结束时间
openState     开放状态
accessible    是否可以预订
```

#### **ChangeDuration （永久）修改预约时段事件**

```js
manager      管理员             
stadium      场馆                   
openingHours 开放时间段划分情况     
date    	 生效日期
time         操作时间
type         操作类型            // 默认修改预约时段事件类型为1
```

#### **AddEvent （临时）添加活动事件**

```js
manager      管理员              
court        场地                
startTime    开始时间
endTime      结束时间
date         活动日期
time         操作时间
type         操作类型            // 默认修改预约时段事件类型为2
```

#### **ReserveEvent 预订事件**

```js
stadium      对应场馆
court        对应场地
user         对应用户
duration	 对应时段
startTime    开始时间
endTime      结束时间
result       预约结果
payment      是否已付费
cancel       是否已取消
repayment    是否已还款
checked      是否已使用
leave        是否已离开
```

#### **Comment** 评价场地信息

```js
user		 评价者
court		 被评价场地
content  	 评价信息
```

#### CommentImage 评价对应的附图

```js
comment		 对应评价
image		 附图
```

#### UserImage 用户图片

```js
user		 对应用户
image		 图片
```

#### StadiumImage 场馆图片

```js
stadium		 对应场馆
image		 图片
```

### **API设计**

#### 身份验证

##### 普通用户注册

```js
Method: POST
Request:
URL: /api/user/logon
Request:
{
   	'username': '',
   	'password': '',
   	'email': ''，
   	'userId':''
}
Response:
{
	'message': 'ok'
}
```

**管理员注册**

```js
Method: POST
Request:
URL: /api/manager/logon
Request:
{
   	'username': '',
   	'password': '',
   	'email': ''，
   	'userId':''
}
Response:
{
	 'message': 'ok'
}
```

##### 普通用户登录

```js
Method: POST
URL: /api/user/login
Request:
{
   	'userId': '',
   	'password': ''
}
Response:
{
	'message': 'ok',
    'loginToken': '546sdwe54'		
}
```

##### **管理员登录**

```js
Method:POST	
URL:/api/manager/login
Request:{
    'userId': '',
    'password': ''
}
Response:{
   	'id',1,
   	'username': '',
   	'token': '',
   	'stadiumId':'',
   	'stadium':''
}	
```

##### 登出

```js
Method: POST
URL: /api/logout/
Response:
{
	'message': 'ok'
}
```

其他可能需求：修改密码、修改个人信息。

##### 获取场馆信息

```js
Method: GET
URL: /api/user/stadium
QueryParam:
Response:
{
    'message': 'ok',
     // stadims,一个列表,每个元素是一个字典，一个场馆的信息
    'stadiums':[
        {
            'id': '',
            'name': '',
            'information': '',
            'foreDays': '', 		                      //可以考虑合并到infomartion
            'contact': '',
            'openTime': '',
            'closeTime': '',
            'openState': '',
           	'openingHours': '',
            'location': ''
        }
    ]
}
```

##### 获取场地信息列表

```js
Method: GET
URL: /api/user/court
QueryParam:
{
    'id': ''	                     // 可选参数，场馆id
    'type': ''						 //	可选参数，场地类型
}
Response:
{
    'message': 'ok',
    // courts,一个列表,每个元素是一个字典，包含该场馆所有场地的信息
    'courts':[
        {
            'id': '',
            'type': '',
            'name': '',
            'price': '',
            'openingHours': '',
            'openState': '',
            'location': ''		    // 可选项，可以缺省
        }
    ]
}
```

##### 获取预约时段信息

```js
Method: GET
URL: /api/user/court/reserve
QueryParam:
{
	  'id': '',	                         // 场地id
}
Response:
{
    'message': 'ok',
    // durations,一个列表,每个元素是一个字典，包含该场地所有预约时段的信息
    'durations':[
        {
            'id': '',
            'date': '',
            'startTime': '',
            'endTime': '',
            'accessible': '',
            'openState': ''
        }
    ]
}
```

其他与场馆信息相关：获取其他用户评价。

##### 预定场馆 (加入志愿或预定场地)

```js
Method: POST
URL: /api/user/reserve
Request:
{
    'durationId': '',	     // 预约时段id
}
Response:
{
    'message': 'ok',
}
```

##### 查看历史消息

```js
Method: GET
URL: /api/user/reserve
QueryParam:
Response:
{
    // history,一个列表,每个元素是一个字典，包含一次操作
    'message': 'ok',
    'history':[
        {
            'stadiumName': '',
            'courtName': '',
            'result': '',		         // 如果result === False则下面几项信息都为空
            'payment': '',
            'cancle': '',
            'startTime': '',
            'endTime': '',
            'checked': '',
            'leave': ''
        }
    ] 
}
```

其他操作相关：评价场地、付费。

#### 管理员相关接口（面向管理员）

##### **获取场地信息列表**

```js
Method:GET
URL: /api/manager/court
QueryParam:{
	 'stadiumId': '19',
   'floor':'1',
   'date':'2020-10-31',
}
Response:{
    'floor':'',
    'number':'',// 该层场地总数
    'duration':'01:00',
    'court':[
        {
            'id':1,
            'location':'',
            'openingHours':'08:00-12:00 14:00-18:00',
            'reservedDuration':[(1,'08:00','9:00','清小软'),(6,'15:00','16:00','清大软')],
            'notReservedDuration':[(2,'09:00','10:00'),(3,'10:00','11:00'),(4,'11:00','12:00'),(5,'14:00','15:00'),(7,'16:00','17:00'),(8,'17:00','18:00')],
            'comment':''
        }
    ]
}	
```

##### **获取场地预约详情**

```js
Method:GET
URL: /api/manager/court/reserve
QueryParam:{
	'courtId': '',
  'durationId':''
}
// 待改
Response:{
    'userId':'',
    'eventId':'',
    'startTime':'08:00',
    'endTime':'09:00',
    'payment':True,
    'checked':True,
    'cancel':False,
    'repayment': False,
    'leave':False,
}	
```

##### **【新】修改场地类型开放时间**  

```js
Method:POST
URL: /api/manager/changeduration/
Request:{
    'date':2020-12-15,                                     
    'courtType_id':1,
    'openingHours':'08:00-10:00'
		'details':'学校通知调整'          // 可选参数，即对应网页端的备注选项
}
Response:{
    'message':'ok',
}
```

##### **【新】添加场地占用**

```js
Method:POST
URL: /api/manager/addevent/
Request:{
    'manager_id':1,
    'court_id':2,
    'date':'2020-12-15',
    'startTime':'09:15',
    'endTime':'09:45'，
    'details':'马杯赛事'            // 可选参数，即对应网页端的备注选项
}
Response:{
    'message':'ok'
}
```

##### **【新】获取特定用户信用记录**

```js
Method:GET
URL: /api/manager/default/
Request:{
    'user_id':1,
}
Response:{
    "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "date": "2020-12-14",
            "time": "22:29",
            "cancel": true,
            "detail": "预约不来",
            "valid": true,
            "user": 1
        },
        {
            "id": 2,
            "date": "2020-12-14",
            "time": "22:29",
            "cancel": true,
            "detail": "预约不来",
            "valid": true,
            "user": 1
        },
        {
            "id": 3,
            "date": "2020-12-14",
            "time": "22:29",
            "cancel": true,
            "detail": "预约不来",
            "valid": true,
            "user": 1
        },
        {
            "id": 9,
            "date": null,
            "time": null,
            "cancel": false,
            "detail": "预约不来",
            "valid": false,
            "user": 1
        }
    ]
}
```

##### **【新】撤销信用记录**

```js
Method:PUT
URL: /api/manager/default/
Request:{
    'default_id':1,
    'detail':''                   // 可选参数，对应备注
}
Response:{
    'message':'ok'
}
```

##### **【新】将用户移入或移出黑名单**

```js
Method:PUT
URL: /api/manager/user/
// 若用户在黑名单中，该操作将用户移出黑名单，等价于手动撤销全部信用记录
// 若用户不在黑名单中，该操作将用户移入黑名单
Request:{
    'user_id':1,
}
Response:{
    'message':'ok'
}
```


##### **查看用户列表**

```js
Method:GET
URL: /api/manager/users
QueryParam:{
    'managerId':1
}
Response:{
    'users':[
        {
            'username':'',
            'userId':'',
            'major':'',
            'violations':1
        }
    ]
}	
```

##### **获取历史操作列表**

```js
Method:GET
URL: /api/manager/history
QueryParam:{
    'managerId':1,
    // 暂不支持
    //'page':1,
    //'size':10
}
Response:{
    'operations':[
        {
            'time':'2020-10-30T15:00:00+08:00',
            'type':1,
            'eventId':2
        }
    ]
}	
```

##### **查看修改场地预订时间详情**

```js
Method:GET
URL: /api/manager/get/change
QueryParam:{
    'eventId':2,
}
Response:{
    'startDate':'2020-11-01',
    'duration':'02:00',
    'openTime':'09:00',
    'closeTime':'22:00',
    'openHours':[(09:00,12:00),(13:00,17:00),(18:00,22:00)]
}	
```

##### **查看添加临时占用事件详情**

```js
Method:GET
URL: /api/manager/get/event
QueryParam:{
  	'eventId':2,
}
Response:{
    'court':'九号场地',
    'courtId':9,
    'date':'2020-10-31',
    'startTime':'09:00',
    'endTime':'12:00',
    'closeDuration':[(08:00,10:00),(10:00,12:00)]
}	
```

##### **撤销操作请求**(未做)

```js
Method:POST
URL: /api/manager/revoke
QueryParam:{
    'id':2,
    'userId':2018013396,
    'username':'管理员A'
}
Response:{
    'message':'ok'
}	
```