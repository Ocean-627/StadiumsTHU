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
	'auth': '',
    'name': '',
    'userId': '',
    'email': '',
    'phone': ''
    'loginToken': ''
    'loginTime': ''
    'openId': ''
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

 3. 头像，以及修改头像

### 场馆信息

##### 获取场馆信息

```js
Method: GET
URL: /api/user/stadium
QueryParam:{
    'info': '',
    'name': '',
    'foreGt': '',
    'openState': ''，
    'foreDays':''
    ‘id’:''
}
Response:
    [
        {
            'id': '',
            'name': '',
            'information': '',
            'openingHours': '',
            'openTime': '',
            'closeTime': '',
            'contact': '',
            'openState': '',
            'foreDays': '',
           	'durations': '',
            // 新增
            'courtType': ['', ],
            'comments': '',
            'score':'',
            'location':'',
        },
    ]
```

其中，返回值是一个`Json`格式的列表，每一项包含了一个**场馆**的信息。

四个请求参数都是可选的。

`info`和`name`分别在场馆的信息和名字中进行**模糊匹配**。

`foreGt`是一个整数，代表至少可以多少天提前预约。(比如如果 `foreGt=3`，后端回返回所有至少可以提前$3$天预约的场馆)。

`openState`代表是否开放，布尔值。

`foreDays`是一个整数，代表可提前预约时间。

`id`是一个整数，代表场馆的编号。

###### 需求

	1. 添加场馆地理位置（描述信息(xx路)和经纬度）
​		目前返回在`location`中

  1. ~~添加场馆运动项目信息~~

     返回在`courtType`中。

  2. ~~添加场馆评分和评论数信息~~

     分别返回在`score`和`location`中

  3. 添加/api/user/stadium/{stadium-id}接口来获取某个场馆具体信息，包括场馆简介，场馆须知，评论

  4. 场馆图片(1张)

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
            'id': '',
            'stadium_id': '',
            'stadiumName': '',
            'type': '',
            'name': '',
            'price': '',
            'openState': '',
            'floor': '',
            'location': ''
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

1. 场地能够提前多少天预约

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
      'startTime': ''
}
Response:
    [
        {
            'stadiumName': '',
            'courtName': '',
            'id': '',
            'date': '',
            'startTime': '',
            'endTime': '',
            'accessible': '',
            'openState': ''
        }
    ]
```

其中，返回值是一个`Json`格式的列表，每一项包含了一个**时段**的信息。

五个参数都为**精确**匹配。

`accessible`代表是否已经被预约。

其余四个参数见字面含义。

###### 需求：

​	1. queryParam里面加一个date，用于获取某一天内的所有时段



### 预订场馆

##### 预定场地

```js
Method: POST
URL: /api/user/reserve
Request:
{
    'duration_id': '',
}
Response: 一个字典，包含models.ReserveEvent的所有字段
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
            'stadiumName': '',
            'courtName': '',
            'result': '',
            'payment': '',
            'cancle': '',
            'startTime': '',
            'endTime': '',
            'checked': '',
            'leave': ''
        }
    ] 
```

返回值是一个列表，每一项代表一次历史消息。

###### 需求：

	1. cancel打错了，查看一下数据库里面是cancle还是cancel
 	2. 

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

	1. 查看预定历史中添加一个字段表示用户是否已经评价，如果有评价需要评价的id
 	2. 查看预定里面没给预定时段id

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
{
    [
        {
         	'user': '',
            'court': '',
            'courtName': '',
            'content': '',
            'images': [
                ''
            ]
        }
    ]
}
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
    'court_id': '',
    'content': '',
}
Response: 一个字典，包含models.Comment的所有字段
```

请求参数分别为场地的`Id`和评价内容。

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





## 需求：

​	请求失败会返回什么？