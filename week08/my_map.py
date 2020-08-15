from typing import Callable, Iterable, Iterator


def my_map(function, *iters,) -> Iterator:
    '''
    返回一个将 function 应用于 iterable 中每一项并输出其结果的迭代器。 如果传入了额外的 iterable 参数，function 必须接受相同个数的实参并被应用于从所有可迭代对象中并行获取的项。 当有多个可迭代对象时，最短的可迭代对象耗尽则整个迭代就将结束。
    '''
    # 将输入的多个可迭代对象的元素组合成function的输入参数
    # zip对象的长度等于iters中最短的可迭代对象长度
    args = zip(*iters)
    while True:
        try:
            yield func(*next(args))
        except StopIteration as _:
            break
    return 


if __name__ == '__main__':
    func = lambda *args: sum(args)
    print('输入1个可迭代对象：')
    m1 = map(func, range(10))
    m2 = my_map(func, range(10))
    print(f'map: {list(m1)}')
    print(f'map: {list(m2)}')
    print('输入多个可迭代对象：')
    m3 = map(func, range(10), range(5), range(10))
    m4 = my_map(func, range(10), range(5), range(10))
    print(f'map: {list(m3)}')
    print(f'map: {list(m4)}')

