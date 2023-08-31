#!/usr/bin/env python3
""" Encrypting and Validating user passwords """
import bcrypt


def hash_password(password: str) -> bytes:
    """ Returns a salted and hashed password, as a byte string """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Validates a password using its byte-ified hash """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
