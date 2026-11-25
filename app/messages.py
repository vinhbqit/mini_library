"""Tập trung toàn bộ câu thông báo tiếng Việt giao diện theo SRS (mục 3.1, SF-01, 4.3)."""

from __future__ import annotations

from app.services.loi import LoiNghiepVu

THONG_BAO_THEM_SACH_THANH_CONG = "Đã thêm đầu sách thành công"

BANG_THONG_BAO_LOI: dict[str, str] = {
    "isbn_da_ton_tai": "ISBN đã tồn tại",
    "isbn_khong_hop_le": "ISBN không hợp lệ",
    "ten_sach_trong": "Vui lòng nhập tên sách",
    "tac_gia_trong": "Vui lòng nhập tác giả",
    "nam_xb_khong_hop_le": "Năm xuất bản không hợp lệ",
    "so_ban_khong_hop_le": "Số bản phải từ 1 trở lên",
}


def anh_xa_ds_loi(loi: LoiNghiepVu) -> tuple[dict[str, list[str]], list[str]]:
    """Chuyển `LoiNghiepVu` thành lỗi theo từng ô nhập và lỗi chung bằng tiếng Việt (SF-01)."""
    loi_theo_truong: dict[str, list[str]] = {}
    loi_chung: list[str] = []

    for ten_truong, ma_loi, tham_so in loi.ds_loi:
        mau_cau = BANG_THONG_BAO_LOI.get(ma_loi, ma_loi)
        thong_bao = mau_cau.format(**tham_so) if tham_so else mau_cau
        if ten_truong is None:
            loi_chung.append(thong_bao)
        else:
            loi_theo_truong.setdefault(ten_truong, []).append(thong_bao)

    return loi_theo_truong, loi_chung
