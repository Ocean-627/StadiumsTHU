# 清动家园——小程序端`API`

### 身份验证

##### 注册

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

其中：四个字段都是**必须的**。

用户名：要求长度在$3-32$之间。

密码：要求长度在$10-32$之间，且必须包含数字，小写字母和大写字母。

学生编号：不允许重复，即一个编号只能注册一个用户。

##### 登录

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

其中`loginToken`应该被前端存储在**请求头(目前是`query_params`)**中，用于后续身份验证。

##### 登出

```js
Method: POST
URL: /api/user/logout/
Response:
{
	'message': 'ok'
}
```

##### 更新个人信息

```js

```

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
        },
    ]
```

其中，返回值是一个`Json`格式的列表，每一项包含了一个**场馆**的信息。

四个请求参数都是可选的。

`info`和`name`分别在场馆的信息和名字中进行**模糊匹配**。

`foreGt`是一个整数，代表至少可以多少天提前预约。(比如如果 `foreGt=3`，后端回返回所有至少可以提前$3$天预约的场馆)。

`openState`代表是否开放，布尔值。

`foreDays`是一个整数，代表可提前预约时间。

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

### 预订场馆

##### 预定场地

```js
Method: POST
URL: /api/user/reserve
Request:
{
    'durationId': '',
}
Response:
{
    'message': 'ok',
    'eventId': ''
}
```

`durationId`为想要预定的时段的 `id`。

##### 查看预定历史

```js
Method: GET
URL: /api/user/reserve
QueryParam:
Response:
{
    'message': 'ok',
    'history':[
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
}
```

其中 `history`是一个列表，每一项代表一次历史消息。

##### 取消预订

```js
Method: PUT
URL: /api/user/reserve
Request:
{
    'eventId': '',
}
Response:
{
    'message': 'ok',
}
```

其中 `eventId`代表要取消预定的时段 `id`。

### 评价场馆

##### 查看个人对场馆的评价

```js
Method: GET
URL: /api/user/comment
Request:
Response:
{
    'message': 'ok',
    'comments':[
        {
         	'user': '',
            'court': '',
            'courtName': '',
            'content': '',
            'images': ''
        }
    ]
}
```

其中 `comments`是一个列表，每一项代表一个评价信息。

`images`是一个图片列表，每一项代表一个图片的`URL`。

**评价场馆**

```js
Method: POST
URL: /api/user/comment
Request:{
    'courtId': '',
    'content': '',
}
Response:
{
    'message': 'ok',
    'commentId': ''
}
```

请求参数分别为场地的`Id`和评价内容。

`content`要求至少为$15$字，最多为$300$字。

回复结果 `commentId`为该条评论的 `Id`。

**撤销评价**

```js
Method: DELETE
URL: /api/user/comment
Request:{
    'commentId': '',
}
Response:
{
    'message': 'ok',
}
```

参数为要撤销的评价的 `Id`。

