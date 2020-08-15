import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(f'cost time: {time.time() - start}s')
        return res
    return wrapper


@timer
def my_sum(arrs: 'list[int]') -> int:
    res = 0
    for i in arrs:
        time.sleep(1)
        res += i
    return res


if __name__ == '__main__':
    l1 = list(range(11))
    print(f'sum({l1}): {my_sum(l1)}')