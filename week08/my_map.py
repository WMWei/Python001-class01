from typing import Callable, Iterable, Iterator


def my_map(function: Callable, *iters: Iterable,) -> Iterator:
    '''
    返回一个将 function 应用于 iterable 中每一项并输出其结果的迭代器。 如果传入了额外的 iterable 参数，function 必须接受相同个数的实参并被应用于从所有可迭代对象中并行获取的项。 当有多个可迭代对象时，最短的可迭代对象耗尽则整个迭代就将结束。
    '''
    for iter_ in iters:
        if not hasattr(iter_, '__iter__'):
            raise TypeError(f'The element of iters must be iterable, '
                            f'"{iter_.__class__.__name__}" is not iterable')
    # 将输入的多个可迭代对象的元素组合成function的输入参数
    # zip对象的长度等于iters中最短的可迭代对象长度
    args = zip(*iters)
    while True:
        try:
            yield func(*next(args))
        except StopIteration as _:
            return


if __name__ == '__main__':
    func = lambda *args: sum(args)
    print('输入1个可迭代对象：')
    m1 = map(func, range(10))
    m2 = my_map(func, range(10))
    print(f'map: {list(m1)}')
    print(f'my_map: {list(m2)}')
    print('输入多个不等长可迭代对象：')
    m3 = map(func, range(10), range(5), range(10))
    m4 = my_map(func, range(10), range(5), range(10))
    print(f'map: {list(m3)}')
    print(f'my_map: {list(m4)}')
    print('输入多个等长可迭代对象：')
    ins = (range(10) for _ in range(3))
    ins2 = (range(10) for _ in range(3))
    m5 = map(func, *ins)
    m6 = my_map(func, *ins2)
    print(f'map: {list(m5)}')
    print(f'my_map: {list(m6)}')
    print('输入为非可迭代对象：')
    try:
        m5 = map(func, 3, 5, 6)
        print(list(m5))
    except Exception as e:
        print(f'map: {e}')
    try:
        m6 = my_map(func, 3, 4, 5)
        print(list(m6))
    except Exception as e:
        print(f'my_map: {e}')
    

