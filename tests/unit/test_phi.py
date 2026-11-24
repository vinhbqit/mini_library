"""Unit test độc lập cho quy tắc tính phí trễ hạn (FR-06 mục 3.1, BR-05 mục 3.3.5, NFR-15).

Không khởi tạo Flask app; kiểm chứng đầy đủ 6 dòng Examples của kịch bản Gherkin
"Tính phí trễ hạn" (hạn trả 15/12/2026) và các giá trị biên của BR-05 (0, 1, 19, 20, 21, 30 ngày).
"""

from __future__ import annotations

from datetime import date

from app.services.phi import tinh_phi_tre

HAN_TRA_P1 = date(2026, 12, 15)


def test_fr06_br05_tra_truoc_han_10_12_2026_khong_tinh_phi() -> None:
    """FR-06 Examples #1, BR-05: Trả trước hạn (10/12/2026) thì trễ 0 ngày, phí 0 đồng."""
    so_ngay_tre, tien_phat = tinh_phi_tre(HAN_TRA_P1, date(2026, 12, 10))
    assert (so_ngay_tre, tien_phat) == (0, 0)


def test_fr06_br05_tra_dung_ngay_han_15_12_2026_tre_0_ngay() -> None:
    """FR-06 Examples #2, BR-05 (biên 0 ngày): Trả đúng hạn 15/12/2026 thì trễ 0 ngày, phí 0 đ."""
    so_ngay_tre, tien_phat = tinh_phi_tre(HAN_TRA_P1, date(2026, 12, 15))
    assert (so_ngay_tre, tien_phat) == (0, 0)


def test_fr06_br05_tre_1_ngay_16_12_2026_phi_5000() -> None:
    """FR-06 Examples #3, BR-05 (biên 1 ngày): Trả ngày 16/12/2026 trễ 1 ngày, phí 5.000 đồng."""
    so_ngay_tre, tien_phat = tinh_phi_tre(HAN_TRA_P1, date(2026, 12, 16))
    assert (so_ngay_tre, tien_phat) == (1, 5000)


def test_fr06_br05_tre_3_ngay_18_12_2026_phi_15000() -> None:
    """FR-06 Examples #4, BR-05: Trả ngày 18/12/2026 trễ 3 ngày, phí 15.000 đồng."""
    so_ngay_tre, tien_phat = tinh_phi_tre(HAN_TRA_P1, date(2026, 12, 18))
    assert (so_ngay_tre, tien_phat) == (3, 15000)


def test_br05_bien_tre_19_ngay_sat_duoi_muc_tran_95000() -> None:
    """BR-05 (biên 19 ngày): Trả ngày 03/01/2027 trễ 19 ngày, phí 95.000 đồng (sát dưới trần)."""
    so_ngay_tre, tien_phat = tinh_phi_tre(HAN_TRA_P1, date(2027, 1, 3))
    assert (so_ngay_tre, tien_phat) == (19, 95000)


def test_fr06_br05_tre_20_ngay_cham_muc_tran() -> None:
    """FR-06 Examples #5, BR-05 (biên 20 ngày): Trả 04/01/2027 trễ 20 ngày, trần 100.000 đ."""
    so_ngay_tre, tien_phat = tinh_phi_tre(HAN_TRA_P1, date(2027, 1, 4))
    assert (so_ngay_tre, tien_phat) == (20, 100000)


def test_br05_bien_tre_21_ngay_vuot_muc_tran_100000() -> None:
    """BR-05 (biên 21 ngày): Trả ngày 05/01/2027 trễ 21 ngày, phí giữ ở mức trần 100.000 đồng."""
    so_ngay_tre, tien_phat = tinh_phi_tre(HAN_TRA_P1, date(2027, 1, 5))
    assert (so_ngay_tre, tien_phat) == (21, 100000)


def test_fr06_br05_tre_30_ngay_giu_muc_tran_100000() -> None:
    """FR-06 Examples #6, BR-05 (biên 30 ngày): Trả 14/01/2027 trễ 30 ngày, tối đa 100.000 đ."""
    so_ngay_tre, tien_phat = tinh_phi_tre(HAN_TRA_P1, date(2027, 1, 14))
    assert (so_ngay_tre, tien_phat) == (30, 100000)


def test_br05_ket_qua_tra_ve_kieu_so_nguyen_khong_dung_float() -> None:
    """BR-05: Số ngày trễ và tiền phạt luôn có kiểu `int` (đơn vị đồng), không dùng `float`."""
    so_ngay_tre, tien_phat = tinh_phi_tre(HAN_TRA_P1, date(2026, 12, 18))
    assert type(so_ngay_tre) is int
    assert type(tien_phat) is int
