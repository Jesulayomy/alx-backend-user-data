#!/usr/bin/env python3
""" authentication module for the user class """
import bcrypt
from typing import TypeVar
from uuid import uuid4

from db import DB


def _hash_password(password: str) -> bytes:
    """ hashes a password with enough salt """

    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ a uuid string generator """
    return str(uuid4())


class Auth:
    """
        Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ Initializes the first call to the auth class """
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """
            hash the password with _hash_password, save the user to the
            database using self._db and return the User object.
        """

        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            hashed_pass = _hash_password(password)
            return self._db.add_user(email, hashed_pass)

        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """ If it matches return True. In any other case, return False """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """ creates a session and returns it's session_id """

        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        if user:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id

    def get_user_from_session_id(self, session_id: str) -> TypeVar('User'):
        """
            session_id string argument and returns the
            corresponding User or None.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: str) -> None:
        """ destroys a session from the db """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ resets a password using a tokrn """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError
        if user is None:
            raise ValueError
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """ Updates a password (Hash) and reset token to none """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError
        hashed_pass = _hash_password(password)
        self._db.update_user(
                user.id,
                hashed_password=hashed_pass,
                reset_token=None)
