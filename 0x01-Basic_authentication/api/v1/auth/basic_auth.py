#!/usr/bin/env python3
""" Module for the authentication routes and class views """
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """ The authentication class for handling auth methods """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
            Returns the base 64 part of the
            Authorization header for a basic auth
        """
        if type(authorization_header) is not str:
            return None
        if authorization_header.startswith('Basic '):
            return authorization_header[6:]
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Returns the decoded value of a Base64 string """

        if type(base64_authorization_header) is not str:
            return None
        try:
            code = base64.b64decode(
                base64_authorization_header
            )
            return code.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """  Returns the user's email and password """
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return (email, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
            Returns the user instance based on
            the username and password supplied
        """
        if type(user_email) is not str or type(user_pwd) is not str:
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves the user instance for a request """

        head = self.authorization_header(request)
        if head is None:
            return None
        extract = self.extract_base64_authorization_header(head)
        if extract is None:
            return None
        decoded = self.decode_base64_authorization_header(extract)
        if decoded is None:
            return None
        credentials = self.extract_user_credentials(decoded)
        if credentials is None:
            return None
        user = self.user_object_from_credentials(
            credentials[0],
            credentials[1]
        )
        return user
