import numba
import numpy as np
import time
t1 = time.clock()

@numba.jit(nopython=True, parallel=True)
def logistic_regression(Y, X, w, iterations):
    for i in range(iterations):
        # numpy.dot(): 返回的是两个数组的点积
        # numpy.exp()：返回e的幂次方，e是一个常数为2.71828
        w -= np.dot(((1.0 / (1.0 + np.exp(-Y * np.dot(X, w))) - 1.0) * Y), X)
    return w
X = list(range(11))
Y = list(range(11))
w = 10
iterations = 10
re_w = logistic_regression(X, Y, w, iterations)
t = time.clock() - t1
print('使用numba：结果为{}，用时{}s'.format(re_w, t))