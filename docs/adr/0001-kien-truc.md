# ADR-0001: Kiến trúc phân lớp và các quyết định kỹ thuật nền tảng

- **Trạng thái:** Đề xuất (chờ chốt 1 trong 2 phương án)
- **Ngày:** 2026-11-24
- **Căn cứ:** `docs/srs.md` (`TVM-SRS-001`, phiên bản 1.0)

## 1. Bối cảnh

Hệ thống Thư viện mini là ứng dụng web nội bộ phục vụ thủ thư (quy mô dưới 5.000 đầu sách, tối đa 2 thủ thư thao tác đồng thời), phát triển bằng Python 3.12, Flask, SQLAlchemy, Jinja và SQLite (mục 2.2, 3.2.3).

Kiến trúc cần đồng thời thoả mãn các ràng buộc chính trong SRS:

- **Phân lớp và kiểm thử (`NFR-15`, mục `3.3.5`):** Tách 3 lớp giao diện – nghiệp vụ – dữ liệu; độ phủ kiểm thử tầng nghiệp vụ đạt từ 70% trở lên; mỗi quy tắc nghiệp vụ (`BR-01` đến `BR-08`) đều có kiểm thử đơn vị.
- **Toàn vẹn dữ liệu và đồng thời (`NFR-03`, `NFR-04`, `DB-01`..`DB-05`):** Tạo/trả phiếu nguyên tử trong một giao dịch; không để số bản còn bị âm khi 2 thủ thư cùng mượn bản cuối; khai báo ràng buộc khoá ngoại, duy nhất, bắt buộc ở cả mức CSDL (`DB-02`); quản lý cấu trúc CSDL bằng tệp migration có phiên bản (`DB-05`).
- **Thời gian và múi giờ (`2.2`, `BR-03`, `BR-05`, `NFR-11`, `NFR-12`, `4.3`):** Cố định múi giờ Việt Nam (`UTC+7`); kiểm thử được cả ngày hiện tại lẫn thời gian hết hạn phiên (30 phút) và khoá tài khoản (5 phút) bằng đồng hồ giả lập.
- **Xử lý lỗi và bản địa hoá (`3.1`, `SF-01`, `3.2.1`, `4.3`):** Hiển thị lỗi nhập liệu tiếng Việt ngay cạnh từng ô bị sai (giữ nguyên dữ liệu đã nhập), đồng thời đặt tập trung văn bản giao diện tách khỏi mã xử lý.
- **Bảo mật và truy vết (`2.2`, `NFR-08`, `NFR-10`, `SF-04`, `SF-05`):** Băm mật khẩu bằng `bcrypt` hoặc `PBKDF2`; mọi biểu mẫu có mã chống CSRF; hỗ trợ cả giao diện web lẫn lệnh quản trị `flask create-librarian`; ghi nhật ký nghiệp vụ gắn với tài khoản thủ thư.

## 2. Tóm tắt so sánh 2 phương án

<!-- Sau khi chọn phương án ở Mục 3, bạn có thể giữ bảng này làm lịch sử cân nhắc hoặc xoá nếu muốn ADR gọn hơn -->

| Tiêu chí | Option 1: Độc lập Flask (`SQLAlchemy` thuần + `Alembic`) | Option 2: Hệ sinh thái Flask (`Flask-SQLAlchemy` + Tách `rules` thuần) |
| --- | --- | --- |
| Mức tách biệt với Flask | `services` và `models` hoàn toàn không phụ thuộc Flask | Chỉ nhóm hàm `rules` thuần độc lập Flask; `services` chạm CSDL cần `app_context` |
| Kiểm thử đơn vị & tích hợp | Unit test `services` chạy trực tiếp với SQLite `:memory:` không cần tạo Flask app | Unit test `rules` không cần Flask; test `services` có truy vấn CSDL chạy qua fixture Flask app |
| Khối lượng cấu hình ban đầu | Cao hơn một chút (tự gắn vòng đời `Session` vào Flask và cấu hình `Alembic`) | Thấp, quen thuộc trong hệ sinh thái Flask (`Flask-SQLAlchemy` + `Flask-Migrate`) |
| Độ khớp với chữ viết trong SRS | Bám sát mục `2.2` và `3.2.3` (`SQLAlchemy` thuần) và mục tiêu tách hẳn Flask khỏi `services` | Thực dụng cho dự án nhỏ (`NFR-16`), vẫn đạt `NFR-15` nhờ tách lớp quy tắc thuần |

---

## 3. Quyết định và Hệ quả

<!-- HƯỚNG DẪN CHỌN THỦ CÔNG: Giữ lại MỘT khối (OPTION 1 hoặc OPTION 2) bên dưới, xoá khối còn lại và xoá dòng hướng dẫn này. -->


<!-- ==================== BẮT ĐẦU OPTION 2 ==================== -->
### [OPTION 2] Kiến trúc 3 lớp theo hệ sinh thái Flask (Flask-SQLAlchemy + Tách lõi quy tắc thuần)

#### Luồng phụ thuộc

- **Tầng giao diện & điểm vào (`app/routes/`, `app/cli.py`, `app/templates/`):** Nhận HTTP request / lệnh CLI, kiểm tra CSRF, quản lý phiên đăng nhập, lấy thời gian từ bộ cấp thời gian `Clock` (`UTC+7`), truyền tham số tường minh xuống `app/services/`.
- **Tầng nghiệp vụ (`app/services/`):** Chia làm 2 phần rõ rệt:
  - `app/services/rules.py`: Các hàm kiểm tra và tính toán thuần không chạm CSDL (`BR-01` ISBN, `BR-03` hạn trả & quá hạn, `BR-05` phí trễ, `BR-08` định dạng/chuẩn hoá email & sinh mã thẻ) — không phụ thuộc Flask hay CSDL.
  - `app/services/*_service.py`: Các ca sử dụng điều phối truy vấn và giao dịch qua `db.session` (`BR-02`, `BR-04`, `BR-06`, `BR-07`, ghi nhật ký `SF-04`), không truy cập trực tiếp `request` hay `session` của HTTP.
- **Tầng dữ liệu (`app/models/`, `migrations/`):** Dùng `Flask-SQLAlchemy` khai báo bảng kèm ràng buộc mức CSDL (`DB-02`, bật kiểm tra khoá ngoại cho SQLite) và `Flask-Migrate` để quản lý migration có phiên bản (`DB-05`).

#### Bảng quyết định chi tiết

| Quyết định | Lựa chọn | Căn cứ trong SRS |
| --- | --- | --- |
| **Kiến trúc** | 3 lớp: `(routes, cli)` (giao diện/điểm vào) → `services` (`*_service` + `rules` thuần) → `models` (dữ liệu) | `2.2`, `NFR-15`, `SF-04` |
| **Nơi đặt quy tắc BR** | Quy tắc tính toán thuần đặt tại `app/services/rules.py` (không phụ thuộc Flask/DB); quy tắc phụ thuộc trạng thái đặt tại `app/services/*_service.py`; ràng buộc toàn vẹn dữ liệu khai báo đồng thời ở `app/models/` và CSDL | `3.3.5`, `NFR-15`, `DB-02`, `4.1` |
| **Quản lý giao dịch** | Mỗi thao tác ghi ở `*_service.py` thực hiện trọn vẹn trong một giao dịch của `db.session` (bật `BEGIN IMMEDIATE` trên SQLite khi lập phiếu mượn để chống mượn trùng bản cuối), lỗi giữa chừng tự động `rollback` | `NFR-03`, `NFR-04` |
| **Thời gian hiện tại** | Dùng bộ cấp thời gian `Clock` cố định múi giờ `UTC+7` (có thể thay thế khi test); `routes` truyền `hom_nay` (và thời điểm hiện tại cho phiên/khoá đăng nhập) xuống `services`, không gọi `date.today()` | `2.2`, `BR-03`, `BR-05`, `NFR-11`, `NFR-12`, `4.3` |
| **Báo lỗi nghiệp vụ** | Ngoại lệ `LoiNghiepVu` chứa danh sách lỗi có cấu trúc `(ten_truong, ma_loi, tham_so)`; câu thông báo tiếng Việt trong SRS đặt tập trung tại `app/messages.py` để hiển thị cạnh đúng ô nhập liệu hoặc vùng lỗi chung | `3.1`, `3.2.1`, `SF-01`, `4.3` |
| **Thư viện** | `Flask`, `Flask-SQLAlchemy`, `Flask-Migrate` (migration), `Flask-WTF` (chỉ dùng `CSRFProtect`), `Werkzeug` (cố định băm `pbkdf2:sha256`), `pytest`, `pytest-cov`, `ruff`, `pip-audit` | `2.2`, `NFR-08`, `NFR-10`, `DB-05` |

#### Hệ quả

- **Ưu điểm:**
  - Cấu hình gọn nhẹ, quen thuộc, ít mã khung nhất cho quy mô dự án nhỏ (`NFR-16`), có sẵn lệnh quản lý migration qua `Flask-Migrate`.
  - Toàn bộ công thức nghiệp vụ cốt lõi trong `rules.py` vẫn unit test độc lập không cần Flask; các ca sử dụng có CSDL kiểm thử dễ dàng bằng fixture ứng dụng Flask với SQLite `:memory:`.
- **Đánh đổi:**
  - Các hàm trong `*_service.py` có thao tác CSDL vẫn cần chạy trong `app.app_context()` của Flask khi viết kiểm thử.
<!-- ==================== KẾT THÚC OPTION 2 ==================== -->
