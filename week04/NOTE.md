# Week04 笔记

本周主要学习数据清洗所需要用到的相关库的使用方法，包括：

- pandas
- numpy
- jieba
- snownlp

## 1. numpy

`NumPy`是一个基础数学库，为`pandas`提供高效的数值计算支持

例子：

```python
import numpy as np

# 数值
a = 1
# 二维向量
vector2 = np.array([1, 1])
vector2.shape
# (2,)
# 向量计算
vector3 = np.array([2, 2])
vector4 = vector3 + vector2
# [3, 3]
# 三维向量
vector5 = np.array([1, 1, 1])
vector5.shape
# (3,)

# 矩阵
mm1 = np.array([[12, 0], [4, 0], [3, 0]])
mm2 = np.array([[0, 0], [0, 0], [0, 0]])
mm1.shape
# (3, 2)
# 矩阵计算
mm3 = mm1 - mm2
# [[12, 0], [4, 0], [3, 0]]
# 曼哈顿距离
linalg.norm(mm1-mm2, 1)
# 19
# 欧几里得距离
linalg.norm(mm1-mm2, 2)
# 13
```



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

### 1.3 输出和绘图

- pandas提供丰富的方法将`DataFrame`数据输出到文档，包括`df.to_csv`、`df.to_excel`、`df.pickle`等
- 利用`matplotlib.pyplot`，可以将`DataFrame`数据绘制成图像
- 利用`seaborn`库丰富图例

例子：

- 输出到excel（需要xlwt包）（读取excel需要xlrd）

  ```python
  import pandas as pd
  import numpy as np
  
  df.to_excel(
  	excel_writer=r'file.xlsx',  # 导出的文档
  	sheet_name='sheet1',		# 设置sheet页名字
  	index=False,				# 设置在导出时把索引去掉
  	columns=['col1', 'col2']	# 设置要导出的列
  )
  # 其他可用参数
  # 缺失值处理（这里将缺失值设置为0）
  # na_rep=0
  # 无穷值处理
  # inf_rep=0
  # 字符编码
  # encoding='utf-8'
  
  
  ```

  

- 绘图

  ```python
  import pandas as pd
  import numpy as np
  import matplotlib.pypolt as plt
  import seaborn as sns
  
  # 生成日期索引序列
  dates = pd.date_range('20200101', periods=12)
  # 一些参数
  # start, end指定开始结束
  # periods指定索引个数
  # freq指定时间间隔，如'5H'设置间隔5小时
  # tz指定时区
  # closed指定是否包含边界点，默认None全包含
  
  # 利用np.random.randn()产生随机数矩阵
  df = pd.DataFrame(np.random.randn(12, 4), index=dates, columns=list('ABCD'))
  
  # 绘图
  # 格式设置
  plt.plot(df.index, 
           df['A'],
           color='#FFAA00',  # 颜色
           linestyle='--',   # 线条类型
           linewidth=3,      # 线条宽度
           marker='D',       # 点标记
          )
  # 展示
  plt.show()
  # 绘制散点图
  plt.scatter(df.index, df['A'])
  # 美化图像
  sns.set_style('darkgrid')
  plt.show()
  
  
  ```

  

## 2. jieba：分词和关键词提取

利用第三方库`jieba`，可以对字符串进行分词，常常用于爬虫结果的关键词提取，用于后续分析

例子：

- 分词
  - 精确模式，试图将句子最精确地切开，适合文本分析；
  - 全模式，把句子中所有的可以成词的词语都扫描出来, 速度非常快，但是不能解决歧义；
  - 搜索引擎模式，在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词。
  - paddle模式，利用PaddlePaddle深度学习框架，训练序列标注（双向GRU）网络模型实现分词。同时支持词性标注

```python
import jieba
import os.path

strings = '极客大学的Python进阶训练营真好玩'
# 默认精确模式分词
default_res = jieba.cut(strings, cut_all=False)
# ['极客', '大学', '的', 'python', '进阶', '训练营', '真好玩']
# 返回的是生成器
# jieba.lcut()直接返回分词列表

#全模式
all_res = jieba.cut(strings, cut_all=True)
# ['极', '客', '大学', '的', 'python', '进阶', '训练', '训练营', '真好', '真好玩', '好玩']

# 对于未登录词，采用HMM模型，通过viterbi算法进行启发式搜索来进行分词
viterbi_res = jieba.cut('钟南山院士接受采访新冠不会二次暴发', cut_all=False)
# ['钟南山', '院士', '接受', '采访', '新冠', '不会', '二次', '暴发']
# 关闭HMM
viterbi_res = jieba.cut('钟南山院士接受采访新冠不会二次暴发', HMM=False)
# ['钟南山', '院士', '接受', '采访', '新', '冠', '不会', '二次', '暴发']

# 搜索引擎模式
result = jieba.cut_for_search('小明硕士毕业于中国科学院计算所，后在日本京都大学深造')
# ['小明', '硕士', '毕业', '于', '中国', '科学', '学院', '科学院', '中国科学院', '计算', '计算所', '，', '后', '在', '日本', '京 都', '大学', '日本京都大学', '深造']

# 手动从文件添加词典
userdict = os.path.join(
	os.path.dirname(os.path.abspath(__file__)),
	'extra_dict/user_dict.txt',
)
# Python进阶训练营 3 nt  词语 词频 词性
jieba.load_userdict(userdict)

# 动态添加词典
jieba.add_word('极客大学')
# 动态删除词典
jieba.del_world('极客大学')


strings2 = '我们中出了一个叛徒'
res1 = jieba.cut(strings2, HMM=False)
# ['我们', '中', '出', '了', '一个', '叛徒']
# 分词合并
jieba.suggest_freq('中出', True)
res3 = jieba.cut(strings2, HMM=False)
# ['我们', '中出', '了', '一个', '叛徒']
# 分开分词
jieba.suggest_freq(('中', '出'), True)
res2 = jieba.cut(strings2, HMM=False)
# ['我们', '中', '出', '了', '一个', '叛徒']
# 自定义的词频在HMM开启时可能无效
```

- 关键词提取

```python
import jieba.analyse
import os.path
# 关键词抽取
text = '机器学习，需要一定的数学基础，需要掌握的数学基础知识特别多，如果从头到尾开始学，估计大部分人来不及，我建议先学习最基础的数学知识'
# tfidf算法，经常使用的提取关键词的算法
tfidf = jieba.analyse.extract_tags(text,
                                   topK=5,  # 抽取权重最高的topK个关键词
                                   withWeight=True,  # 是否显示权重
                                  )
# [('数学', 0.6293657596000001), ('学习', 0.5502018873247619), ('数学知识', 0.5192831132571429), ('基础知识', 0.4862761046619048), ('从头到尾', 0.4538680856909523)]
# TextRank算法
textrank = jieba.analyse.textrank(text,
                                  topK=5,
                                  withWeight=False,
                                 )
# ['需要', '基础', '数学', '学习', '掌握']

# 对于分析不准确的场景，手动添加忽略的词
# 配置忽略词文本文件
stop_words = os.path.join(
	os.path.dirname(os.path.abspath(__file__)),
    'extra_dict/stop_words.txt',  # 文本文件中，每个屏蔽词为一行
)
jieba.analyse.set_stop_words(stop_words)
textrank = jieba.analyse.textrank(text,
                                  topK=5,
                                  withWeight=False,
                                 )
# ['学习', '基础', '建议', '估计', '数学']
```

- 参考：[jieba词性标注表](https://www.jianshu.com/p/866e16794e9f)

## 3. snownlp：情感倾向分析

```python
from snownlp import SnowNLP
from snownlp import seg

text = '其实故事本来真的只值三星当初的中篇就足够了但是啊看到最后我又一次被东野叔的反战思想打动了所以就加多一星吧'
s = SnowNLP(text)

# 1 中文分词
s.words

# 2 词性标注 (隐马尔可夫模型)
list(s.tags)

# 3 情感分析（朴素贝叶斯分类器）
s.sentiments
text2 = '这本书烂透了'
s2 = SnowNLP(text2)
s2.sentiments

# 4 拼音（Trie树）
s.pinyin

# 5 繁体转简体
text3 = '後面這些是繁體字'
s3 = SnowNLP(text3)
s3.han

# 6 提取关键字
s.keywords(limit=5)

# 7 信息衡量
s.tf # 词频越大越重要
s.idf # 包含此条的文档越少，n越小，idf越大，说明词条t越重要

# 8 训练
seg.train('data.txt')
seg.save('seg.marshal')
# 修改snownlp/seg/__init__.py的 data_path 指向新的模型即可
```

