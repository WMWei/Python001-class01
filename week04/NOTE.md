# Week04 笔记

本周主要学习数据清洗所需要用到的相关库的使用方法，包括：

- pandas
- numpy
- jieba
- snownlp

## 1. pandas

`pandas`（pd）是一个基于`NumPy`（np）开发的数据分析库，提供了快速、简捷、易懂的数据结构，简化了数据整理步骤。pandas能更方便的操作大型数据集，很适合用来对爬虫获取的基础进行清洗，获得结构化的数据供数据分析等项目使用。
`NumPy`是一个基础数学库，为`pandas`提供高效的数值计算支持，配合`matplotlib`（plt）可用实现可视化功能。

### 1.1 pandas数据类型

`pandas`中有两个重要的数据类型：`Series`、`DataFrame`

- `Series`：类似一维数组，是`DataFrame`的基础
  - 基本操作：

  ```python
  import pandas as pd


  # 创建Series
  # 基于列表创建
  # 自动创建索引index
  s1 = pd.Series(['a', 'b', 'c'])
  # 通过字典创建，带索引
  s2 = pd.Series({'a':11, 'b':22, 'c':33})
  # 通过关键字设置索引
  s3 = pd.Series([11, 22, 33], index = ['a', 'b', 'c'])
  # 获取全部索引
  s1.index
  # 获取全部值
  s1.values
  # 使用index会提升查询性能
  #    如果index唯一，pandas会使用哈希表优化，查询性能为O(1)
  #    如果index有序不唯一，pandas会使用二分查找算法，查询性能为O(logN)
  #    如果index完全随机，每次查询都要扫全表，查询性能为O(N)

  # 一些有用的函数
  # Series.map(self, arg, na_action=None)，
  # 根据输入的映射关系（如字典、函数）
  # 将Series的值映射为新的值
  # 创建新的Series

  emails = pd.Series(['abc at amazom.com', 'admin1@163.com', 'mat@m.at', 'ab@abc.com'])
  import re
  pattern ='[A-Za-z0-9._]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,5}'
  mask = emails.map(lambda x: bool(re.match(pattern, x)))
  emails[mask]
  ```

- `DataFrame`：类似多维数组
  - `DataFrame`支持多种方式创建：
  
  ```python
  import pandas as pd
  # 一维列表 => df的一列数据（column）
  df1 = pd.DataFrame(['a', 'b', 'c', 'd'])
  # 二维列表 => df的多行（index）
  df2 = pd.DataFrame([
                     ['a', 'b'],
                     ['c', 'd']
                    ])
  # 基于字典创建 => df的多列（column）
  df3 = pd.DataFrame({
        'A': range(1, 5),
        'B': range(1, 5),
        'C': range(1, 5),
        'D': range(1, 5)
    })
    # 列名可以
    # 通过字典创建定义
    # 通过DataFrame的columns关键字指定
    # 另外单独指定columns属性
    df2.columns= ['one', 'two']

    # 索引df.index类似

    # 另外，还可以从文件中读取
    df4 = pd.read_csv('xxx.csv')
  ```

### 1.2 pandas数据处理

pandas提供丰富的方法读取和处理`DataFrame`的数据

- 数据预处理：主要是处理缺失值和重复值

```python
import pandas as pd
import numpy as np

x = pd.Series([ 1, 2, np.nan, 3, 4, 5, 6, np.nan, 8])
#检验序列中是否存在缺失值
x.hasnans
# 将缺失值填充为平均值
x.fillna(value = x.mean())

# 前向填充缺失值
df3=pd.DataFrame({"A":[5,3,None,4],
                  "B":[None,2,4,3],
                  "C":[4,3,8,5],
                  "D":[5,4,2,None]})

df3.isnull().sum() # 查看缺失值汇总
df3.ffill() # 用上一行填充
df3.ffill(axis=1)  # 用前一列填充

# 缺失值删除
df3.info()
df3.dropna()

# 填充缺失值
df3.fillna('无')

# 重复值处理
df3.drop_duplicates()
```

- 数据调整：筛选数据、结构化处理等
- 数值计算和聚合操作：如count、sum、group等，与数据库的操作类似
- 多表拼接和关联：类似数据库的join、union等

### 1.3 绘图

## 2. jieba：分词和关键词提取

## 3. snownlp：情感倾向分析
