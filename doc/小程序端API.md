清动家园——小程序端`API`

网址URL:https://cbx.iterator-traits.com

### 身份验证

##### 登录

```js
Method: POST
URL: /api/user/login
Request:
{
   	'js_code': '',
    'token': '',
}
Response:
{
	'message': 'ok',
    'loginToken': '546sdwe54'		
}
```

请求参数`js_code`是微信小程序进行身份认证需要的，`token`用于给助教小程序发送请求。

其中`loginToken`应该被前端存储在**请求头**中，用于后续身份验证。

##### 获取个人信息

```js
Method: GET
URL: /api/user/user
Request:
Response:
{
    "id": 1,
    "phone": "4008823823",
    "openId": "ojXf94o4sj8EZKUS9l5mdn2NsH5U",
    "loginToken": "1",
    "loginTime": "2020-12-18T21:59:07.059572",
    "type": "学生",
    "name": "胡浩宇",
    "nickName": "一只大萝卜",
    "userId": 2017013594,
    "email": "hhy17@mails.tsinghua.edu.cn",
    "major": "软件学院",
    "image": "http://127.0.0.1:8000/media/user/wx45b215f8db5d15f4.o6zAJs8rMS-DuYactSr6tHqzUn-A.WejhT0zkQ95o7920aa1e087379def2638b6_qbyOong.png",
    "defaults": 0,
    "inBlacklist": false,
    "inBlacklistTime": "0"
}
```

其中`defualts`代表个人的违约次数，`inBlacklist`代表是否在黑名单中。

##### 更新个人信息

```js
Method: POST
URL: /api/user/user
Request:
{
    'nickName': '',
    'userId': '',
    'email': '',
    'phone': '',
    'major': '',
    'image': '',
    'type': ''
}
Response:
{
 	'message': 'ok'   
}
```

参数即为用户需要完善的个人信息。解释为`type`是类型，包括在校学生和校友等。`nickName`是昵称。

### 场馆信息

##### 获取场馆信息

```js
Method: GET
URL: /api/user/stadium
QueryParam:{
    'id': ''
    'info': '',
    'name': '',
    'foreGt': '',
    'openState': ''，
    'foreDays':''
}
Response:
[
    {
        "id": 1,
        "images": [
            {
                "id": 1,
                "detail": null,
                "image": "http://127.0.0.1:8000/media/stadium/1.jpg",
                "stadium": 1
            }
        ],
        "comments": 2,
        "score": "3.0",
        "collect": 10,
        "courtTypes": [
            {
                "id": 1,
                "openingHours": "08:00-10:00",
                "type": "篮球",
                "duration": "01:00",
                "price": 1,
                "membership": 1,
                "openState": false
            },
            {
                "id": 2,
                "openingHours": "09:00-11:00 15:00-17:00",
                "type": "羽毛球",
                "duration": "00:30",
                "price": 50,
                "membership": 4,
                "openState": true
            }
        ],
        "name": "综合体育馆",
        "pinyin": "zonghetiyuguan",
        "openTime": "08:00",
        "closeTime": "22:00",
        "openState": true,
        "durations": "01:00",
        "location": "北京市海淀区新民路",
        "longitude": "116.338968",
        "latitude": "40.010093",
        "createTime": "2020-12-01"
    }
]
```

其中，返回值是一个`Json`格式的列表，每一项包含了一个**场馆**的信息。

六个请求参数都是可选的。

`id`是一个整数，代表场馆的编号。

`info`和`name`分别在场馆的信息和名字中进行**模糊匹配**。

`foreGt`是一个整数，代表至少可以多少天提前预约。(比如如果 `foreGt=3`，后端回返回所有至少可以提前$3$天预约的场馆)。

`openState`代表是否开放，布尔值。

`foreDays`是一个整数，代表可提前预约时间。

**新增了加强版**

`URL:/api/user/stadiumdetail`

获取更详细的信息，之前的`URL`只返回一个信息相对较少的列表。

##### 获取场地信息

```js
Method: GET
URL: /api/user/court
QueryParam:
{
    'type': '',	                     
    'priceGt': '',
    'priceLt': '',
    'sort': '',
    'stadium_id',
    'openState',
    'floor',
    'location'
}
Response:
[
    {
        "id": 32,
        "stadiumName": "综合体育馆",
        "foreDays": 3,
        "type": "羽毛球",
        "name": "场地0",
        "price": 30,
        "openState": true,
        "floor": 1,
        "location": "110B",
        "stadium": 10,
        "courtType": 5
    }
]
```

其中，返回值是一个`Json`格式的列表，每一项包含了一个**场地**的信息。

所有参数都是可选的。

其中 `type`代表运动类型。

`priceGt & priceLt`分别代表价格多于某个值和价格少于某个值。

`sort`按照价格排序，`sort=price`代表由小到大，`sort=-price`代表由大到小。

剩下四项都是**精确**匹配。

`stadium_id`代表对应的场馆`id`。

`openState`代表开放状态。

剩下两项就是字面意思。

##### 获取时段信息

```js
Method: GET
URL: /api/user/duration
QueryParam:
{
	  'stadium_id': '',
      'court_id': '',
      'openState': '',
      'accessible': '',
      'startTime': '',
      'date': ''
}
Response:
[
    {
        "id": 241,
        "stadiumName": "综合体育馆",
        "courtName": "场地0",
        "date": "11.16",
        "startTime": "10:00",
        "endTime": "11:00",
        "openState": true,
        "accessible": false,
        "stadium": 10,
        "court": 32,
        "user": 2
    },
]
```

其中，返回值是一个`Json`格式的列表，每一项包含了一个**时段**的信息。

五个参数都为**精确**匹配。

`accessible`代表是否已经被预约。

###### 需求：

​	1. ~~`queryParam`里面加一个date，用于获取某一天内的所有时段~~

​		增加了date，是一个字符串，要求**精确**匹配

### 预订场馆

##### 预定场地

```js
Method: POST
URL: /api/user/reserve/
Request:
{
    'duration_id': '',
}
Response:
{
    "id": 9,
    "stadiumName": "综合体育馆",
    "courtName": "场地0",
    "result": "success",
    "comments": [],
    "has_comments": false,
    "startTime": "11:00",
    "endTime": "12:00",
    "payment": false,
    "cancel": false,
    "checked": false,
    "leave": false,
    "stadium": 10,
    "court": 32,
    "user": 2,
    "duration": 243
}
```

`durationId`为想要预定的时段的 `id`。

##### 查看预定历史

```js
Method: GET
URL: /api/user/reserve
QueryParam:
Response:
[
    {
        "id": 15,
        "result": "success",
        "comments": [
            {
                "id": 32,
                "courtName": "场地4",
                "images": [],
                "content": "有一说一确实得试一下你知道吧，要不然不放心",
                "score": 3,
                "user": 1,
                "court": 52
            }
        ],
        "has_comments": true,
        "stadium": "综合体育馆",
        "court": "场地4",
        "court_id": 52,
        "date": "2020-11-26",
        "startTime": "11:00",
        "endTime": "12:00",
        "payment": false,
        "cancel": false,
        "checked": false,
        "leave": false,
        "user": 1
    }
]
```

返回值是一个列表，每一项代表一次历史消息。

###### 需求：

1. ~~cancel打错了，查看一下数据库里面是`cancle`还是cancel~~

   问题不大，只是文档手滑写错了。

##### 更改预订

```js
Method: PUT
URL: /api/user/reserve
Request:
{
    'id': '',
    'payment': '',
    'cancel': '',
    'checked': '',
    'leave': ''
}
Response:
{
    'message': 'ok',
}
```

其中 `id`代表要取消预定的时段 `id`。

四个参数都是可选的，代表这个预定的状态。

其中`cancel`应该进行合法性检查，暂时不清楚前端还是后端做。

**删除历史记录**

```js
Method: DELETE
URL: /api/user/reserve
Request:
{
    'id': '',
}
Response:
{
    'message': 'ok',
}
```

`id`为要删除的记录的`id`

###### 需求：

1. ~~查看预定历史中添加一个字段表示用户是否已经评价，如果有评价需要评价的id~~

   增加了comments和has_comments返回值，前者返回一个comments列表，后者返回一个布尔值，如果为True代表已经评论过，否则为没有评论过。

  2. ~~查看预定里面没给预定时段id~~

     返回在`duration_id`中，但是`duration`是会每天更新的，不应该用这个东西作为筛选的参数。

### 评价场馆

##### 查看个人对场馆的评价

```js
Method: GET
URL: /api/user/comment
Request:{
    'content': '',
    'court_id': ''，
    'stadium_id': '',
    'page': '',
    'size': ''
}
Response:
[
    {
        "id": 22,
        "courtName": "场地0",
        "images": [],
        "content": "#includ<iostream>",
        "score": 3,
        "user": 2,
        "court": 33,
        "reserve": 8
    }
]
```

其中返回值是一个列表，每一项代表一个评价信息。

`images`是一个图片列表，每一项代表一个图片的`URL`。

请求参数都是可选的。

`content`在评价内容中进行模糊匹配。

`court_id`**精确**匹配场地编号。

`stadium_id`精确匹配场馆编号。

`page`和`size`是分页参数，`page`代表分页的第几页，`size`代表一页的大小。

**评价场馆**

```js
Method: POST
URL: /api/user/comment
Request:{
    'reserve_id': '',
    'content': '',
}
Response:
{
    "id": 23,
    "courtName": "场地0",
    "images": [],
    "content": "虽然不是同一个时间，但是是同一个厕所",
    "score": 3,
    "user": 2,
    "court": 33,
}
```

这里的评价是基于`ReserveEvent`的，并且绑定到一个预订事件中。

请求参数分别为事件的`Id`和评价内容。

`content`要求至少为$5$字，最多为$300$字。

**撤销评价**

```js
Method: DELETE
URL: /api/user/comment
Request:{
    'comment_id': '',
}
Response:
{
    'message': 'ok',
}
```

参数为要撤销的评价的 `Id`。

**上传评价图片**

```js
Method: POST
URL: /api/user/commentimage
Request:{
    'comment_id': ''
}
Response:
{
    "id": 12,
    "image": "http://127.0.0.1:8000/media/comment/timg_Pi3DKKT.jpg",
    "comment": 23
}
```

返回值中`image`为图片的`URL`，可以直接访问。

#### 收藏体育馆

**收藏体育馆**

```js
Method: POST
URL: /api/user/collect
Request:{
    'stadium_id': '',
    'detail': ''
}
Response:
{
    "id": 3,
    "stadium_name": "西区体育馆",
    "detail": "明天打算去",
    "user": 2,
    "stadium": 11
}
```

其中`detail`是收藏的备注。

**查看收藏的体育馆**

```js
Method: GET
URL: /api/user/collect
Request:{
    'detail': '',
    'id': '',
    'stadium_id'
}
Response:
[
    {
        "id": 2,
        "stadium_name": "综合体育馆",
        "detail": "明天打算去",
        "user": 2,
        "stadium": 10
    },
    {
        "id": 3,
        "stadium_name": "西区体育馆",
        "detail": "明天打算去",
        "user": 2,
        "stadium": 11
    }
]
```

请求参数分别是收藏备注`detail`的模糊匹配，该条收藏信息的精确匹配和场馆`stadium_id`的精确匹配。

结果是一个列表。

**取消收藏**

```python
Method: DELETE
URL: /api/user/collect
Request:{
    'collect_id': ''
}
Response:
{
    'message': 'ok'
}
```

#### 站内会话

##### 查看所有会话

```js
Method: GET
URL: /api/user/session
Request:{
    'id': '',
    'open': '',
    'checked': ''
    'sort': ''
}
Response:
[
    {
        "id": 3,
        "messages": [],
        "user_id": 2,
        "open": true,
        "checked": false,
        "createTime": "2020-12-10T03:50:39.587558Z",
        "updateTime": "2020-12-10T03:50:39.587558Z"
    },
]
```

请求参数中`open`字段代表会话是否关闭，`checked`代表管理员是否已经审核。

`sort`目前支持按照`createTime`和`updateTime`排序。

返回值中`messages`是一个列表，每一项是一条消息。

**创建会话**

```js
Method: POST
URL: /api/user/session
Request:{}
Response:
{
    "id": 11,
    "messages": [],
    "user_id": 2,
    "open": false,
    "checked": false,
    "createTime": "2020-12-10T09:56:56.624058Z",
    "updateTime": "2020-12-10T09:56:56.624058Z"
}
```

不需要任何参数。

**关闭会话**

```js
Method: PUT
URL: /api/user/session
Request:{
    'session_id': ''
}
Response:
{
    'message': 'ok'
}
```

**发送消息**

```js
Method: POST
URL: /api/user/message
Request:{
    'session_id': '',
    'content': ''
}
Response:
{
    "id": 10,
    "sender": "U",
    "content": "我们是尽力局",
    "createTime": "2020-12-10T10:01:55.554084Z",
    "session": 11
}
```

请求参数中`session_id`代表会话的`id`，`content`代表消息内容。

**查看消息**

```js
Method: GET
URL: /api/user/message
Request:{
    'session_id': '',
    'id': '',
    'sort': '',
    'content': ''
}
Response:
[
    {
        "id": 2,
        "sender": "U",
        "content": "管理员您好，我上当了",
        "createTime": "2020-12-10T04:16:16.262133Z",
        "session": 2
    }
]
```

参数`sort`表示排序，目前只支持按照`createTime`排序，`content`按照模糊匹配查找。

## 需求：

请求失败会返回什么？

所有异常都会返回类似下方的结果。

```python
{
    "error": {
        "detail": "Method \"POST\" not allowed."
    }
}
```

其中必定包含`error`字段，其内部是具体的错误信息。

需要注意的是，使用`GET`请求进行筛选时，如果没有得到数据可能是筛选结果是一个空列表，这个时候是不会有`error`字段的。