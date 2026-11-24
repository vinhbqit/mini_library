"""Cấu hình fixture dùng chung cho pytest với SQLite trong bộ nhớ (NFR-15)."""

from __future__ import annotations

from collections.abc import Generator

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from app import db as _db


@pytest.fixture()
def app() -> Generator[Flask, None, None]:
    """Khởi tạo ứng dụng Flask thử nghiệm với CSDL SQLite `:memory:`."""
    ung_dung = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SECRET_KEY": "khoa-thu-nghiem-khong-dung-san-xuat",
        }
    )
    with ung_dung.app_context():
        yield ung_dung


@pytest.fixture()
def db(app: Flask) -> Generator[SQLAlchemy, None, None]:
    """Tạo toàn bộ bảng trên SQLite trong bộ nhớ cho mỗi ca kiểm thử."""
    _db.create_all()
    yield _db
    _db.session.remove()
    _db.drop_all()
