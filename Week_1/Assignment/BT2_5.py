students = {
    23110096: {"diem": {"Lap trinh win": 7.0, "Ly 2": 4.0, "Lap trinh web": 7.0, "Lap trinh C": 4.5}},
    23110012: {"diem": {"Lap trinh win": 8.5, "Ly 2": 6.0, "Lap trinh web": 9.0, "Lap trinh C": 7.5}},
    23110025: {"diem": {"Lap trinh win": 5.0, "Ly 2": 5.5, "Lap trinh web": 6.0, "Lap trinh C": 4.0}},
    23110123: {"diem": {"Lap trinh win": 7.0, "Ly 2": 8.0, "Lap trinh web": 6.5, "Lap trinh C": 7.5}},
    23110234: {"diem": {"Lap trinh win": 9.0, "Ly 2": 9.5, "Lap trinh web": 8.5, "Lap trinh C": 9.0}},
    23110345: {"diem": {"Lap trinh win": 3.5, "Ly 2": 4.0, "Lap trinh web": 5.0, "Lap trinh C": 5.5}},
    23110456: {"diem": {"Lap trinh win": 6.5, "Ly 2": 7.0, "Lap trinh web": 6.0, "Lap trinh C": 6.0}},
}



def check(target):
    sv = students.get(target)
    if sv is None:
        print("Ko tim thay ma so sinh vien: ", target)
    else:
        ds_diem = sv["diem"]
        print(ds_diem)
        
        print(f"Các môn sinh viên {target} còn nợ là: ")
        #.items() giúp ta duyệt được các key-value của dict
        #.keys() de duyet key, .values() de duyet value
        for mon, diem in ds_diem.items():
            if diem < 5:
                print(f"  {mon}: {diem}")
                
target = int(input("Nhập vào mã số sinh viên cần kiểm tra: "))
check(target)
            
