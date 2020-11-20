# Web-Frontend 开发文档

## 库的引入

### 全局使用的库

css：引入到``App.vue``中

js：引入到``index.html``中

因为有些js存在依赖关系，而vue的import无法保持这种依赖关系，除非重构库文件。~~说到底jquery的库在vue下适配性确实很差。~~

### 局部使用的库

在组件的style和script分别import即可。

## 注意事项

- 路由跳转时最好使用href标签，需要参数可以使用:href标签，实在不行就用``window.location.replace()``，不要用``this.$router.push()``，否则会导致全局js失效。
- 使用swal时，用箭头函数不要用function()，否则会导致this指针引用出错。

## 留下的坑

- 有朝一日可能要重构这个库引入的逻辑。但是jquery适配性太差了以至于我都不知道能不能重构。

