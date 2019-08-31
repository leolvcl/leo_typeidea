from numba import jit
import random
import time

t1 = time.clock()
def monte_carlo_pi(n):
    tmp_a = 0
    for i in range(n):
        x = random.random()
        y = random.random()
        if (x ** 2 + y ** 2) < 1.0:
            tmp_a += 1
    return 4.0 * tmp_a / n

count1 = monte_carlo_pi(100)
tt1 = time.clock() - t1
print('不使用numba：和为{}，用时{}s'.format(count1, tt1))

t2 = time.clock()
@jit(nopython=True)
def monte_carlo_pi(n):
    tmp_a = 0
    for i in range(n):
        x = random.random()
        y = random.random()
        if (x ** 2 + y ** 2) < 1.0:
            tmp_a += 1
    return 4.0 * tmp_a / n

count2 = monte_carlo_pi(100)
tt2 = time.clock() - t1
print('使用numba和为{}，用时{}s'.format(count2, tt2))