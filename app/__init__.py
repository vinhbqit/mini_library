"""Khởi tạo ứng dụng Flask cho Hệ thống Thư viện mini (mục 2.2, DB-02, NFR-10)."""

from __future__ import annotations

import os
import secrets
import sqlite3
from collections.abc import Mapping
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


@event.listens_for(Engine, "connect")
def _bat_khoa_ngoai_sqlite(dbapi_connection: Any, _connection_record: Any) -> None:
    """Bật kiểm tra ràng buộc khoá ngoại cho mọi kết nối SQLite (DB-02)."""
    if isinstance(dbapi_connection, sqlite3.Connection):
        con_tro = dbapi_connection.cursor()
        con_tro.execute("PRAGMA foreign_keys=ON")
        con_tro.close()


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
