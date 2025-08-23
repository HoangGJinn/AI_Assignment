import numpy as np 

a = np.array([-2, 6, 3, 10, 15, 48])
print (a)
#1D a[start:stop:step]
#2D A[r_start:r_stop, c_start:c_stop]
#slice can't print the value at stop index
# step: the stride between selected indices (default 1)
print(a[2:5:2])
print(a[1:6:2])
print(a[-3:]) # or print(a[3:])
print(a[-1:-4:-1])