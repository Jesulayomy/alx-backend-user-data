#!/usr/bin/env python3
""" Module for the authentication routes and class views """
import re
from flask import request
from os import getenv
from typing import List, TypeVar


class Auth:
    """ The authentication class for handling auth methods """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            Returns true if path is not in the route
            Returns false if path is in the excluded
        """
        if excluded_paths is None or excluded_paths == [] or path is None:
            return True
        if path[-1] != '/':
            path += '/'
        for route in excluded_paths:
            if re.match(route.replace('*', '.*'), path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Returns None for now to the header authorization """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None, will be the flask request object """
        return None

    def session_cookie(self, request=None):
        """ gets a cookie value from a request passed into the method"""
        if request is None:
            return None
        session_name = getenv('SESSION_NAME')
        return request.cookies.get(session_name)
