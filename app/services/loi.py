"""Định nghĩa ngoại lệ nghiệp vụ có cấu trúc cho tầng services (3.1, 3.2.1, SF-01, 4.3)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

MucLoi = tuple[str | None, str, dict[str, Any]]


class LoiNghiepVu(Exception):
    """Ngoại lệ mang danh sách lỗi nghiệp vụ có cấu trúc `(ten_truong, ma_loi, tham_so)`.

    Không nhúng trực tiếp chuỗi thông báo giao diện tiếng Việt để đảm bảo tách biệt
    văn bản hiển thị khỏi mã xử lý (SF-01, mục 4.3).
    """

    def __init__(
        self,
        ds_loi: Sequence[tuple[str | None, str, dict[str, Any] | None]],
    ) -> None:
        self.ds_loi: list[MucLoi] = [
            (ten_truong, ma_loi, dict(tham_so) if tham_so is not None else {})
            for ten_truong, ma_loi, tham_so in ds_loi
        ]
        super().__init__(self.ds_loi)
