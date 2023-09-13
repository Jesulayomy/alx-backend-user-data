#!/usr/bin/env python3
""" authentication module for the user class """
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """ hashes a password with enough salt """

    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """
        Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
            hash the password with _hash_password, save the user to the
            database using self._db and return the User object.
        """

        if self._db.find_user_by(email=email):
            raise ValueError(f'User {email} already exists')
        hashed_pass = _hash_password(password)
        return self._db.add_user(email, hashed_pass)
