# Thư viện mini – Hướng dẫn cho trợ lý lập trình

## Dự án
Ứng dụng web nội bộ cho thủ thư quản lý sách, độc giả và mượn – trả sách.
- Đặc tả yêu cầu: `docs/srs.md` (`TVM-SRS-001` v1.0).
- Kiến trúc đã chốt: `docs/adr/0001-kien-truc.md` (Option 2: `Flask-SQLAlchemy` + tách lõi `rules` thuần).
- Truy vết: mọi yêu cầu có mã `FR-xx`, `BR-xx`, `NFR-xx`, `DB-xx`, `SF-xx`; ghi mã liên quan trong docstring, tên test và thông điệp commit.

## Công nghệ
Python 3.12, Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-WTF (chỉ dùng `CSRFProtect`), Werkzeug (băm mật khẩu với `pbkdf2:sha256`), SQLite, Jinja, pytest, pytest-cov, ruff, pip-audit.

## Lệnh
- Cài đặt: `pip install -r requirements.txt`
- Cập nhật CSDL (migration): `flask --app app db upgrade`
- Tạo migration mới: `flask --app app db migrate -m "<mo_ta>"`
- Tạo tài khoản thủ thư: `flask --app app create-librarian`
- Chạy ứng dụng: `flask --app app run --debug`
- Chạy test: `pytest -q`
- Đo độ phủ tầng nghiệp vụ: `pytest --cov=app/services --cov-fail-under=70`
- Kiểm tra mã nguồn & bảo mật gói: `ruff check .` và `pip-audit`

## Kiến trúc
```text
app/routes/, app/cli.py, app/templates/  tầng giao diện & điểm vào (HTTP/CLI, CSRF, phiên đăng nhập, render)
app/services/rules.py                    quy tắc tính toán/kiểm tra thuần, KHÔNG import Flask hay models
app/services/*_service.py                điều phối ca sử dụng, giao dịch db.session và nhật ký SF-04
app/models/, migrations/                 Flask-SQLAlchemy + Flask-Migrate, đúng bảng/cột trong SRS mục 4.1
app/messages.py                          tập trung câu thông báo tiếng Việt đúng nguyên văn SRS (mục 4.3)
```
- **Ranh giới tầng:** `routes` và `cli` không truy vấn CSDL trực tiếp, không chứa quy tắc nghiệp vụ. `*_service.py` không truy cập `flask.request` hay `flask.session` (nhận tường minh dữ liệu đầu vào, thời gian và tài khoản thủ thư từ tầng gọi).
- **Phân bổ quy tắc BR (`3.3.5`, `NFR-15`, `DB-02`):**
  - `app/services/rules.py`: chứa các hàm thuần cho `BR-01` (ISBN), `BR-03` (hạn trả, quá hạn), `BR-05` (phí trễ), `BR-08` (định dạng/chuẩn hoá email, sinh mã thẻ kế tiếp).
  - `app/services/*_service.py`: chứa quy tắc phụ thuộc trạng thái CSDL (`BR-02`, `BR-04`, `BR-06`, `BR-07`).
  - `app/models/`: khai báo đầy đủ ràng buộc `UNIQUE`, `NOT NULL`, `FOREIGN KEY`, `CHECK (so_ban >= 1)` ở mức CSDL (`DB-02`) và bật `PRAGMA foreign_keys=ON` cho mọi kết nối SQLite.
- **Giao dịch & đồng thời (`NFR-03`, `NFR-04`):** Mỗi thao tác ghi ở `*_service.py` thực hiện nguyên tử trong một giao dịch của `db.session`; dùng `BEGIN IMMEDIATE` trên SQLite khi tạo phiếu mượn để chống mượn trùng bản sách cuối; lỗi giữa chừng phải `rollback`.
- **Thời gian (`2.2`, `BR-03`, `BR-05`, `NFR-11`, `NFR-12`, `4.3`):** Dùng bộ cấp thời gian `Clock` cố định múi giờ `UTC+7` (`Asia/Ho_Chi_Minh`, có thể thay bằng đồng hồ giả lập khi test). `routes` lấy thời gian từ `Clock` và truyền `hom_nay: date` (cùng thời điểm hiện tại cho kiểm tra hết hạn phiên 30 phút / khoá đăng nhập 5 phút) xuống `services`.
- **Lỗi nghiệp vụ (`3.1`, `3.2.1`, `SF-01`, `4.3`):** `services` gom các lỗi kiểm tra và `raise LoiNghiepVu` chứa danh sách lỗi có cấu trúc `(ten_truong, ma_loi, tham_so)`. Tầng giao diện ánh xạ qua `app/messages.py` để hiển thị câu tiếng Việt ngay cạnh từng ô bị sai (giữ nguyên dữ liệu đã nhập) hoặc tại vùng lỗi chung.

## Quy ước
- Tên bảng, cột, hàm, biến: tiếng Việt không dấu, `snake_case`, khớp SRS (`sach`, `doc_gia`, `phieu_muon`, `tinh_phi_tre`...).
- Chú thích mã nguồn và văn bản giao diện (trong `app/messages.py`, `app/templates/`): tiếng Việt có dấu, chuẩn UTF-8 (`DB-04`).
- Kiểm thử (`NFR-15`):
  - Mọi hàm trong `rules.py` có unit test độc lập (không khởi tạo Flask app); các hàm trong `*_service.py` test qua fixture ứng dụng Flask với SQLite `:memory:`.
  - Tên test chứa mã `BR`/`FR`/`NFR`, ví dụ `test_br05_tre_20_ngay_cham_muc_tran`.
  - Kiểm tra `LoiNghiepVu` dựa trên `(ten_truong, ma_loi, tham_so)`, không so khớp chuỗi câu thông báo.
- Số bản còn luôn tính động từ các phiếu mở (`ngay_tra IS NULL`), không lưu thành cột riêng (`DB-01`).
- Tiền là số nguyên (`int`, đơn vị đồng), không dùng `float`; hiển thị dạng `15.000 đ`. Ngày lưu chuẩn ISO `YYYY-MM-DD` (`DB-04`), hiển thị `dd/mm/yyyy` (`4.3`).
- Băm mật khẩu bằng `werkzeug.security.generate_password_hash` phải chỉ định rõ `method="pbkdf2:sha256"` (`NFR-08`).
- Mọi thay đổi lược đồ CSDL thực hiện qua tệp migration có phiên bản của `Flask-Migrate` (`DB-05`).

## Điều cấm
- Không thêm thư viện ngoài danh sách ở mục Công nghệ khi chưa hỏi.
- Không sửa, bỏ qua (`skip`/`xfail`) hoặc xoá test để ép test qua.
- Không sửa file ngoài phạm vi task được giao.
- Không làm tính năng ngoài phạm vi SRS mục `1.4` (gửi email/SMS, độc giả tự đăng nhập, đặt trước, gia hạn, thu tiền phạt trên hệ thống, phân quyền nhiều vai trò...).
- Không gọi trực tiếp `date.today()` hay `datetime.now()` trong `routes` và `services` (luôn đi qua `Clock` `UTC+7` hoặc tham số truyền vào).
- Không nhúng cứng câu thông báo tiếng Việt trong `services`; không dùng `WTForms` validators để kiểm tra quy tắc `BR` ở tầng giao diện (`Flask-WTF` chỉ dùng chống CSRF cho mọi biểu mẫu theo `NFR-10`).
- Không nối chuỗi SQL (`NFR-09`); không ghi cứng mật khẩu hoặc khoá bí mật; không ghi mật khẩu vào nhật ký (`SF-05`); không lộ chi tiết kỹ thuật ra trang lỗi người dùng (`SF-02`).
- Không xoá bản ghi phiếu mượn (`DB-03`).
