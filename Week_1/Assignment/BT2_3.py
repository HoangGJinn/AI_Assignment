import math
n = 0
def choose(n):
    while True:
        try:
            n = int(input("Bạn muốn giải ptr bậc 1 hay 2?: "))
                
            match n:
                case 1:
                    print("Bạn đã chọn giải phương trình ax + b, hãy nhập giá 2 trị a và b: ")
                    a = int(input("Nhap vao gia tri a: "))
                    b = int(input("Nhap vao gia tri b: "))
                    return 1, a, b, None
                case 2:
                    print("Bạn đã chọn giải phương trình ax^2 + bx + c, hãy nhập 3 giá trị a, b và c: ")
                    a = int(input("Nhap vao gia tri a: "))
                    b = int(input("Nhap vao gia tri b: "))
                    c = int(input("Nhap vao gia tri c: "))
                    return 2, a, b, c
                case _:
                    raise ValueError("Lựa chọn không hợp lệ (chỉ 1 hoặc 2)")
        except ValueError as e:
            print(e, "- Hãy nhập lại nhé!")


type, a, b, c = choose(n)

if type==1:
    if a==0:
        if b==0:
            print("Phương trình có vô số nghiệm")
        else:
            print("Phương trình vô nghiệm")
    else:
        print(f"Phương trình có nghiệm x = -{b}/{a} = ", -b/a)
else:
    if a == 0:
        # bx + c = 0
        if b == 0:
            print("Vô số nghiệm" if c == 0 else "Vô nghiệm")
        else:
            print("Nghiệm duy nhất x =", -c/b)
    else:
        delta = b*b - 4*a*c
        if delta > 0:
            x1 = (-b - math.sqrt(delta))/(2*a)
            x2 = (-b + math.sqrt(delta))/(2*a)
            print("2 nghiệm phân biệt:", x1, x2)
        elif delta == 0:
            print("Nghiệm kép:", -b/(2*a))
        else:
            print("Vô nghiệm (trong ℝ)")
    

