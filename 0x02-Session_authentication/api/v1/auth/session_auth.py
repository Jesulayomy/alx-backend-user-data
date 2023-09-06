#!/usr/bin/env python3
""" Module for the session authentication class """
from flask import session
from typing import TypeVar
from uuid import uuid4
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ Session authentication class for the users api """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a session for the user ID """
        if type(user_id) is not str:
            return None
        session_id = uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns the user id for the session id given """

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Returns a User instance based on cookie values """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ deletwes the user session and logs out """
        if request is None:
            return None
        cookies = self.session_cookie(request)
        if cookies is None or cookies == '':
            return False
        if self.user_id_for_session_id(cookies) is None:
            return False
        del self.user_id_by_session_id[cookies]
        return True
