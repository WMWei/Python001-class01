
## 问题

### django反向orm导致ValueError

场景：利用`python manage.py inspectdb`反向生成`models.py`，执行`python manage.py migrate`报错`ValueError: source code string cannot contain null bytes`
原因：新生成的文件编码为`utf-16`导致识别失败
解决：修改编码为`utf-8`


### mysql和django的时区问题

场景：

- Django中，`TIME_ZONE = 'Asia/ShangHai'`
- MYSQL中，`TIME_ZONE = 'Asia/ShangHai'`
- 在MYSQL中使用`TIMESTAMP`存储时间

导致的问题：Django从MYSQL读取的时间比实际的当前时区实际晚了8小时

原因：

- `TIMESTAMP`字段按MYSQL设定的时区读取写入的时间，并将其转换为唯一的时间戳存储；
- 在数据库中查询`TIMESTAMP`字段时，将根据MYSQL设定的时区获取时间字符串；
- Django默认从数据库读取的时间为UTC时间，再根据`TIME_ZONE`设定的时区进行转换显示；

解决办法：

- 方法一：关闭Django的`USE_TZ`
- 方法二：确保Django读取的时间是UTC时间


