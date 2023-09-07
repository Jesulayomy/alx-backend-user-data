#!/usr/bin/env python3
""" Module for the session authentication class """
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """ Session authentication class for the users api with timeout """

    def __init__(self) -> None:
        """ Overload function and constructor """
        try:
            self.session_duration = int(getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """ creates a session for the user ID """
        try:
            session_id = super().create_session(user_id)
        except Exception:
            return None
        if session_id:
            self.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.utcnow()
                }
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ overloads and Returns the user id for the session id given """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id.get(session_id).get("user_id")
        created_at = self.user_id_by_session_id.get(session_id).get(
            "created_at")
        if not created_at:
            return None
        exp_time = created_at + timedelta(seconds=self.session_duration)
        if exp_time < datetime.utcnow():
            return None
        return self.user_id_by_session_id.get(session_id).get("user_id")
