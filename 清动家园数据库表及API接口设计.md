## 清动家园——数据库表及API接口设计

### 数据库表设计

#### User 普通用户

```js
username    用户名
major       所在院系        // 可选
password    密码
userId      学号
email       邮箱           // 可选
phone       手机号         // 可选
loginToken  登录的令牌
notice      未读通知列表
violations  违规次数        // 高级需求
```

#### Manager 场馆管理员

```js
username    用户名
workplace   所在场馆名称
workplaceId 所在场馆编号
email       邮箱          // 可选
password    密码
userId      工号
loginToken  登录的令牌
notice      未读通知列表
```

#### Stadium 场馆

```js
name         场馆名称
information  场馆信息
contact      联系方式            // 可考虑与场馆信息合并
openTime     开馆时间
closeTime    闭馆时间
openstate    是否开放
openingHours 开放时间段划分情况
location     位置信息            // 可能是存一个指向地图的url
foredays     可提前预约天数
```

#### Court 场地

```js
stadium      所属场馆
floor        所在楼层
type         场地类型(如羽毛球、网球)
name         场地名称
price        价格
openingHours 开放时间段划分情况
durations    单次预订时常限制
location     位置信息
close        是否临时关闭
closeTime    临时关闭时间
```

#### Duration 预约时段

```js
stadium       所属场馆
name          场地名称
date          日期
startTime     开始时间
endTime       结束时间
cloes         是否临时关闭         // 高级需求
accessible    是否已被预订
```

#### **ChangeDuration （永久）修改预约时段事件**

```js
stadiumId    场馆ID
openingHours 开放时间段划分情况     
```

#### **AddEvent （临时）添加活动事件**

```js
courtId      场地ID
openingHours 开放时间段划分情况
date         事件日期
```

#### **ReserveEvent 预订事件**

```js
stadiumId    场馆ID
stadiumName  场馆名
courtId      场地ID
courtName    场地名
userId       用户ID
startTime    开始时间
endTime      结束时间
result       预约结果            // 针对填志愿和抽签需求
payment      是否已付费
cancel       是否已取消
repayment    是否已还款
checked      是否已使用
leave        是否已离开
```

#### **Comment** 评价场地信息 （可留作后续迭代）

```js
stadiumId    场馆ID
courtId      场地ID
userId       用户ID            // 扩展：匿名？
information  评价信息
```

### **API设计**

#### 身份验证

##### 注册

```js
Method: POST
Request:
URL: /api/logon
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
	 'message': 'ok'
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
   'workplace':''
}	
```

##### 登出

```js
Method: POST
URL: /api/logout
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
	  'id': ''	                     // 场馆id
}
Response:
{
    'message': 'success',
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
    'id': '',	     // 预约时段id
    'userId':'',   // 申请者id
}
Response:
{
    'message': 'ok',
}
```

##### 查看历史消息

```js
Method: GET
URL: /api/user/history
QueryParam:
{
	  'userId': '',	                     // 用户id
}
Response:
{
    // history,一个列表,每个元素是一个字典，包含一次操作
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
	'workplace': '',
    'floor':'',
    'date':'',
}
Response:{
    'floor':'',
    'number':'',
    'duration':'01:00',
    'court':[
        {
            'id':1,
            'location':'',
            'accessibleDuration':[('08:00','12:00'),('14:00','18:00')],
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

##### **（永久）修改场地预约时间**

```js
Method:POST
URL: /api/manager/change
Request:{
    'id':1,
    'username':'管理员A',
	'stadium': '紫荆乒羽馆',
    'startDate':'2020-11-01',
    'duration':'02:00',
    'openTime':'09:00',
    'closeTime':'22:00',
    'openHours':[(09:00,12:00),(13:00,17:00),(18:00,22:00)]
}
Response:{
    'message':'ok',
}	
```

##### **（临时）添加场地占用**

```js
Method:POST
URL: /api/manager/event
Request:{
    'id':1,
    'username':'管理员A',
	'stadium': '紫荆乒羽馆',
    'court':'九号场地',
    'courtId':9,
    'date':'2020-10-31',
    'startTime':'09:00',
    'endTime':'12:00',
    'closeDuration':[(08:00,10:00),(10:00,12:00)]
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
    'id':1,
    'username':'管理员A',
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
    'id':1,
    'username':'管理员A',
    'page':1,
    'size':10
}
Response:{
    'operations':[
        {
            'time':'2020-10-30T15:00:00+08:00',
            'type':1,
            'name':'修改场地预订时间'，
            'id':2
        }
    ]
}	
```

##### **查看修改场地预订时间详情**

```js
Method:GET
URL: /api/manager/change
QueryParam:{
    'id':2,
    'userId':2018013396,
    'username':'管理员A'
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
URL: /api/manager/event
QueryParam:{
    'id':2,
    'userId':2018013396,
    'username':'管理员A'
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

##### **撤销操作请求**

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