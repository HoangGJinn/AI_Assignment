import numpy as np
import random, math
# a = np.array([random.randint(0, 50) for _ in range(20)])

n, m = 3, 4
rng = np.random.default_rng(42) #seed
#random int array
a = rng.integers(0, 100, size=(n, m))
print(a)
print("Gia tri lon nhat cua array la: ",a.max())
# max(0) return max values of columns of 2D array
print("Cac gia tri lon nhat cua cac column la: ", a.max(0))
# max(1) return max values of rows of 2D array
print("Cac gia tri lon nhat cua cac row la: ", a.max(1))
