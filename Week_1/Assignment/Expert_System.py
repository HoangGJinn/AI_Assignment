#He chuyen gia quyen dinh xem la co nen lam bai tap hay khong?

def decide(deadline: float, free_time: int, mood: str):
    if deadline <= 1:
        return ("Làm liền đi ông",
                "Hạn chót chỉ còn một ngày thôi cho dù ông có lười nhé!")

    if deadline <= 3:
        if free_time >= 45:
            if mood == "Tốt" or mood == "Bình thường":
                return ("Nên bắt đầu làm từ từ",
                        "Hạn chót còn 3 ngày, ông có thời gian và tâm trạng cũng ổn.")
            else:
                return ("Cố gắng làm ít nhất một phần",
                        "ông có thời gian nhưng hơi lười, tranh thủ làm phần dễ trước.")
        else:
            return ("Làm một phần nhỏ thôi",
                    "Hạn chót còn 3 ngày nhưng không có đủ thời gian nên làm phần nhỏ/dàn ý ngay.")

    if deadline <= 7:
        if free_time >= 30:
            if mood == "Tốt":
                return ("Tranh thủ làm sớm nhé để thời gian cho môn khác",
                        "Còn 1 tuần, tâm trạng tốt, có thời gian nên làm sớm để đỡ áp lực.")
            else:
                return ("Có thể làm nhẹ nhàng như coi sơ qua các bài, câu hỏi",
                        "Còn 1 tuần, ông có thời gian nhưng tâm trạng chưa tốt nên cứ thong thả.")
        else:
            return ("Chưa cần gấp",
                    "Còn 1 tuần, thời gian rảnh ít nên ông có thể nghỉ ngơi rồi lên kế hoạch sau, hoặc làm việc khác quan trọng.")

    if deadline > 7:
        if mood == "Tốt" or mood == "Bình thường":
            return ("ông có thể làm môn này hoặc là làm các môn sắp tới hạn nhé!",
                    "Deadline còn xa nhưng ông đang trong trạng thái tuyệt vời")
        else:
            return ("Nghỉ đi rồi làm gì làm nhé",
                    "Deadline còn xa, ông có thời gian nhưng tâm trạng chưa tốt.")
    else:
        return ("Hoãn lại cũng được",
                "Deadline còn xa và thời gian rảnh quá ít.")


if __name__ == '__main__':
    print("Tui sẽ giúp ông quyết định là ông có nên làm bài tập bây giờ không?")
    try:
        dd = float(input("ông còn bao nhiêu ngày nữa tới hạn nộp? "))
        free_time = int(input("ông sẽ rảnh trong bao lâu? "))
        mood = input("Tâm trạng hiện tại của ông như thế nào (Tốt/ Bình thường/ Lười): ")
    except Exception as e:
        print("ông nhập ko đúng yêu cầu, nhập lại nhé", e)
        exit(1)

    decision, why = decide(dd, free_time, mood)
    print("Quyết định: ", decision)
    print("Lý do: ", why)