# week07学习笔记

## 类与对象

### 类属性与对象属性

### 类属性作用域

### 实例方法、类方法与静态方法

### 属性描述符

### 继承

### 元类

## 几种设计模式

### 单例模式

单例模式：个人理解就是一个类只允许实现一个实例
三种实现单例模式的方式：

```python
# 装饰器
def singleton(cls):
    instance = {}
    def getinstance(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    return getinstance

@singleton
class Foo:
    pass

# 利用__new__构造
# __new__是类中的静态构造方法，在类实例化时，首先执行__new__构造实例，在执行__init__初始化实例

class Singleton:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

if __name__ == '__main__':
    s1 = Singleton()
    s2 = Singleton()
    assert id(s1) == id(s2)

# 在并发条件下，__new__实现单例模式并不是线程安全的，需要加锁
# 双检查模式（不是很理解）
import threading
class Singleton(object):
    objs = {}
    objs_locker = threading.Lock()
    def __new__(cls, *args, **kargs):
        if cls in cls.objs:
            return cls.objs[cls]
        cls.objs_locker.acquire()
        try:
            if cls in cls.objs: ## double check locking
                return cls.objs[cls]
            cls.objs[cls] = object.__new__(cls)
        finally:
            cls.objs_locker.release()
# 两小问题：
# ·如果Singleton的子类重载了__new__()方法，会覆盖或者干扰Singleton类中__new__()的执行 => 子类化Singleton的时候，务必记得调用父类的__new__()方法
# ·如果子类有__init__()方法，那么每次实例化的时候，
# __init__()都会被调用到，__init__()只应该在创建实例的时候被调用一次。 => 可以通过偷偷地替换掉__init__()方法来确保它只调用一次。


# python的导入模块天生就是单例模式
# 所有的变量都会绑定到模块。
# ·模块只初始化一次。
# ·import机制是线程安全的（保证了在并发状态下模块也只有一个实例）。(不理解)
```

### 工厂模式

### mixin模式
