"""Các quy tắc tính toán và kiểm tra nghiệp vụ thuần (BR-05, FR-06, NFR-15).

Module này tuyệt đối không import Flask hay models để đảm bảo unit test độc lập.
"""

from __future__ import annotations

from datetime import date

DON_GIA_PHAT_MOI_NGAY: int = 5000
MUC_TRAN_TIEN_PHAT: int = 100000


def tinh_phi_tre(han_tra: date, ngay_tra: date) -> tuple[int, int]:
    """Tính số ngày trễ và tiền phạt trễ hạn cho một phiếu mượn (BR-05, FR-06).

    Công thức: `5.000 đ × số ngày trễ`, tối đa `100.000 đ` mỗi phiếu;
    trả trước hoặc đúng ngày hạn thì trễ `0` ngày, phí `0` đồng.
    """
    if ngay_tra <= han_tra:
        return 0, 0

    so_ngay_tre: int = (ngay_tra - han_tra).days
    tien_phat: int = min(so_ngay_tre * DON_GIA_PHAT_MOI_NGAY, MUC_TRAN_TIEN_PHAT)
    return so_ngay_tre, tien_phat
