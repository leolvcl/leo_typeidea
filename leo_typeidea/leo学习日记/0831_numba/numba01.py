from numba import jit
import time

t1 = time.clock()
@jit
def add_num(a, b):
    count = 0
    for i in range(a, b):
        count += 1
    return count

count = add_num(1,500000000)
tt = time.clock() - t1
print('和为{}，用时{}s'.format(count, tt))


