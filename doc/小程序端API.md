# 清动家园——小程序端`API`

网址URL:https://cbx.iterator-traits.com

### 身份验证

##### 登录

```js
Method: POST
URL: /api/user/login
Request:
{
   	'code': '',
}
Response:
{
	'message': 'ok',
    'loginToken': '546sdwe54'		
}
```

其中`loginToken`应该被前端存储在**请求头**中，用于后续身份验证。

##### 获取个人信息

```js
Method: GET
URL: /api/user/user
Request:
Response:
{
    "id": 2,
    "phone": "18801225328",
    "openId": "yyh",
    "loginToken": "3",
    "loginTime": "2020-11-30T15:56:07.143532Z",
    "auth": false,
    "name": "cbx",
    "nickName": "战神",
    "userId": 2018011894,
    "email": "cbx@qq.com",
    "image": "/media/user/timg_VCjkG6O.jpg"
}
```

##### 更新个人信息

```js
Method: POST
URL: /api/user/user
Request:
{
	'auth': '',
    'name': '',
    'userId': '',
    'email': '',
    'phone': ''
    'image': ''
}
Response:
{
 	'message': 'ok'   
}
```

参数即为用户需要完善的个人信息，其中`auth`字段代表用户是否绑定了清华身份，其他字段为具体信息。

###### 需求：

 1. ~~个人信息添加nickname字段，代表昵称，name代表真实姓名，在评论显示的时候使用昵称。~~

    加上了

 2. ~~为什么更新信息用的是GET指令？~~

    应该用POST

 3. ~~头像，以及修改头像~~

    增加了image字段，在body中传入image即可

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
        "id": 11,
        "images": [],
        "comments": 0,
        "score": 3,
        "courtTypes": [
            {
                "id": 7,
                "openingHours": "8:00-10:00 13:00-17:00",
                "type": "羽毛球",
                "duration": "01:00",
                "price": 30,
                "membership": 3
            },
            {
                "id": 8,
                "openingHours": "8:00-10:00 13:00-17:00",
                "type": "篮球",
                "duration": "01:00",
                "price": 30,
                "membership": 3
            }
        ],
        “collect”: true,
        "name": "西区体育馆",
        "pinyin": "xiqutiyuguan",
        "information": "cbx用来写bug的场馆",
        "openTime": "07:00",
        "closeTime": "18:00",
        "contact": "18801225328",
        "openState": true,
        "foreDays": 2,
        "durations": "02:00",
        "location": "至善路",
        "longitude": "106.332390",
        "latitude": "40.004239"
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

###### 需求

1. ~~添加场馆地理位置（描述信息(xx路)和经纬度）~~

​		目前返回在`location`,`latitude`和`longtitude`中

  1. ~~添加场馆运动项目信息~~

     返回在`courtType`中。

  2. ~~添加场馆评分和评论数信息~~

     分别返回在`score`和`location`中

  3. ~~添加/api/user/stadium/{stadium-id}接口来获取某个场馆具体信息，包括场馆简介，场馆须知，评论~~

     请求参数中增加id=要查询场馆参数即可

  4. ~~场馆图片(1张)~~

     返回在images列表中，列表中每一项是图片的URL，可以直接访问。

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

###### 需求：

1. ~~场地能够提前多少天预约~~

   返回在`foreDays`中

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
      'data': ''
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
URL: /api/user/reserve
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
        "id": 7,
        "stadiumName": "综合体育馆",
        "courtName": "场地0",
        "result": "success",
        "comments": [],
        "has_comments": false,
        "startTime": "10:00",
        "endTime": "11:00",
        "payment": false,
        "cancel": false,
        "checked": false,
        "leave": false,
        "stadium": 10,
        "court": 32,
        "user": 2,
        "duration": 241
    },
]
```

返回值是一个列表，每一项代表一次历史消息。

###### 需求：

1. ~~cancel打错了，查看一下数据库里面是`cancle`还是cancel~~

   问题不大，只是文档手滑写错了。

##### 取消预订

```js
Method: PUT
URL: /api/user/reserve
Request:
{
    'event_id': '',
}
Response:
{
    'message': 'ok',
}
```

其中 `eventId`代表要取消预定的时段 `id`。

###### 需求：

1. ~~查看预定历史中添加一个字段表示用户是否已经评价，如果有评价需要评价的id~~

   增加了comments和has_comments返回值，前者返回一个comments列表，后者返回一个布尔值，如果为True代表已经评论过，否则为没有评论过。

  2. ~~查看预定里面没给预定时段id~~

     返回在`duration`中

### 评价场馆

##### 查看个人对场馆的评价

```js
Method: GET
URL: /api/user/comment
Request:{
    'content': '',
    'court_id': ''
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
    "reserve": 8
}
```

这里的评价是基于`ReserveEvent`的，并且绑定到一个预订事件中。

请求参数分别为事件的`Id`和评价内容。

`content`要求至少为$15$字，最多为$300$字。

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