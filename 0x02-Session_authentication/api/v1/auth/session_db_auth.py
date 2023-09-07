#!/usr/bin/env python3
""" This module contains a class for Session storage auth """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ a session DB auth class """

    def create_session(self, user_id=None):
        """ creates a session ID for a user ID """

        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession(user_id=user_id,
                                       session_id=session_id)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """ returns a User ID based on a Session ID """

        if session_id is None or type(session_id) is not str:
            return None
        try:
            user_session = UserSession.search({'session_id': session_id})
        except Exception:
            return None

        if user_session:
            user_session = user_session[0]
            if self.session_duration <= 0:
                return user_session.user_id
            created_at = user_session.created_at
            if not created_at:
                return None
            exp_time = created_at + timedelta(
                                            seconds=self.session_duration)
            if exp_time < datetime.utcnow():
                return None
            return user_session.user_id

    def destroy_session(self, request=None):
        """ destroys a session """

        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return False

        user_session = user_session[0]
        user_session.remove()
        return True
