#!/usr/bin/env python3
""" Module for the session authentication class """
from flask import session
from typing import TypeVar
from uuid import uuid4
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime
from models.user import User
from os import getenv


class SessionExpAuth(SessionAuth):
    """ Session authentication class for the users api with timeout """

    def __init__(self):
        """ Overload function and constructor """
        session_duration = getenv('SESSION_DURATION', 0)

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a session for the user ID """
        try:
            session_id = super()
        except Exception:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
            }

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ overloads and Returns the user id for the session id given """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id.get(session_id).get("user_id")
        if "created_at" not in self.user_id_by_session_id.get(
                "session_id").keys():
            return None
        created_at = self.user_id_by_session_id.get(
                "session_id").get("created_at")
        if created_at + self.session_duration < datetime.now():
            return None
        return self.user_id_by_session_id.get(session_id).get("user_id")
