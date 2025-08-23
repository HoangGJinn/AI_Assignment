from math import *

print("Nhập x (độ) vào để tính cos(x) nhé: ", end = "")
x_do = float(input())
# chuyen tu do -> rad
x = radians(x_do)

def cosX(x, eps=1e-12):
    term = 1.0
    s = term
    for i in range(1, 100):
        #Đây là công thức truy hồi
        term *= -x*x / ((2*i - 1)*(2*i))
        s += term
        if abs(term) < eps:
            break
    return s
        
    
print(f"cos({x_do}) = {cosX(x):.11f}")