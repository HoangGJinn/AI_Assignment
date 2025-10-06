# AI_Assignment

# Báo cáo Đồ án Cá nhân Trí tuệ Nhân tạo

## Đề tài: Giải bài toán **8-Queens (8 quân hậu)** bằng các thuật toán tìm kiếm

Giảng viên hướng dẫn: **TS Phan Thị Huyền Trang**
Sinh viên thực hiện: **Nguyễn Hoàng Giáp – 23110096**
Ngày báo cáo: *Tháng 10 năm 2025 (Học Kì I)*

---

## 1. Mục tiêu

Mục tiêu của dự án là xây dựng một **ứng dụng mô phỏng trực quan** việc giải bài toán **8-Queens** (đặt 8 quân hậu trên bàn cờ 8×8 sao cho không quân nào tấn công nhau) bằng cách áp dụng và **so sánh hiệu quả** của nhiều **thuật toán tìm kiếm** trong Trí tuệ Nhân tạo (AI).

Ứng dụng cung cấp giao diện Tkinter để:
- Chọn thuật toán và **quan sát quá trình đặt hậu từng bước** (animate).
- Xem **log chi tiết** (đường đi, chi phí/heuristic, xác suất chấp nhận, tiến hoá…).
- **So sánh** hành vi giữa các nhóm thuật toán (blind, informed, local, đặc biệt).

**Mô hình hoá bài toán:**
- **Trạng thái (State):** Một bàn cờ 8×8, biểu diễn bằng ma trận 0/1 (1 là vị trí có hậu).
- **Hành động (Action):** Đặt một hậu vào một ô hợp lệ ở hàng hiện tại.
- **Môi trường (Environment):** Tập hợp tất cả các trạng thái có thể đạt được từ trạng thái ban đầu bằng cách áp dụng các hành động thỏa ràng buộc.
- **Ràng buộc:** Không có 2 hậu nào cùng hàng, cùng cột, hoặc cùng đường chéo.
- **Trạng thái đích (Goal):** Đặt đủ 8 hậu thoả ràng buộc và **phải thỏa bàn cờ đích** (là bàn cờ bên phải).
- **Chi phí (Step Cost):** Chi phí để thực hiện một hành động.

---

## 2. Nội dung

### 2.1. Các thuật toán **Tìm kiếm không có thông tin** (Uninformed / Blind Search)

**Khái niệm:** Nhóm này tìm kiếm **không dùng heuristic**, chỉ dựa vào cấu trúc không gian tìm kiếm.

**Định nghĩa bài toán 8-Queens theo search:**
- Mỗi bước mở rộng đặt thêm 1 hậu ở **hàng hiện tại** vào cột hợp lệ (*isValid* kiểm tra cột và 2 đường chéo phía trên).  
- Mục tiêu là đặt đủ **8 hậu** (độ sâu lời giải *d* = 8).

**Thuật toán đã triển khai:**
- **BFS (Breadth-First Search):** mở rộng theo **tầng** (row 0 → 1 → …).
- **DFS (Depth-First Search):** đi **sâu** theo một nhánh rồi quay lui.
- **DLS / IDS (Depth-Limited / Iterative Deepening):** giới hạn độ sâu và lặp tăng dần.

**Hình ảnh minh họa**  

**Biểu đồ so sánh hiệu suất** 

**Ưu/nhược điểm & Hiệu suất (trên 8-Queens):**
- **BFS:**  
  - *Ưu:* Đầy đủ; nếu mỗi bước đồng chi phí thì mang tính tối ưu về số bước mở rộng.  
  - *Nhược:* Bộ nhớ lớn (frontier nở nhanh theo b^d).  
- **DFS:**  
  - *Ưu:* Tiết kiệm bộ nhớ; có thể nhanh nếu nhánh “đúng” được duyên.  
  - *Nhược:* Không đảm bảo đầy đủ/tối ưu; dễ lạc vào nhánh sâu.   
- **DLS/IDS:**  
  - *Ưu:* IDS kết hợp ưu thế đầy đủ/tối ưu về độ sâu như BFS với bộ nhớ kiểu DFS; phù hợp khi **không biết trước độ sâu**.  
  - *Nhược:* Lặp lại nút tầng nông nhiều lần (nhưng chi phí thường chấp nhận được).

---

### 2.2. Các thuật toán **Tìm kiếm có thông tin** (Informed Search)

**Khái niệm:** Sử dụng **heuristic** để ước lượng “mức xung đột” hoặc “độ gần tới đích” giúp **hướng** việc mở rộng.
- Heuristic tiêu biểu trong repo: **đếm xung đột** giữa các hậu (*heuristic_cost*). Giá trị càng thấp càng tốt; **0** là cấu hình **hợp lệ hoàn toàn**.

**Thuật toán đã triển khai:**
- **UCS (Uniform-Cost Search):** dùng **chi phí bước đi** dựa trên vị trí để minh hoạ (ví dụ, ưu/nhược về viền – trung tâm).
- **Greedy Best-First:** mở rộng theo trạng thái có **h** nhỏ nhất.
- **A\*:** xét **f = g + h**, trong đó *g* là chi phí tích luỹ (ví dụ *cost_estimate* theo vị trí), *h* là xung đột sau khi đặt.

**Hình ảnh minh họa**  

**Biểu đồ so sánh hiệu suất** 

**Ưu/nhược điểm & Hiệu suất:**
- **UCS:**  
  - *Ưu:* Tối ưu theo **hàm chi phí** thiết kế (nếu chi phí không âm).  
  - *Nhược:* Có thể mở rộng rất nhiều nếu chi phí “cào bằng” hoặc không giúp phân biệt. 
- **Greedy:**  
  - *Ưu:* Nhanh trong nhiều trường hợp vì “lao” theo h nhỏ.  
  - *Nhược:* Không đảm bảo tối ưu hay đầy đủ; dễ kẹt “local minima/plateau”.  
- **A\*:**  
  - *Ưu:* Khi *h* là “admissible/consistent” và *g* thiết kế hợp lý, A\* **tối ưu** theo *f*.  
  - *Nhược:* Tốn bộ nhớ (frontier là hàng đợi ưu tiên lớn).

---

### 2.3. **Tìm kiếm cục bộ** (Local Search)

**Khái niệm:** Làm việc trực tiếp trên **một cấu hình** và tìm **lân cận tốt hơn** theo hàm mục tiêu (số xung đột). Không nhấn mạnh “đường đi”, mà nhắm **một nghiệm** thoả ràng buộc.

**Thuật toán đã triển khai:**
- **Hill Climbing (HC):** chọn lân cận giảm xung đột; dễ kẹt tại **cực trị cục bộ/plateau/ridge**.
- **Simulated Annealing (SA):** cho phép **nhảy lên** (nhận trạng thái xấu hơn) theo xác suất phụ thuộc **nhiệt độ T**, giúp thoát kẹt; repo có **multi-restart**.
- **Beam Search:** giữ **K** ứng viên tốt nhất tại mỗi bước; cân bằng giữa đa dạng và chất lượng.
- **Genetic Algorithm (GA):** mã hoá lời giải theo vector cột; dùng **chọn lọc – lai ghép – đột biến**; có **log tiến hoá** (fitness, xung đột, số cột khớp target).

**Hình ảnh minh họa**  

**Biểu đồ so sánh hiệu suất** 

**Ưu/nhược điểm & Gợi ý dùng:**
- **HC:** Nhanh, ít bộ nhớ; nhưng kẹt cục bộ → nên kết hợp **random restarts**.
- **SA:** Khả năng thoát kẹt tốt; thời gian hội tụ phụ thuộc lịch giảm nhiệt **T0, alpha, Tmin**.  
- **Beam:** Tăng đa dạng so với HC; hiệu quả phụ thuộc **K**.  
- **GA:** Tìm kiếm toàn cục, phù hợp không gian lớn; phải **thiết kế fitness** tốt (ở repo dùng “ít xung đột + thưởng khớp nghiệm đích”).

---

### 2.4. **Tìm kiếm dựa trên ràng buộc** (Constraint-Based / CSP-flavored)

Mặc dù 8-Queens là **CSP kinh điển**, repo minh hoạ các kỹ thuật gần gũi:
- **Backtracking:** quay lui khi bị mâu thuẫn.
- **Forward Checking (ý tưởng):** sau khi gán một biến (đặt một hậu), **cắt tỉa** miền giá trị các biến chưa gán (các cột/chéo bị chiếm). *(Có thể mở rộng trong tương lai)*
- **Constraint Propagation (AC-3 – ý tưởng/mô phỏng):** duy trì nhất quán cung, giúp cắt tỉa mạnh hơn. *(Trong repo, phần cắt tỉa chính nằm ở `isValid` & cấu trúc tìm kiếm theo hàng)*

**Hình ảnh minh họa**  

**Biểu đồ so sánh hiệu suất** 

**Ưu/nhược điểm:**
- **Backtracking:**  
  - *Ưu:* Đơn giản, tìm nghiệm chính xác; có thể tối ưu thêm **MRV/LRV**, **LCV**, **ràng buộc bậc cao**…  
  - *Nhược:* Dễ bùng nổ tổ hợp nếu không cắt tỉa tốt.
- **Forward Checking / Propagation:**  
  - *Ưu:* Giảm mạnh không gian tìm kiếm.  
  - *Nhược:* Tăng chi phí tính toán cục bộ; cần triển khai cẩn thận.

---

### 2.5. **Tìm kiếm trong môi trường đặc biệt**

Repo có 2 phần minh hoạ mở rộng khái niệm “môi trường” (theo giáo trình AI):
- **AND–OR Search (môi trường không xác định):** biểu diễn **kế hoạch** theo OR-nodes (lựa chọn đặt hậu) và AND-nodes (tất cả điều kiện con phải thoả). Kết quả trả về một **cây kế hoạch**; có chức năng **trích xuất path** để animate.
- **Belief-State Search (môi trường không quan sát đầy đủ):** duy trì một **tập trạng thái niềm tin** (ví dụ, một trong số 12 nghiệm chuẩn có thể là đích thật). Mỗi lần đặt hậu **thu hẹp** tập nghiệm có thể (“lọc bằng quan sát”), đến khi belief co lại còn **một nghiệm**.

**Hình ảnh minh họa**  

**Biểu đồ so sánh hiệu suất** 

**Ưu/nhược điểm:**
- **AND–OR:** diễn đạt được các **chiến lược** trong môi trường có nhiều khả năng; tuy nhiên cây kế hoạch phức tạp.  
- **Belief-State:** hữu ích khi **không chắc chắn** trạng thái thực; nhưng **không gian belief** có thể rất lớn.

---

## 3. Kết luận

Dự án đã xây dựng một **nền tảng trực quan** cho 8-Queens, tích hợp đa dạng thuật toán: **blind, informed, local, CSP-flavored, AND–OR, Belief-State**.  
Người dùng có thể:
- **Hiểu cách vận hành** từng thuật toán qua hoạt ảnh đặt hậu.
- **Quan sát log/chi phí/heuristic** và các quyết định (nhận/chối trong SA, tiến hoá GA…).
- **So sánh** hành vi các nhóm thuật toán trong cùng một khung bài toán.

Kết quả: Ứng dụng Python (Tkinter) với mã nguồn rõ ràng (`algorithms.py`, `run_game.py`…), có sẵn **12 nghiệm chuẩn** để **đối chiếu** quá trình tìm kiếm.

---

## 4. Hướng dẫn cài đặt & chạy

### 4.1. Môi trường & thư viện

- Cần **Python 3.x**.
- Phần lớn thư viện **có sẵn** trong Python (collections, heapq, random, math…).  
- **Chỉ cần cài thêm Tkinter!**  

### 4.2. Chạy ứng dụng

- **Giao diện Tkinter** hiển thị:
  - Bàn cờ trái: **animate** đường đi (đặt hậu theo từng bước).
  - Bàn cờ phải: **nghiệm đích** để đối chiếu (lấy từ `twelve_queen_solutions.py`).
  - Cụm **nút thuật toán**: BFS, DFS, UCS, DLS, IDS, Greedy, A\*, Hill Climbing, Simulated Annealing, Genetic, Beam, AND–OR, Belief-State…
  - **Log box**: ghi lại bước đặt hậu / chi phí / heuristic / xác suất SA / tiến hoá GA…
- **Tham số tốc độ** (ms) có thể điều chỉnh ngay trong UI.

---

## 5. Cấu trúc thư mục
```
ASSIGNMENT/
├─ solvers/
│  ├─ __init__.py
│  ├─ common.py
│  ├─ bfs.py      ├─ dfs.py      ├─ ucs.py
│  ├─ dls.py      ├─ greedy.py   ├─ hill_climbing.py
│  ├─ simulated_annealing.py     ├─ genetic.py
│  ├─ beam.py     ├─ and_or.py   ├─ belief.py
│  └─ backtracking.py
├─ run_game.py
├─ twelve_queen_solutions.py
├─ image/                # ảnh/GIF minh hoạ (tuỳ chọn)
├─ requirements.txt
└─ .gitignore (khuyến nghị: .idea/, __pycache__/, tempCodeRunnerFile.py)

```

---

## 6. Nhật ký & Nguồn tham khảo (theo tuần)

- **Week 2:** Các nguồn tổng hợp trên mạng và trong slide bài giảng về 8-Queens, định nghĩa bài toán & ràng buộc.  
- **Week 3:** Cơ sở cài BFS cho 8-Queens, tham khảo:  
  https://www.geeksforgeeks.org/dsa/8-queen-problem *(ý tưởng cơ bản; code trong repo tự triển khai theo mô hình đặt-hàng)*  
- **Week 4:** Phát triển **DFS, UCS, DLS, IDS** dựa trên cơ sở BFS; tham khảo slide chương **Tìm kiếm không thông tin**.  
- **Week 5:** Thêm **Greedy, A\***; bổ sung **Local Search** (*Hill Climbing, Simulated Annealing, Beam, Genetic*).  
- **Week 6:** Thêm **AND–OR** cho môi trường **không xác định** và **Belief-State** cho môi trường **không quan sát đầy đủ**.  
- **Week 7:** Thêm **Search in Partially Observable Environments**, và nhóm thuật toán **ràng buộc** (Backtracking, Forward Checking, Propagation).

> Tham khảo các thuật toán và ý tưởng chính từ cuốn sách **Artificial Intelligence: A Modern Approach (2016)** của tác giả **Stuart J. Russell và Peter Norvig**

---

## 7. Liên kết GitHub
