"""Kiểm thử chức năng Thêm đầu sách [T-01.2] (FR-01, BR-01, BR-07, SF-01, NFR-10, MH-03)."""

from __future__ import annotations

import re

import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from app.models import Sach
from app.services.loi import LoiNghiepVu
from app.services.sach_service import them_sach, tinh_so_ban_con


def _lay_csrf_token(client: FlaskClient, duong_dan: str = "/sach/them") -> str:
    """Lấy mã chống CSRF từ biểu mẫu HTML để gửi POST hợp lệ (NFR-10)."""
    phan_hoi = client.get(duong_dan)
    assert phan_hoi.status_code == 200
    khop = re.search(
        r'name=["\']csrf_token["\'][^>]*value=["\']([^"\']+)["\']',
        phan_hoi.get_data(as_text=True),
    )
    assert khop is not None, "Biểu mẫu thiếu trường ẩn csrf_token"
    return khop.group(1)


def test_fr01_1_br01_br07_them_sach_hop_le_luu_isbn_khong_gach_va_so_ban_con(
    db: SQLAlchemy,
) -> None:
    """FR-01.1, BR-01, BR-07, DB-01: Lưu ISBN bỏ dấu gạch và số bản còn bằng số bản."""
    sach = them_sach(
        isbn="978-604-123-456-7",
        ten="Lập trình Python cơ bản",
        tac_gia="Nguyễn Văn A",
        so_ban=3,
        nam_xb=2026,
    )

    da_luu = db.session.get(Sach, sach.id)
    assert da_luu is not None
    assert da_luu.isbn == "9786041234567"
    assert da_luu.ten == "Lập trình Python cơ bản"
    assert da_luu.tac_gia == "Nguyễn Văn A"
    assert da_luu.nam_xb == 2026
    assert da_luu.so_ban == 3
    assert tinh_so_ban_con(da_luu.id) == 3


def test_fr01_1_br07_bien_so_ban_bang_1_va_nam_xb_de_trong_hop_le(
    db: SQLAlchemy,
) -> None:
    """FR-01, BR-07 (biên so_ban = 1), mục 4.1: Năm xuất bản tuỳ chọn có thể để trống."""
    sach = them_sach(
        isbn="0-306-40615-X",
        ten="Cấu trúc dữ liệu",
        tac_gia="Trần Văn B",
        so_ban=1,
        nam_xb=None,
    )

    assert sach.isbn == "030640615X"
    assert sach.nam_xb is None
    assert sach.so_ban == 1
    assert tinh_so_ban_con(sach.id) == 1


def test_fr01_2_br01_isbn_da_ton_tai_ke_ca_khac_dau_gach_bi_tu_choi(
    db: SQLAlchemy,
) -> None:
    """FR-01.2, BR-01: Từ chối lưu khi ISBN sau chuẩn hoá đã tồn tại, số đầu sách không đổi."""
    them_sach(
        isbn="9786041234567",
        ten="Lập trình Python cơ bản",
        tac_gia="Nguyễn Văn A",
        so_ban=3,
    )

    with pytest.raises(LoiNghiepVu) as thong_tin_loi:
        them_sach(
            isbn="978-604-123-456-7",
            ten="Sách khác cùng ISBN",
            tac_gia="Lê Văn C",
            so_ban=2,
        )

    assert ("isbn", "isbn_da_ton_tai", {}) in thong_tin_loi.value.ds_loi
    assert db.session.query(Sach).count() == 1


@pytest.mark.parametrize(
    "isbn_sai",
    ["12345", "978604123456X", "97860412345678"],
)
def test_fr01_3_br01_examples_isbn_khong_hop_le_bi_tu_choi(
    db: SQLAlchemy,
    isbn_sai: str,
) -> None:
    """FR-01.3, BR-01: Từ chối 3 mẫu ISBN không hợp lệ trong bảng Examples của SRS."""
    with pytest.raises(LoiNghiepVu) as thong_tin_loi:
        them_sach(
            isbn=isbn_sai,
            ten="Sách kiểm thử",
            tac_gia="Nguyễn Văn A",
            so_ban=1,
        )

    assert ("isbn", "isbn_khong_hop_le", {}) in thong_tin_loi.value.ds_loi
    assert db.session.query(Sach).count() == 0


@pytest.mark.parametrize("so_ban_sai", [0, -1])
def test_fr01_4_br07_bien_so_ban_nho_hon_1_bi_tu_choi(
    db: SQLAlchemy,
    so_ban_sai: int,
) -> None:
    """FR-01.4, BR-07 (biên 0, -1): Từ chối lưu khi số bản nhỏ hơn 1."""
    with pytest.raises(LoiNghiepVu) as thong_tin_loi:
        them_sach(
            isbn="9786041234567",
            ten="Lập trình Python cơ bản",
            tac_gia="Nguyễn Văn A",
            so_ban=so_ban_sai,
        )

    assert ("so_ban", "so_ban_khong_hop_le", {}) in thong_tin_loi.value.ds_loi
    assert db.session.query(Sach).count() == 0


def test_fr01_4_sf01_gom_du_loi_khi_thieu_ten_tac_gia_va_so_ban_sai(
    db: SQLAlchemy,
) -> None:
    """FR-01.4, SF-01: Gom đồng thời lỗi cho tất cả các trường bị sai trong một lần gọi."""
    with pytest.raises(LoiNghiepVu) as thong_tin_loi:
        them_sach(
            isbn="9786041234567",
            ten="   ",
            tac_gia="",
            so_ban=0,
        )

    cac_cap_loi = {(truong, ma) for truong, ma, _ in thong_tin_loi.value.ds_loi}
    assert ("ten", "ten_sach_trong") in cac_cap_loi
    assert ("tac_gia", "tac_gia_trong") in cac_cap_loi
    assert ("so_ban", "so_ban_khong_hop_le") in cac_cap_loi
    assert db.session.query(Sach).count() == 0


def test_mh03_get_hien_thi_du_truong_nhap_va_nut_luu_huy(
    app: Flask,
    db: SQLAlchemy,
) -> None:
    """Mục 3.2.1 (MH-03): Trang thêm sách có đủ ô ISBN, tên, tác giả, năm XB, số bản, Lưu, Huỷ."""
    phan_hoi = app.test_client().get("/sach/them")
    assert phan_hoi.status_code == 200

    html = phan_hoi.get_data(as_text=True)
    for ten_o in ("isbn", "ten", "tac_gia", "nam_xb", "so_ban", "csrf_token"):
        assert f'name="{ten_o}"' in html
    assert "Lưu" in html
    assert "Huỷ" in html


def test_fr01_1_post_them_sach_hop_le_luu_csdl_va_hien_thong_bao_thanh_cong(
    app: Flask,
    db: SQLAlchemy,
) -> None:
    """FR-01.1, mục 3.2.1: Gửi biểu mẫu hợp lệ lưu đầu sách và hiện thông báo thành công."""
    client = app.test_client()
    token = _lay_csrf_token(client)

    phan_hoi = client.post(
        "/sach/them",
        data={
            "csrf_token": token,
            "isbn": "9786041234567",
            "ten": "Lập trình Python cơ bản",
            "tac_gia": "Nguyễn Văn A",
            "nam_xb": "2026",
            "so_ban": "3",
        },
        follow_redirects=True,
    )

    assert phan_hoi.status_code == 200
    sach = db.session.query(Sach).filter_by(isbn="9786041234567").one_or_none()
    assert sach is not None
    assert sach.so_ban == 3
    assert tinh_so_ban_con(sach.id) == 3


def test_fr01_2_post_isbn_trung_hien_thi_dung_cau_thong_bao_srs(
    app: Flask,
    db: SQLAlchemy,
) -> None:
    """FR-01.2, SF-01: ISBN trùng hiển thị 'ISBN đã tồn tại' và giữ dữ liệu đã nhập."""
    them_sach(
        isbn="9786041234567",
        ten="Lập trình Python cơ bản",
        tac_gia="Nguyễn Văn A",
        so_ban=3,
    )
    client = app.test_client()
    token = _lay_csrf_token(client)

    phan_hoi = client.post(
        "/sach/them",
        data={
            "csrf_token": token,
            "isbn": "9786041234567",
            "ten": "Nhập môn CNPM",
            "tac_gia": "Trần Thị B",
            "nam_xb": "2025",
            "so_ban": "2",
        },
    )

    html = phan_hoi.get_data(as_text=True)
    assert "ISBN đã tồn tại" in html
    assert "Nhập môn CNPM" in html
    assert db.session.query(Sach).count() == 1


def test_fr01_3_post_isbn_sai_hien_thi_dung_cau_thong_bao_srs(
    app: Flask,
    db: SQLAlchemy,
) -> None:
    """FR-01.3, SF-01: ISBN không thỏa BR-01 hiển thị 'ISBN không hợp lệ' và giữ dữ liệu nhập."""
    client = app.test_client()
    token = _lay_csrf_token(client)

    phan_hoi = client.post(
        "/sach/them",
        data={
            "csrf_token": token,
            "isbn": "12345",
            "ten": "Nhập môn CNPM",
            "tac_gia": "Trần Thị B",
            "nam_xb": "",
            "so_ban": "2",
        },
    )

    html = phan_hoi.get_data(as_text=True)
    assert "ISBN không hợp lệ" in html
    assert "12345" in html
    assert "Nhập môn CNPM" in html
    assert db.session.query(Sach).count() == 0


def test_fr01_4_sf01_post_thieu_truong_va_so_ban_sai_giu_nguyen_du_lieu_nhap(
    app: Flask,
    db: SQLAlchemy,
) -> None:
    """FR-01.4, SF-01: Thiếu tên, tác giả, số bản < 1 thì báo lỗi cạnh ô và giữ dữ liệu đã nhập."""
    client = app.test_client()
    token = _lay_csrf_token(client)

    phan_hoi = client.post(
        "/sach/them",
        data={
            "csrf_token": token,
            "isbn": "9786041234567",
            "ten": "",
            "tac_gia": "",
            "nam_xb": "2024",
            "so_ban": "0",
        },
    )

    html = phan_hoi.get_data(as_text=True)
    assert "9786041234567" in html
    assert "2024" in html
    assert db.session.query(Sach).count() == 0


def test_nfr10_post_them_sach_khong_co_csrf_token_bi_tu_choi_400(
    app: Flask,
    db: SQLAlchemy,
) -> None:
    """NFR-10: Gửi biểu mẫu POST không kèm mã chống CSRF bị từ chối với mã 400."""
    phan_hoi = app.test_client().post(
        "/sach/them",
        data={
            "isbn": "9786041234567",
            "ten": "Lập trình Python cơ bản",
            "tac_gia": "Nguyễn Văn A",
            "so_ban": "3",
        },
    )

    assert phan_hoi.status_code == 400
    assert db.session.query(Sach).count() == 0
