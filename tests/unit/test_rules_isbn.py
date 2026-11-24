"""Unit test độc lập cho quy tắc chuẩn hoá và kiểm tra ISBN (FR-01 mục 3.1, BR-01 mục 3.3.5).

Không khởi tạo Flask app; bao phủ toàn bộ bảng Examples của FR-01 và các trường hợp biên
của BR-01 (độ dài 9, 10, 11, 13, 14 ký tự; ký tự X ở cuối và vị trí khác; có dấu gạch).
"""

from __future__ import annotations

from app.services.isbn import chuan_hoa_isbn, la_isbn_hop_le


def test_br01_chuan_hoa_isbn_bo_dau_gach_ngang() -> None:
    """BR-01, mục 4.1: Loại bỏ dấu gạch ngang để lưu chuẩn không dấu gạch."""
    assert chuan_hoa_isbn("978-604-123-456-7") == "9786041234567"
    assert chuan_hoa_isbn("0-306-40615-X") == "030640615X"


def test_fr01_br01_bien_13_chu_so_hop_le() -> None:
    """FR-01 (Thêm sách hợp lệ), BR-01 (biên 13 ký tự): ISBN gồm 13 chữ số hợp lệ."""
    assert la_isbn_hop_le("9786041234567") is True


def test_br01_isbn_co_dau_gach_ngang_hop_le() -> None:
    """BR-01 (biên có dấu gạch): Dấu gạch được bỏ trước khi kiểm tra độ dài và ký tự."""
    assert la_isbn_hop_le("978-604-123-456-7") is True
    assert la_isbn_hop_le("0-306-40615-2") is True


def test_br01_bien_10_chu_so_hop_le() -> None:
    """BR-01 (biên 10 ký tự): ISBN gồm 10 chữ số hợp lệ."""
    assert la_isbn_hop_le("0306406152") is True


def test_br01_bien_10_ky_tu_x_o_vi_tri_cuoi_hop_le() -> None:
    """BR-01 (biên 10 ký tự, X ở vị trí cuối): 9 chữ số đầu và ký tự cuối là X hợp lệ."""
    assert la_isbn_hop_le("030640615X") is True
    assert la_isbn_hop_le("0-306-40615-X") is True


def test_fr01_br01_examples_12345_khong_hop_le() -> None:
    """FR-01 Examples #1: Chuỗi '12345' không đủ độ dài ISBN."""
    assert la_isbn_hop_le("12345") is False


def test_fr01_br01_examples_978604123456x_khong_hop_le() -> None:
    """FR-01 Examples #2: Chuỗi 13 ký tự kết thúc bằng X ('978604123456X') không hợp lệ."""
    assert la_isbn_hop_le("978604123456X") is False


def test_fr01_br01_examples_bien_14_chu_so_khong_hop_le() -> None:
    """FR-01 Examples #3, BR-01 (biên 14 ký tự): Chuỗi 14 chữ số không hợp lệ."""
    assert la_isbn_hop_le("97860412345678") is False


def test_br01_bien_9_chu_so_khong_hop_le() -> None:
    """BR-01 (biên 9 ký tự): Chuỗi 9 chữ số sát dưới mốc 10 không hợp lệ."""
    assert la_isbn_hop_le("123456789") is False


def test_br01_bien_11_chu_so_khong_hop_le() -> None:
    """BR-01 (biên 11 ký tự): Chuỗi 11 chữ số nằm giữa mốc 10 và 13 không hợp lệ."""
    assert la_isbn_hop_le("12345678901") is False


def test_br01_ky_tu_x_o_vi_tri_khac_cuoi_khong_hop_le() -> None:
    """BR-01 (biên X ở vị trí khác): Ký tự X nằm ở đầu hoặc giữa chuỗi 10/13 ký tự không hợp lệ."""
    assert la_isbn_hop_le("X306406152") is False
    assert la_isbn_hop_le("03064X6152") is False
    assert la_isbn_hop_le("978604X234567") is False


def test_br01_chuoi_rong_hoac_chua_ky_tu_khong_phai_so_khong_hop_le() -> None:
    """BR-01: Chuỗi rỗng, toàn dấu gạch hoặc chứa chữ cái khác không hợp lệ."""
    assert la_isbn_hop_le("") is False
    assert la_isbn_hop_le("---") is False
    assert la_isbn_hop_le("978604123456A") is False
