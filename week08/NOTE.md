# week08学习笔记

本周学习了Python的一些高级特性，包括：

xxx



## 1. 内置数据类型分类

- 按存放类型分类：

  - 容器类型：能存放不太类型的数据，存放的是包含任意类型对象的引用（如：`list`，`tuple`，`collections.queue`，`dict`等）
  - 扁平类型：只能存放同一基础类型数据，存放的是值，是一段连续的内存（如：`array.array`，`str`，`bytes`）

- 按能否被修改分类：

  - 可变类型：`list`，`array.array`，`collections.queue`，`dict`；
  - 不可变类型：`tuple`，`str`，`bytes`;

  > `tuple`的相对不可变性：`tuple`的不可变是指其数据结构的物理内容（保存的引用）不变，元素引用所绑定的对象可能是可变的；

- 按照是否有序：

  - 序列
  - 非序列



## 2. 深拷贝与浅拷贝

### 变量与对象

通过别名共享对象：python的变量是引用式变量，可以理解为只是对象的别名/引用，是对对象的绑定；

赋值操作右边先行：对象在变量赋值前就已经创建；（通过`dis.dis()`函数查看相应语句字节码，可以了解执行细节）

对象的三个属性：标识、类型和值

- 标识也就是对象的id，是唯一数值标注，在对象的生命周期内不会变化；（类似于对象在内存中的地址）
- `id()`可以获得对象标识；
- `==`比较的是对象的值；
- `is`比较的是对象的标识；

### 深拷贝与浅拷贝

python的容器对象的元素保存的都是对象的引用，基于此前提，在对象拷贝时，需要考虑深拷贝、浅拷贝问题；

浅拷贝：只复制对象最外层的容器

- 大部分赋值操作都是浅拷贝，如`[:]`，`a = list(b)`等
- 浅拷贝的好处：在其元素都是不可变类型的前提下，不会引起问题，还能节省内存；（`tuple`除外）
- 存在问题：若元素为可变对象，对副本元素的操作会影响复制源对象；

深拷贝：副本不共享内部对象的引用；

`copy`模块：

- `copy.copy(x)`提供浅复制；
- `copy.deepcopy(x)`提供深复制；



## 3. 字典与相关数据类型扩展



### 字典与散列表

字典有着高效的查找和更新性能，散列表是其如此高效的原因；

字典内部使用一个称为散列表的数据结构：

- 散列表是一个稀疏数组（总是有空白元素的数组），其每一个元素称之为表元；
- 字典的散列表中，每一个键值对占用一个表元，表元有两个部分，一个是对键的引用，一个是对值的引用；
- 表元的大小是一致的，因此可以通过偏移量来读取表元；（类似列表通过索引读取元素）
- 读取字典元素时：
  - 通过散列函数，计算键的散列值，取散列值中的几位与表元偏移量对应；
  - 找到相应表元，若表元为空，则`KeyError`异常；
  - 否则比较查找键与表元键是否相等，相等则返回相应值；
  - 若不相等，则发生散列冲突，重新获取散列值的几位数字进行新一轮查找；
- 存储字典元素：流程与读取元素类似；

基于内部的散列表结构，字典的键必须是可散列的：

- 生命周期其散列值不变；
- 不同对象散列值不同；
- 相同对象散列值相同；

可散列的数据类型：

- 一般不可变数据类型都是可散列的（`Tuple`视其元素而定，必须满足所有元素都是可散列的）；
- 用户自定义对象一般都是可散列的，散列值为`id()`；

### 字典相关数据类型

`collections`模块提供了许多集合数据类型的拓展：

- `collections.namedtuple`：命名元组，将元素与属性绑定，如`collections.namedtuple('Card', ['rank', 'suit'])`
- `collections.deque`：双向队列，类似列表，最大区别在于可以使用`d.popleft()`和`d.appendleft()`
- `collections.Counter`：计数字典，`collections.Counter('acdade')`



### 魔术方法`__sub__`

在对象中定义`__sub__`方法进行运算符重载，能够让对象支持`-`操作；

>  在python中，使用`__`+方法名+`__`来标记魔术方法。
>
> 魔术方法是python自身构建模块的接口，通过魔术方法，能够激活对象的一些基本操作，**使得自定义对象能够表现得和内置数据类型一样**，支持相应的操作，如：迭代、运算符重载、管理上下文等；
>
> 魔术方法使得python中针对不同对象的一些标准操作变得统一；



## 4. 函数

### 函数与对象

python中一切皆对象，函数也是对象：

- `func()`调用函数，传递的是函数的返回值
- `func`直接传递的函数对象本身

通过实现`__call__`魔术方法，能够让对象成为可调用对象；



### 变量作用域

作用域的LEGB原则:

- L Local：函数内部命名空间；
- E Enclosing function local：外部嵌套函数的命名空间；
- G Global：函数所在模块命名空间；
- B Builtin：内置模块命名空间；

python访问变量时，按照LEGB顺序查找变量；

变量按作用域分类：

- 局部变量：python不需要声明变量，默认在函数内部中赋值的变量为局部变量 => 对应L 作用域；
- 全局变量：在模块内绑定的变量，模块内所有作用域都能访问 => G 作用域；
- 自由变量：未在函数的Local作用域绑定的变量 => E 作用域；

对于函数内部来说，全局变量、自由变量都可以直接访问，但是若要赋值，则需要在内部进行声明：

- `global`声明全局变量；
- `nolocal`声明自由变量；

### 函数参数

- 定义参数顺序：位置>默认>可变>限定关键字>（可变）关键字；（`def func(a, b=None, *c, d, e=None, **f)`；
- 理论上，`func(*args, **kwargs)`可以定义一切函数；
  - `*args`：接受不定长参数，存储为元组传入函数；函数内可以通过索引、遍历取出参数值；
  - `**kwargs`：接受不定长的关键字参数，存储为字典传入函数，函数内部通过关键字获取参数值；

### 类型标注

由于Python是动态语言，解释器在运行时不会检查类型，即使参数类型不对，解释器也不会抛出任何异常。

以上特性导致在使用函数时，使用者不清楚函数需要的参数类型，很容易传错参数。

因此，python提供了类型标注来对参数和返回值进行解释说明（python3.6后，对变量也能进行类型标注）

- 使用冒号 `:` 加类型名来代表参数的类型；
- 使用箭头 `->` 加类型表示返回值的类型；

类型标注主要起到提示作用，实际执行时解释器会忽略这部分，也不会对进行类型检查。

### 匿名函数

语法：`lambda 参数: 返回值`

匿名函数一般用作只使用一次的临时函数；



### 高阶函数

高阶函数：接收函数对象作为输入/输出函数对象的函数；

python中常见高阶函数：

- `map(func, iter)`：返回一个将`func`应用于`iter`中每一项并输出其结果的迭代器；也可以接受多个iter参数，此时func必须接受相同个数的参数；
- `functools.reduce(func, iter)`：将两个参数的`func`从左至右积累地应用到`iter`的条目，以便将该可迭代对象缩减为单一的值。`func`第一个参数代表累计值，第二各参数是来自`iter`的更新值；
- `filter(func, iter)`：`func`接收`iter`中的每一项并进行判断，返回`bool`值；`filter`返回`iter`中经`func`处理判断为`True`的元素组成的迭代器；
- `functools.partial(*func*, */*, **args*, ***keywords*)`：返回一个偏函数，其相当于原函数`func`部分参数被固定的函数；

## 5. 闭包和装饰器

### 闭包

闭包：闭包是一种函数，它保留函数定义时对自由变量（外部函数的变量）的绑定。在调用时，虽然定义的作用域不可用，但仍可以使用那些绑定；

闭包只在函数嵌套时出现；

```python
a = 1  # 全局变量


def decorator():
    b = 1  # 对于wrapper属于自由变量
    def wrapper(*args, **kwargs):  # 闭包
        global a  # 当需要赋值时，要声明全局变量
        nolocal b # 当需要赋值时，需要声明自由变量
        a += 1
        b += 1
        print(a, b)
    return wrapper


func = decorator()
func()  # 在执行func()时，decorator()已执行完毕，本地作用域已经不存在，b作为自由变量存在
```

### 装饰器

概念：装饰器是可调用对象，输入函数对象，对其进行处理，并输出该函数对象或替换成新函数；

作用：动态的给函数增加额外职责；

实现：装饰器通过闭包实现；

```python
import time


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(f'cost time: {time.time() - start}s')
        return res


@timer  # @xxx是Python中使用装饰器的语法糖
def func1():  # 相当于func1 = timer(func1)
    pass
```



装饰器何时执行：在被装饰函数定义后立即执行，通常是模块加载时；

多个装饰器执行顺序：从下到上

```python
@a
@b
def func():  # func = a(b(func))
    pass
```

带参数的装饰器：

```python
def comment(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(func.__name__ * n)
            retrun func(*args, **kwargs)
        return weapper
    return decorator


@comment(4)
def func(x, y):  # 相当于func=comment(3)(func)
    pass
```

类装饰器：

```python
import time


class Timer:
    def __init__(self, func):
        self.func = func
    
    def __call__(self, *args, **kwargs):
        start = time.time()
        res = self.func(*args, **kwargs)
        print(time.time() - start)
        return res

 
@Timer
def func():  # 相当于func = Timer(func)
    pass

func()  # 调用func实际调用的是Timer实例的__call__方法
```

### 标准库中的装饰器

`functools.wraps`：

- 普通装饰器，实际将原函数替换为了新函数，原函数的`__name__`和`__doc__`属性无法获取；
- `@functools.wraps(func)`将原函数的`__name__`和`__doc__`属性复制到新函数；

`functools.lru_cache`：

- 作用：对被装饰函数的相应处理结构进行备忘记录，避免重复运算；

- 应用：如对于递归函数的优化；

`dataclasses.dataclass`：[参考](https://docs.python.org/zh-cn/3/library/dataclasses.html#module-level-decorators-classes-and-functions)

- `dataclasses`模块提供了一个装饰器和一些函数，用于自动添加生成的一些魔术方法，如`__init__`

- ``@``dataclasses.``dataclass`(***, *init=True*, *repr=True*, *eq=True*, *order=False*, *unsafe_hash=False*, *frozen=False*)` 

  - 装饰器检查并找到具有**类型标注的类变量**，基于这些类变量，生成相应的魔术方法，包括`__init__`、`__repr__`等；

  - 字段顺序以类变量的定义顺序为准；

  - 例子：

    ```python
    from dataclasses import dataclass
    
    
    @dataclass
    calss InventoryItem:
        name: str
        unit_price: float
        quantity_on_head: int=0
        # 等价于
        # def __init__(self, name: str, unit_price: float, quantity_on_head: int=0):
            # self.name = name
        	# self.unit_price = unit_price
        	# self.quantity_on_head = quantity_on_head
        
       	def total_cost(self) -> float:
            return self.unit_price * self.quantity_on_hand
        
    ```

    

## 可迭代对象、迭代器和生成器

可迭代对象：简单的理解就是可以通过循环遍历其元素的对象，如常见的`list`、`dict`等；
迭代器：用于从集合中**取出**元素，为可迭代对象提供支持；
生成器：用于“凭空”**生成**元素，python中生成器完全实现了迭代器接口，因此所有生成器都是迭代器；

### 可迭代对象能够被遍历的原因

解释器需要迭代对象x时，会自动调用`iter(x)`；
`iter(x)`作用：

- 检查对象是否实现了`__iter__`方法，调用`__iter__`获得**迭代器**；
- 若无`__iter__`，检查对象是否实现了`__getitem__`方法，若存在，则解释器自动创建**迭代器**，并通过`__getitem__`方法读取元素；
- 若上述都尝试失败，则抛出`TypeError`，即该对象不是可迭代对象；

也就是说，在python中，如果实现了`__iter__`方法获得**迭代器对象**，那么该对象就是可迭代的；

### 标准迭代器

要构造标准的迭代器对象，需要实现两个方法：`__next__`和`__iter__`：

- 实现无参数的`__next__`方法，通过`next()`的调用，返回下一个可用元素，以支持迭代功能；若没有元素，则抛出`StopIteration`；
- 实现`__iter__`方法，返回迭代器对象本身，以便在可以使用可迭代对象的地方，也能使用迭代器；

### 可迭代对象与迭代器关系

- python从可迭代对象获取迭代器；
- 迭代器可用作为可迭代对象使用；
- 可迭代对象实现的`__iter__`方法每次返回都是新的迭代器 => 对象可以支持多次迭代；
- 迭代器对象实现的`__iter__`方法返回迭代器本身 => 对象的迭代是一次性的；

### 标准生成器函数

只要函数的定义体中又`yield`参数，该函数就是生成器函数；

- 调用生成器函数，返回生成器对象，包装生成器函数的定义体；
- python中生成器实现了迭代器接口，因此生成器就是迭代器；
- 把生成器对象传入`next()`函数，每次调用，生成器函数会向前执行到下一个`yield`语句，返回**产出值**，然后暂停；
- 最终函数体返回时抛出`StopIteraton`；（和迭代器行为一致）

生成器表达式：类似列表推导式，将`[]`改为`()`，就是生成器表达式；
生成器表达式是python提供的语法糖，相比定义生成器函数更加便利：

- 生成器表达式语法简洁，无需先定义函数再调用；
- 生成器函数更加灵活，能够实现相对更复杂的逻辑；
- 生成器函数方便重用；

生成器作用：一种惰性获取数据项的方式，按需一次获取一个数据项，节省内存；
