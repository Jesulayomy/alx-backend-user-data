#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *    # noqa E402
from api.v1.views.users import *    # noqa E402
from api.v1.views.session_auth import *    # noqa E402

User.load_from_file()
