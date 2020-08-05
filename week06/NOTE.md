# 学习笔记

## 作业中的一些jQuery技巧记录

- 实现异步加载/翻页/查询：
  - 单独编写需要异步加载的子页面模板，如`comments.html`；
  - 利用`jQuery`，`$('#xxx').click()`or`$(document).on('click', '#xxx', function)`捕获页面操作；利用`$(window).ready()`捕获加载事件；
  - 通过模板变量获取相应必要参数如`url`；
  - 单独写js调用`.ajax()`发起异步请求；
  - `views.py`中捕获异步请求的，渲染子页面模板，通过`JsonResponse`将渲染的html传递给`.ajax`；
  - `.ajax`中通过`.html`在目标位置插入子页面；
- 实现返回页首的悬浮图标：
  - 在页面的任意位置（一般是页末）添加譬如`<a href="javascript:scroll(0, 0)">Top</a>`的元素，点击后，`href`属性会调用js的`scroll`函数，返回页首
  - 编写相应的css为元素添加样式
  - 编写`jQuery`，通过`$('#xxx').scrollTop()`捕获元素的位置，根据位置，通过`.addClass`/`.remveClass`等函数为元素设置属性进行显示/隐藏；
- 实现异步翻页后定位到指定位置（如定位到第一条评论）
  - 方式1：直接在按钮上使用`href="#xxx"`这样的锚点操作；（定位的锚点会显示在页面url上）
  - 方式2：在按钮上调用`href="javascript:scroll(x, y)`；（不方便根据元素在页面的位置动态调整）
  - 方式3：编写`jQuery`，利用`x = $('#xxx').offset().top`捕获目标位置的垂直坐标；`$(window).scrollTop(x)`定位到指定位置；

## 作业中遇到的问题及解决

### 问题1：`requests`库与`accept-encoding`

- 问题：使用`requests`访问douban页面，结果返回的`response.content`无法解码
- 具体场景：
  - 使用`requests`请求douban页面时，若请求头只配置`user-agent`，获得的`response.content`能够正常被解码
  - 当复制开发者工具中的请求头进行访问，获得的`response.content`无法正常解码，使用chardet工具检测，编码为`None`
- 排查：经过对请求头参数的逐项排查，发现最终问题出现在`accept-encoding`参数上
  - 当不设置`accept-encoding`，响应返回的`content-encoding`是`gzip`
  - 当设置了`'accept-encoding': 'gzip, deflate, br'`，响应返回的`content-encoding`是`br`
  - 问题就出在`gzip`和`br`上
    - `br`是比`gzip`效率更高的压缩编码，当douban检测客户端能够接受`br`时会优先按`br`编码传输
    - 而`requests`的`Response`不支持对`br`的解析
- 解决：`accept-encoding`去除`br`设置即可

### 问题2：`mssql`的`safe-updates`模式

- 问题：手动删除`mysql`相应表的数据时出错，ERROR CODE 1175，mysql版本5.
- 场景：在调试爬虫代码时，因为需要存储重复的数据到数据库，所以经常要手动删除mysql相应表的所有数据，但是执行`delete from table_name`时，数据库提示ERROR CODE 1175，不允许直接删除表所有数据
- 排查：经查询，是因为MySql默认运行在`safe-updates`模式下，该模式会导致非主键条件下无法执行`update`或者`delete`命令
- 解决：在运行命令前，执行`set SQL_SAFE_UPDATES=0`即可。安全起见，执行完删除后，再修改回`set SQL_SAFE_UPDATES=1`

### 问题3：`img`防盗链问题

- 问题：在模板中的`img`元素引用了正确的在线图片链接，但执行代码后，图片未加载。`img`请求返回403错误。
- 原因：提供在线图片的网址可能做了防盗链处理。具体是通过检测请求头的`referrer`参数来达成防盗链处理。
- 解决：为引用图片的`img`元素设置`referrerPolicy="no-referrer"`属性，不在请求头发送`referrer`参数即可解决。

### 问题4：外键约束

- 问题：在创建`movies`和`comments`表时，使用了外键为两个表之间建立了联系，带来方便的同时也产生了约束：主表相应`id`数据未产生时，插入子表对应`id`的数据将会失败；
- 解决：在连接数据库插入数据之前，先取消约束，处理完成后再恢复约束。

### 问题5：无法捕获ajax加载页面元素问题

- 场景：利用`detail.html`渲染详情页，利用`comments.html`渲染评论部分。通过在`detail.html`页面编写jQuery执行ajax将`comments.html`成功插入`detail.html`；现在需要在`detail.html`捕获`comments.html`中的翻页元素，以调用新的ajax实现翻页；
- 问题：直接使用`$('#xxx').click()`捕获不到ajax加载页面目标元素的事件；
- 原因：猜测是在页面捕获目标元素到ajax页面加载之间存在微小延时，导致捕获不到事件
- 解决：利用`jQuery`的`$(selector).on(event,childSelector,data,function)`方法将子页面的目标元素事件绑定到主页面可解决
  - 关于`$(selector).on(event,childSelector,data,function)`：
    - `on()`方法在被选元素及子元素上添加一个或多个事件处理程序；
    - 自jQuery版本1.7起，`on()`方法是`bind()`、`live()`和`delegate()`方法的新的替代品；
    - 使用on()方法添加的事件处理程序适用于当前及未来的元素（比如由脚本创建的新元素）；
  - 解决的代码`$(document).on('click', '#xxx', function(){};)`；
