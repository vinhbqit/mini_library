"""Khởi tạo ứng dụng Flask cho Hệ thống Thư viện mini (mục 2.2, DB-02, NFR-10)."""

from __future__ import annotations

import os
import secrets
import sqlite3
import unicodedata
from collections.abc import Mapping
from functools import lru_cache
from pathlib import Path
from typing import Any

from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import Engine, event

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()


_CHU_CAI_TIENG_VIET = (
    "aàảãáạăằẳẵắặâầẩẫấậbcdđeèẻẽéẹêềểễếệfghijklmnoòỏõóọôồổỗốộơờởỡớợ"
    "pqrstuùủũúụưừửữứựvwxyỳỷỹýỵz"
)
_BANG_THU_TU_VI: dict[str, tuple[int, int]] = {
    **{chr(ma): (0, ma) for ma in range(ord("a"))},
    **{ky_tu: (1, chi_so) for chi_so, ky_tu in enumerate(_CHU_CAI_TIENG_VIET)},
}


@lru_cache(maxsize=8192)
def _khoa_sap_xep_tieng_viet(chuoi: str) -> tuple[tuple[int, int], ...]:
    """Sinh khoá so sánh thứ tự chữ cái tiếng Việt (mục 4.3)."""
    chuan_nfc = unicodedata.normalize("NFC", chuoi).casefold()
    return tuple(_BANG_THU_TU_VI.get(ky_tu, (2, ord(ky_tu))) for ky_tu in chuan_nfc)


def _so_sanh_tieng_viet(trai: str, phai: str) -> int:
    """Hàm collation `VIETNAMESE` cho SQLite ('Đ' đứng sau 'D' và trước 'E', mục 4.3)."""
    khoa_trai = _khoa_sap_xep_tieng_viet(trai)
    khoa_phai = _khoa_sap_xep_tieng_viet(phai)
    if khoa_trai < khoa_phai:
        return -1
    if khoa_trai > khoa_phai:
        return 1
    return 0


def _chua_tu_khoa_vi(van_ban: str | None, tu_khoa: str | None) -> int:
    """So khớp chuỗi con không phân biệt hoa thường nhưng có phân biệt dấu (FR-02.2)."""
    if van_ban is None or tu_khoa is None:
        return 0
    van_ban_chuan = unicodedata.normalize("NFC", van_ban).casefold()
    tu_khoa_chuan = unicodedata.normalize("NFC", tu_khoa).casefold()
    return 1 if tu_khoa_chuan in van_ban_chuan else 0


@event.listens_for(Engine, "connect")
def _bat_khoa_ngoai_sqlite(dbapi_connection: Any, _connection_record: Any) -> None:
    """Bật khoá ngoại và đăng ký hàm/collation tiếng Việt cho mọi kết nối SQLite (DB-02, 4.3)."""
    if isinstance(dbapi_connection, sqlite3.Connection):
        con_tro = dbapi_connection.cursor()
        con_tro.execute("PRAGMA foreign_keys=ON")
        con_tro.close()
        dbapi_connection.create_collation("VIETNAMESE", _so_sanh_tieng_viet)
        dbapi_connection.create_function("chua_tu_khoa_vi", 2, _chua_tu_khoa_vi)


def create_app(config: Mapping[str, Any] | None = None) -> Flask:
    """Tạo và cấu hình ứng dụng Flask với SQLite và chống CSRF (2.2, 3.2.4, NFR-10)."""
    app = Flask(__name__, instance_relative_config=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    duong_dan_csdl = Path(app.instance_path) / "thu_vien.db"
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY") or secrets.token_hex(32),
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{duong_dan_csdl}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=True,
    )

    if config is not None:
        app.config.update(config)

    if app.debug or app.testing:
        app.config.setdefault("SESSION_COOKIE_SECURE", False)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from app import models as _models  # noqa: F401
    from app.routes.sach import sach_bp

    app.register_blueprint(sach_bp)

    @app.get("/")
    def trang_chu() -> str:
        """Hiển thị khung giao diện chính với thanh menu (mục 3.2.1)."""
        return render_template("base.html")

    return app
