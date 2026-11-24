"""Quy tắc chuẩn hoá và kiểm tra ISBN thuần (BR-01, FR-01, NFR-15).

Module này tuyệt đối không import Flask hay models để đảm bảo unit test độc lập.
"""

from __future__ import annotations


def _la_chu_so_ascii(chuoi: str) -> bool:
    """Kiểm tra chuỗi không rỗng chỉ gồm các chữ số ASCII 0-9."""
    return chuoi.isascii() and chuoi.isdigit()


def chuan_hoa_isbn(isbn: str) -> str:
    """Loại bỏ dấu gạch ngang khỏi chuỗi ISBN trước khi kiểm tra và lưu trữ (BR-01, mục 4.1)."""
    return isbn.replace("-", "")


def la_isbn_hop_le(isbn: str) -> bool:
    """Kiểm tra ISBN hợp lệ theo BR-01 (13 chữ số, hoặc 9 chữ số đầu + chữ số/X ở cuối)."""
    da_chuan_hoa = chuan_hoa_isbn(isbn)
    if len(da_chuan_hoa) == 13:
        return _la_chu_so_ascii(da_chuan_hoa)
    if len(da_chuan_hoa) == 10:
        return _la_chu_so_ascii(da_chuan_hoa[:9]) and (
            _la_chu_so_ascii(da_chuan_hoa[9]) or da_chuan_hoa[9] == "X"
        )
    return False
