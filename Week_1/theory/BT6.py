import numpy as np

matrix = [[11, 10, 9, 7, 8, 14, 12],
          [15, 12, 7, 20, 4, 9, 13]]

a = np.array(matrix)  # chuyển list 2D thành mảng NumPy (shape = (2, 7))
maxCostofDays = 0
maxCostofSession = 0
days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
sessions = ["Morning", "Afternoon"]
cntMorning = 0
cntAfternoon = 0
for col in range(a.shape[1]):  # a.shape[1] = số cột = 7
    if a[0,col] > a[1,col]:
        cntMorning += 1
    else:
        cntAfternoon += 1
    costofDay = a[0][col] + a[1][col]  # cộng 2 phần tử cùng cột: hàng 0 và hàng 1
    if costofDay > maxCostofDays:  # cập nhật giá trị lớn nhất
        maxCostofDays = costofDay
        day = days[col]
    for row in range(a.shape[0]):
        if maxCostofSession < a[row][col]:
            maxCostofSession = a[row][col]
            session = sessions[row]
            dayofSession = days[col]
print("1) Ngay ban duoc nhieu nhat tuan la: {0} duoc {1}$".format(day, maxCostofDays))
print("2) Buoi ban duoc nhieu nhat tuan la: buoi {0} ngay {1} duoc {2}$".format(session, dayofSession, maxCostofSession))
if cntMorning > cntAfternoon:
    print("3) Buoi sang ban duoc nhieu hon")
elif cntMorning == 3 and cntAfternoon == 3:
    print("3) Ca hai buoi deu ban nhu nhau")
else:
    print("3) Buoi chieu ban duoc nhieu hon")

