# Backlog – Thư viện mini (theo TVM-SRS-001 v1.0)

| Đợt | Task | Nội dung | Yêu cầu, quy tắc |
| --- | --- | --- | --- |
| 1 | T-01.1 | Hàm chuẩn hoá và kiểm tra ISBN | BR-01 |
| 1 | T-01.2 | Service thêm sách, route và màn hình MH-03 | FR-01, BR-07 |
| 1 | T-02.1 | Service danh sách sách: phân trang 20, tìm kiếm, số bản còn | FR-02, BR-07, 4.3 |
| 1 | T-02.2 | Route và màn hình MH-02 | FR-02 |
| 1 | T-04.1 | Service thêm độc giả: sinh mã thẻ, chuẩn hoá email | FR-04, BR-08 |
| 1 | T-04.2 | Route và màn hình MH-04 | FR-04 |
| 2 | T-06.1 | Hàm tính phí trễ hạn | BR-05 |
| 2 | T-05.1 | Service tạo phiếu mượn trong một giao dịch | FR-05, BR-02, BR-03, BR-04, BR-07, NFR-04 |
| 2 | T-05.2 | Route và màn hình MH-05 | FR-05 |
| 2 | T-06.2 | Service trả sách, route và màn hình MH-06 | FR-06 |
| 3 | T-07.1 | Danh sách phiếu quá hạn và màn hình MH-07 | FR-07, BR-03 |
| 3 | T-03.1 | Sửa, xoá đầu sách | FR-03, BR-06 |
| 3 | T-08.1 | Đăng nhập, đăng xuất, bảo vệ route | FR-08 |
| 3 | T-08.2 | Khoá tài khoản sau 5 lần sai, hết phiên sau 30 phút | NFR-11, NFR-12 |
| 3 | T-08.3 | Lệnh `flask create-librarian` tạo tài khoản thủ thư | FR-08, 2.2 |
| 3 | T-09.1 | Nhật ký lỗi, nghiệp vụ, đăng nhập và địa chỉ /health | SF-02 đến SF-06 |

## Mẫu issue

[T-06.1] Hàm tính phí trễ hạn
Yêu cầu: BR-05; dữ liệu kiểm thử: kịch bản "Tính phí trễ hạn" của FR-06 (SRS 3.1)
Mô tả: tinh_phi_tre(han_tra, ngay_tra) -> (so_ngay_tre, tien_phat) trong app/services/phi.py
Tiêu chí xong:
- [ ] 6 trường hợp trong bảng Examples của SRS đều có test và xanh
- [ ] Thêm test biên trễ 19 và 21 ngày
- [ ] Không dùng float, không gọi date.today()
File dự kiến: app/services/phi.py, tests/unit/test_phi.py