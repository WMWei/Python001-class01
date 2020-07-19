import pandas as pd


def select(df: pd.DataFrame, cols: list=None, limit: int=None):
    '''
    1. SELECT * FROM data;
    2. SELECT * FROM data LIMIT 10;
    3. SELECT id FROM data;
    '''
    print('-' * 10)
    if cols:
        print(df.loc[:limit, cols])
    else:
        print(df[:limit])


def count(df: pd.DataFrame, cols: list):
    '''
    4. SELECT COUNT(id) FROM data;
    '''
    print('-' * 10)
    print(df[cols].count())


def query(df: pd.DataFrame, query_str: str):
    '''
    5. SELECT * FROM data WHERE id<1000 AND age>30;
    '''
    print('-' * 10)
    print(df.query(expr=query_str))


def group_count(df: pd.DataFrame, group_col: str, count_col: str):
    '''
    6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
    '''
    print('-' * 10)
    print(df.groupby(group_col)[count_col].nunique())


def join(df: pd.DataFrame, other: pd.DataFrame, df_key: str, other_key: str):
    '''
    7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
    '''
    print('-' * 10)
    print(df.set_index(df_key).join(other.set_index(other_key),
                                    how='inner',
                                    lsuffix='_left',
                                    rsuffix='_right'))


def union(df: pd.DataFrame, other: pd.DataFrame):
    '''
    8. SELECT * FROM table1 UNION SELECT * FROM table2;
    '''
    print('-' * 10)
    print(pd.concat([df, other], ignore_index=True))


def delete_rows(df: pd.DataFrame, query_str: str):
    '''
    9. DELETE FROM table1 WHERE id=10;
    '''
    print('-' * 10)
    delete_indexs = df.query(expr=query_str).index
    print(df.drop(delete_indexs))

def drop_columns(df: pd.DataFrame, cols: list):
    '''
    10. ALTER TABLE table1 DROP COLUMN column_name;
    '''
    print('-' * 10)
    print(df.drop(cols, axis=1))


if __name__ == '__main__':
    df1 = pd.DataFrame({
        'A': range(4),
        'B': range(2, 6),
        'C': range(4, 8),
        'D': range(6, 10)
    })

    df2 = pd.DataFrame({
        'A': range(1, 5),
        'B': range(1, 5),
        'C': range(1, 5),
        'D': range(1, 5)
    })
    select(df1)
    select(df1, limit=3)
    select(df1, cols=['A', 'B'])
    count(df1, ['A'])
    query(df1, 'A > 2 and B < 6')
    group_count(df1, 'A', 'B')
    join(df1, df2, 'A', 'A')
    union(df1, df2)
    delete_rows(df1, 'A > 2 and B < 6')
    drop_columns(df1, ['C', 'D'], )