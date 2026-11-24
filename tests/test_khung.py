"""Kiểm thử dựng khung CSDL và giao diện theo mục 3.2.1, 4.1 của SRS (DB-01, DB-02)."""

from __future__ import annotations

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text


def test_db01_db02_tao_du_4_bang_va_khong_co_cot_so_ban_con(db: SQLAlchemy) -> None:
    """Xác nhận tạo thành công 4 bảng mục 4.1, bật FK và không lưu cột số bản còn."""
    bo_kiem_tra = inspect(db.engine)
    tap_bang = set(bo_kiem_tra.get_table_names())

    assert {"sach", "doc_gia", "phieu_muon", "thu_thu"}.issubset(tap_bang)

    cot_bang_sach = {cot["name"] for cot in bo_kiem_tra.get_columns("sach")}
    assert cot_bang_sach == {"id", "isbn", "ten", "tac_gia", "nam_xb", "so_ban"}
    assert "so_ban_con" not in cot_bang_sach

    trang_thai_fk = db.session.execute(text("PRAGMA foreign_keys")).scalar()
    assert trang_thai_fk == 1


def test_khung_giao_dien_hien_thi_thanh_menu_3_2_1(app: Flask) -> None:
    """Xác nhận mở `/` trả mã 200 và hiển thị đủ thanh menu theo mục 3.2.1."""
    phan_hoi = app.test_client().get("/")
    assert phan_hoi.status_code == 200

    noi_dung = phan_hoi.get_data(as_text=True)
    for muc_menu in ("Sách", "Độc giả", "Mượn sách", "Phiếu đang mở", "Quá hạn", "Đăng xuất"):
        assert muc_menu in noi_dung
