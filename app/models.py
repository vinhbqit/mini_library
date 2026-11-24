"""Mô hình dữ liệu SQLAlchemy cho 4 bảng trong SRS mục 4.1 (DB-01, DB-02, DB-04)."""

from __future__ import annotations

from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db


class Sach(db.Model):
    """Bảng đầu sách `sach` (mục 4.1, BR-01, BR-07, DB-01, DB-02).

    Không lưu cột số bản còn; số bản còn luôn tính từ các phiếu mở (DB-01).
    """

    __tablename__ = "sach"
    __table_args__ = (
        CheckConstraint("so_ban >= 1", name="ck_sach_so_ban_toi_thieu"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    isbn: Mapped[str] = mapped_column(String(13), nullable=False, unique=True)
    ten: Mapped[str] = mapped_column(String(200), nullable=False)
    tac_gia: Mapped[str] = mapped_column(String(200), nullable=False)
    nam_xb: Mapped[int | None] = mapped_column(Integer, nullable=True)
    so_ban: Mapped[int] = mapped_column(Integer, nullable=False)

    ds_phieu_muon: Mapped[list[PhieuMuon]] = relationship(
        "PhieuMuon",
        back_populates="sach",
    )


class DocGia(db.Model):
    """Bảng độc giả `doc_gia` (mục 4.1, BR-08, DB-02)."""

    __tablename__ = "doc_gia"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ma_the: Mapped[str] = mapped_column(String(6), nullable=False, unique=True)
    ho_ten: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    sdt: Mapped[str | None] = mapped_column(String(15), nullable=True)

    ds_phieu_muon: Mapped[list[PhieuMuon]] = relationship(
        "PhieuMuon",
        back_populates="doc_gia",
    )


class PhieuMuon(db.Model):
    """Bảng phiếu mượn `phieu_muon` (mục 4.1, BR-03, BR-05, DB-02, DB-03)."""

    __tablename__ = "phieu_muon"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sach_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sach.id", ondelete="RESTRICT"),
        nullable=False,
    )
    doc_gia_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("doc_gia.id", ondelete="RESTRICT"),
        nullable=False,
    )
    ngay_muon: Mapped[date] = mapped_column(Date, nullable=False)
    han_tra: Mapped[date] = mapped_column(Date, nullable=False)
    ngay_tra: Mapped[date | None] = mapped_column(Date, nullable=True)
    tien_phat: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    sach: Mapped[Sach] = relationship("Sach", back_populates="ds_phieu_muon")
    doc_gia: Mapped[DocGia] = relationship("DocGia", back_populates="ds_phieu_muon")


class ThuThu(db.Model):
    """Bảng tài khoản thủ thư `thu_thu` (mục 4.1, FR-08, NFR-08, DB-02)."""

    __tablename__ = "thu_thu"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ten_dang_nhap: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    mat_khau_hash: Mapped[str] = mapped_column(String(255), nullable=False)
