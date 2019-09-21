import functools
import time

CACHE = {}

def cache_it(func):
    @functools.wraps(func)  # 保留被装饰函数的所有属性
    def inner(*args, **kwargs):
        key = repr(*args, **kwargs)
        print(func.__name__)
        try:
            result = CACHE[key]
        except KeyError:
            result = func(*args, **kwargs)
            CACHE[key] = result
        return result
    return inner

@cache_it
def query(sql):
    time.sleep(1)
    result = 'execute %s' % sql
    CACHE[sql] = result

if __name__ == '__main__':
    start = time.time()
    query('SELECT * FROM blog_post')
    print(time.time() - start)

    start = time.time()
    query('SELECT * FROM blog_post')
    print(time.time() - start)