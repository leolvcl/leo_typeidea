import time

CACHE = {}

# def query(sql):  # 开销更大
#     try:
#         result = CACHE[sql]
#     except KeyError:
#         time.sleep(1)
#         result = 'execute %s' %sql
#         CACHE[sql] = result

def query(sql):
    result = CACHE.get(sql)
    if not result:
        time.sleep(1)
        result = 'execute %s' % sql
        CACHE[sql] = result
    return result

if __name__ == '__main__':
    start = time.time()
    query('SELECT * FROM blog_post')
    print(time.time() - start)

    start = time.time()
    query('SELECT * FROM blog_post')
    print(time.time() - start)