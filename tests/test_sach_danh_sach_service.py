"""Kiểm thử service danh sách & tìm sách [T-02.1] (FR-02, BR-07, DB-01, NFR-01, NFR-09, 4.3)."""

from __future__ import annotations

import time
from datetime import date

import pytest
from flask_sqlalchemy import SQLAlchemy

from app.models import DocGia, PhieuMuon, Sach
from app.services.sach_service import danh_sach_sach, them_sach


def test_fr02_1_khi_chua_co_sach_tra_danh_sach_rong(db: SQLAlchemy) -> None:
    """FR-02.1 (biên 0 đầu sách): Trả về danh sách rỗng, tổng số 0, tổng trang 0."""
    ket_qua = danh_sach_sach()

    assert ket_qua.ds_sach == []
    assert ket_qua.trang == 1
    assert ket_qua.moi_trang == 20
    assert ket_qua.tong_so == 0
    assert ket_qua.tong_trang == 0


def test_fr02_1_phan_trang_25_dau_sach_moi_trang_20(db: SQLAlchemy) -> None:
    """FR-02.1 (Gherkin Phân trang): Có 25 đầu sách thì trang 1 có 20 mục, trang 2 có 5 mục."""
    for i in range(1, 26):
        them_sach(
            isbn=f"9786040000{i:03d}",
            ten=f"Sách giáo trình {i:02d}",
            tac_gia="Nguyễn Văn A",
            so_ban=2,
        )

    trang_1 = danh_sach_sach(trang=1)
    assert len(trang_1.ds_sach) == 20
    assert trang_1.trang == 1
    assert trang_1.moi_trang == 20
    assert trang_1.tong_so == 25
    assert trang_1.tong_trang == 2

    trang_2 = danh_sach_sach(trang=2)
    assert len(trang_2.ds_sach) == 5
    assert trang_2.trang == 2
    assert trang_2.tong_so == 25
    assert trang_2.tong_trang == 2

    tap_id_1 = {muc.id for muc in trang_1.ds_sach}
    tap_id_2 = {muc.id for muc in trang_2.ds_sach}
    assert tap_id_1.isdisjoint(tap_id_2)

    trang_vuot = danh_sach_sach(trang=3)
    assert trang_vuot.ds_sach == []
    assert trang_vuot.tong_so == 25
    assert trang_vuot.tong_trang == 2


@pytest.mark.parametrize("trang_nho_hon_1", [0, -1, -10])
def test_fr02_1_bien_trang_nho_hon_1_reset_ve_trang_1(
    db: SQLAlchemy,
    trang_nho_hon_1: int,
) -> None:
    """FR-02.1 (biên trang < 1): Tự động đưa `trang` về 1 và trả dữ liệu trang đầu tiên."""
    them_sach(
        isbn="9786041234567",
        ten="Lập trình Python cơ bản",
        tac_gia="Nguyễn Văn A",
        so_ban=3,
    )

    ket_qua = danh_sach_sach(trang=trang_nho_hon_1)
    assert ket_qua.trang == 1
    assert len(ket_qua.ds_sach) == 1


def test_fr02_1_muc_4_3_sap_xep_ten_theo_bang_chu_cai_tieng_viet(db: SQLAlchemy) -> None:
    """FR-02.1, mục 4.3: Sắp xếp tên A->Z theo chữ cái tiếng Việt ('Đ' sau 'D' và trước 'E')."""
    danh_muc_ngau_nhien = [
        ("9786040000101", "Em học toán"),
        ("9786040000102", "Đồ thị và thuật toán"),
        ("9786040000103", "Dữ liệu lớn"),
        ("9786040000104", "Âm thanh số"),
        ("9786040000105", "Ăn quả nhớ kẻ trồng cây"),
        ("9786040000106", "An toàn thông tin"),
        ("9786040000107", "Bí quyết lập trình"),
    ]
    for isbn, ten in danh_muc_ngau_nhien:
        them_sach(isbn=isbn, ten=ten, tac_gia="Tác giả", so_ban=1)

    ket_qua = danh_sach_sach()
    ds_ten = [muc.ten for muc in ket_qua.ds_sach]

    assert ds_ten == [
        "An toàn thông tin",
        "Ăn quả nhớ kẻ trồng cây",
        "Âm thanh số",
        "Bí quyết lập trình",
        "Dữ liệu lớn",
        "Đồ thị và thuật toán",
        "Em học toán",
    ]


def test_fr02_2_tim_kiem_khong_phan_biet_hoa_thuong_trong_ten_va_tac_gia(
    db: SQLAlchemy,
) -> None:
    """FR-02.2 (Gherkin): Tìm từ khoá không phân biệt hoa thường trên cả tên sách và tác giả."""
    them_sach(
        isbn="9786041234567",
        ten="Lập trình Python cơ bản",
        tac_gia="Nguyễn Văn A",
        so_ban=3,
    )
    them_sach(
        isbn="9786041234568",
        ten="Mạng máy tính",
        tac_gia="Đặng Thị Bình",
        so_ban=2,
    )

    theo_ten = danh_sach_sach(tu_khoa="lập TRÌNH")
    assert [muc.ten for muc in theo_ten.ds_sach] == ["Lập trình Python cơ bản"]

    theo_tac_gia = danh_sach_sach(tu_khoa="đặng THỊ")
    assert [muc.ten for muc in theo_tac_gia.ds_sach] == ["Mạng máy tính"]

    tu_khoa_trang = danh_sach_sach(tu_khoa="   ")
    assert tu_khoa_trang.tong_so == 2


def test_fr02_2_tim_kiem_co_phan_biet_dau_tieng_viet(db: SQLAlchemy) -> None:
    """FR-02.2: Tìm từ khoá không dấu không khớp với dữ liệu có dấu."""
    them_sach(
        isbn="9786041234567",
        ten="Lập trình Python cơ bản",
        tac_gia="Nguyễn Văn A",
        so_ban=3,
    )

    assert danh_sach_sach(tu_khoa="Lap trinh").ds_sach == []
    assert danh_sach_sach(tu_khoa="Nguyen Van").ds_sach == []


def test_fr02_3_tim_kiem_khong_co_ket_qua_tra_rong(db: SQLAlchemy) -> None:
    """FR-02.3 (Gherkin): Tìm từ khoá không tồn tại trả về danh sách rỗng và tổng số 0."""
    them_sach(
        isbn="9786041234567",
        ten="Lập trình Python cơ bản",
        tac_gia="Nguyễn Văn A",
        so_ban=3,
    )

    ket_qua = danh_sach_sach(tu_khoa="không-tồn-tại")
    assert ket_qua.ds_sach == []
    assert ket_qua.tong_so == 0
    assert ket_qua.tong_trang == 0


def test_br07_db01_tinh_dong_so_ban_con_chi_tru_phieu_dang_mo(db: SQLAlchemy) -> None:
    """BR-07, DB-01: `so_ban_con` chỉ trừ phiếu có `ngay_tra IS NULL`, không trừ phiếu đã trả."""
    sach = them_sach(
        isbn="9786041234567",
        ten="Lập trình Python cơ bản",
        tac_gia="Nguyễn Văn A",
        so_ban=3,
    )
    doc_gia = DocGia(ma_the="DG0001", ho_ten="Trần Thị B", email="b.tran@example.com")
    db.session.add(doc_gia)
    db.session.flush()

    phieu_dang_mo = PhieuMuon(
        sach_id=sach.id,
        doc_gia_id=doc_gia.id,
        ngay_muon=date(2026, 12, 1),
        han_tra=date(2026, 12, 15),
        ngay_tra=None,
    )
    phieu_da_tra = PhieuMuon(
        sach_id=sach.id,
        doc_gia_id=doc_gia.id,
        ngay_muon=date(2026, 11, 1),
        han_tra=date(2026, 11, 15),
        ngay_tra=date(2026, 11, 10),
    )
    db.session.add_all([phieu_dang_mo, phieu_da_tra])
    db.session.commit()

    ket_qua = danh_sach_sach()
    assert len(ket_qua.ds_sach) == 1
    muc = ket_qua.ds_sach[0]
    assert muc.isbn == "9786041234567"
    assert muc.so_ban == 3
    assert muc.so_ban_con == 2


def test_nfr09_tu_khoa_chua_sql_injection_va_ky_tu_dai_dien_an_toan(
    db: SQLAlchemy,
) -> None:
    """NFR-09: Từ khoá chứa `' OR 1=1 --` hoặc `%`, `_` không làm lộ toàn bộ danh sách."""
    them_sach(
        isbn="9786041234567",
        ten="Lập trình Python cơ bản",
        tac_gia="Nguyễn Văn A",
        so_ban=3,
    )

    assert danh_sach_sach(tu_khoa="' OR 1=1 --").tong_so == 0
    assert danh_sach_sach(tu_khoa="%").tong_so == 0
    assert danh_sach_sach(tu_khoa="_").tong_so == 0


def test_nfr01_hieu_nang_danh_sach_va_tim_kiem_5000_dau_sach_duoi_2_giay(
    db: SQLAlchemy,
) -> None:
    """NFR-01: Phân trang và tìm kiếm trên 5.000 đầu sách hoàn tất dưới 2 giây."""
    lo_sach = [
        Sach(
            isbn=f"978604{i:07d}",
            ten=f"Giáo trình Công nghệ phần mềm tập {i}",
            tac_gia=f"Tác giả {i % 100}",
            nam_xb=2026,
            so_ban=3,
        )
        for i in range(1, 5001)
    ]
    db.session.add_all(lo_sach)
    db.session.commit()

    bat_dau_ds = time.perf_counter()
    kq_ds = danh_sach_sach(trang=1)
    thoi_gian_ds = time.perf_counter() - bat_dau_ds

    bat_dau_tim = time.perf_counter()
    kq_tim = danh_sach_sach(tu_khoa="phần MỀM tập 499", trang=1)
    thoi_gian_tim = time.perf_counter() - bat_dau_tim

    assert len(kq_ds.ds_sach) == 20
    assert kq_ds.tong_so == 5000
    assert thoi_gian_ds < 2.0
    assert kq_tim.tong_so == 11
    assert thoi_gian_tim < 2.0
