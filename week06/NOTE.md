# 学习笔记

## 作业中遇到的问题及解决

### 问题1

- 问题：使用requests访问douban页面，结果返回的response.content无法解码
- 具体场景：
  - 使用requests请求douban页面时，若请求头只配置user-agent，获得的response.content能够正常被解码
  - 当复制开发者工具中的请求头进行访问，获得的response.content无法正常解码，使用chardet工具检测，编码为none
- 排查：经过对请求头参数的逐项排查，发现最终问题出现在accept-encoding参数上
  - 当不设置`accept-encoding`，响应返回的`content-encoding`是`gzip`
  - 当设置了`'accept-encoding': 'gzip, deflate, br'`，响应返回的`content-encoding`是`br`
  - 问题就出在`gzip`和`br`上
    - `br`是比`gzip`效率更高的压缩编码，当douban检测客户端能够接受`br`时会优先按`br`编码传输
    - 而`requests`的`Response`不支持对`br`的解析
- 解决：`accept-encoding`去除`br`设置即可

### 问题2

- 问题：手动删除mysql相应表的数据时出错，ERROR CODE 1175，mysql版本5.
- 场景：在调试爬虫代码时，因为需要存储重复的数据到数据库，所以经常要手动删除mysql相应表的所有数据，但是执行`delete from table_name`时，数据库提示ERROR CODE 1175，不允许直接删除表所有数据
- 排查：经查询，是因为MySql默认运行在`safe-updates`模式下，该模式会导致非主键条件下无法执行`update`或者`delete`命令
- 解决：在运行命令前，执行`set SQL_SAFE_UPDATES=0`即可。安全起见，执行完删除后，再修改回`set SQL_SAFE_UPDATES=1`
