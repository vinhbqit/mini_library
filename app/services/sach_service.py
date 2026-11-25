"""Điều phối ca sử dụng quản lý đầu sách (FR-01, BR-01, BR-07, DB-01, DB-02, NFR-04)."""

from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import PhieuMuon, Sach
from app.services.isbn import chuan_hoa_isbn, la_isbn_hop_le
from app.services.loi import LoiNghiepVu


def _phan_tich_so_nguyen(gia_tri: int | str) -> int | None:
    """Chuyển đổi đầu vào sang `int` (từ chối `bool` và chuỗi không phải số nguyên)."""
    if isinstance(gia_tri, bool):
        return None
    if isinstance(gia_tri, int):
        return gia_tri
    if isinstance(gia_tri, str):
        chuoi = gia_tri.strip()
        if not chuoi:
            return None
        try:
            return int(chuoi)
        except ValueError:
            return None
    return None


def them_sach(
    isbn: str,
    ten: str,
    tac_gia: str,
    so_ban: int | str,
    nam_xb: int | str | None = None,
) -> Sach:
    """Kiểm tra quy tắc BR-01, BR-07 và thêm đầu sách mới trong một giao dịch (FR-01)."""
    ds_loi: list[tuple[str | None, str, dict[str, Any] | None]] = []
    isbn_chuan: str | None = None

    if not la_isbn_hop_le(isbn):
        ds_loi.append(("isbn", "isbn_khong_hop_le", {}))
    else:
        isbn_chuan = chuan_hoa_isbn(isbn)
        da_ton_tai = db.session.scalar(select(Sach.id).filter_by(isbn=isbn_chuan))
        if da_ton_tai is not None:
            ds_loi.append(("isbn", "isbn_da_ton_tai", {}))

    ten_sach = ten.strip()
    if not ten_sach:
        ds_loi.append(("ten", "ten_sach_trong", {}))

    ten_tac_gia = tac_gia.strip()
    if not ten_tac_gia:
        ds_loi.append(("tac_gia", "tac_gia_trong", {}))

    nam_xb_hop_le: int | None = None
    if nam_xb is not None and not (isinstance(nam_xb, str) and not nam_xb.strip()):
        nam_xb_hop_le = _phan_tich_so_nguyen(nam_xb)
        if nam_xb_hop_le is None:
            ds_loi.append(("nam_xb", "nam_xb_khong_hop_le", {}))

    so_ban_hop_le = _phan_tich_so_nguyen(so_ban)
    if so_ban_hop_le is None or so_ban_hop_le < 1:
        ds_loi.append(("so_ban", "so_ban_khong_hop_le", {}))

    if ds_loi:
        raise LoiNghiepVu(ds_loi)

    assert isbn_chuan is not None
    assert so_ban_hop_le is not None

    sach_moi = Sach(
        isbn=isbn_chuan,
        ten=ten_sach,
        tac_gia=ten_tac_gia,
        nam_xb=nam_xb_hop_le,
        so_ban=so_ban_hop_le,
    )
    try:
        db.session.add(sach_moi)
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise LoiNghiepVu([("isbn", "isbn_da_ton_tai", {})]) from exc

    return sach_moi


def tinh_so_ban_con(sach_id: int) -> int:
    """Tính động số bản còn = `so_ban` trừ số phiếu đang mở của đầu sách (BR-07, DB-01)."""
    sach = db.session.get(Sach, sach_id)
    if sach is None:
        raise ValueError(f"Khong tim thay sach id={sach_id}")

    so_phieu_mo = db.session.scalar(
        select(func.count(PhieuMuon.id)).where(
            PhieuMuon.sach_id == sach_id,
            PhieuMuon.ngay_tra.is_(None),
        )
    )
    return sach.so_ban - int(so_phieu_mo or 0)
