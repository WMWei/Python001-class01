import pandas as pd
import matplotlib.pyplot as plt

import settings
from database import connect_mongo


# 解析工资字符串
def parser_salary(salary_str: str, mode: str='max') -> int or float:
    if not salary_str:
        return None
    min_s, max_s = map(lambda x: int(x.lower().replace('k', '000')), salary_str.split('-'))
    if mode == 'min':
        return min_s
    if mode == 'mean':
        return (max_s + min_s) >> 1
    else:
        return max_s


# 获取薪资分布表
def get_salary_map() -> pd.DataFrame:
    db_client = connect_mongo()
    db_post = db_client[settings.MONGODB_DB][settings.MONGODB_COLNAME]
    positions = db_post.find({}, {'_id': 0})
    positions_df = pd.DataFrame(positions)
    positions_df['max'] = positions_df['salary'].map(parser_salary)
    positions_df['min'] = positions_df['salary'].map(
        lambda x: parser_salary(x, 'min')
        )
    positions_df['mean'] = positions_df['salary'].map(
        lambda x: parser_salary(x, 'mean'))
    salary_map = positions_df.dropna().groupby('city').aggregate({
        'max': 'max',
        'min': 'min',
        'mean': 'mean',
    })
    
    return salary_map


# 为直方图矩形添加数值
def add_labels(rects: 'matplotlib.container.BarContainer'):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2,
                 height,
                 height,
                 ha='center',
                 va='bottom')

def salary_show():
    salary_map = get_salary_map()
    width = 0.35

    # 画布尺寸
    plt.figure(figsize=(10, 6))
    # y轴名
    plt.ylabel('工资（元/月）', fontsize=14)
    # x轴名
    plt.xlabel('城市', fontsize=14)
    # 标题
    plt.title('各大城市的python工程师工资分布', fontsize=20)
    p_max = plt.bar(
        salary_map.index,
        salary_map['max'], 
        width, 
        # bottom=salary_map['mean'].round(1),
        color='#6495ED', 
        )
    p_mean = plt.bar(
        salary_map.index,
        # 舍入到个位
        salary_map['mean'].round(0), 
        width, 
        # bottom=salary_map['min'],
        color='#BDB76B', 
        )
    p_min = plt.bar(
        salary_map.index,
        salary_map['min'], 
        width, 
        color='#B22222', 
        )
    add_labels(p_max)
    add_labels(p_mean)
    add_labels(p_min)
    # 设置图示
    plt.legend((p_max[0], p_mean[0], p_min[0]), ('Max', 'Mean', 'Min'))
    # 用来正常显示中文标签
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 用来正常显示负号
    plt.rcParams['axes.unicode_minus'] = False
    plt.show()


if __name__ == '__main__':
    salary_show()

