"""Các route quản lý đầu sách (FR-01, MH-03, SF-01, NFR-10)."""

from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.wrappers import Response

from app.messages import THONG_BAO_THEM_SACH_THANH_CONG, anh_xa_ds_loi
from app.services.loi import LoiNghiepVu
from app.services.sach_service import them_sach

sach_bp = Blueprint("sach", __name__, url_prefix="/sach")


@sach_bp.get("")
def danh_sach() -> str:
    """Điểm đích danh sách sách (sẽ hoàn thiện bảng phân trang MH-02 ở T-02.2)."""
    return render_template("base.html")


@sach_bp.route("/them", methods=["GET", "POST"])
def them() -> str | Response:
    """Hiển thị và xử lý biểu mẫu thêm đầu sách mới MH-03 (FR-01, SF-01, NFR-10)."""
    if request.method == "GET":
        return render_template(
            "sach_form.html",
            du_lieu={},
            loi_truong={},
            loi_chung=[],
        )

    du_lieu = {
        "isbn": request.form.get("isbn", ""),
        "ten": request.form.get("ten", ""),
        "tac_gia": request.form.get("tac_gia", ""),
        "nam_xb": request.form.get("nam_xb", ""),
        "so_ban": request.form.get("so_ban", ""),
    }

    try:
        them_sach(
            isbn=du_lieu["isbn"],
            ten=du_lieu["ten"],
            tac_gia=du_lieu["tac_gia"],
            so_ban=du_lieu["so_ban"],
            nam_xb=du_lieu["nam_xb"],
        )
    except LoiNghiepVu as loi:
        loi_truong, loi_chung = anh_xa_ds_loi(loi)
        return render_template(
            "sach_form.html",
            du_lieu=du_lieu,
            loi_truong=loi_truong,
            loi_chung=loi_chung,
        )

    flash(THONG_BAO_THEM_SACH_THANH_CONG, "success")
    return redirect(url_for("sach.danh_sach"))
