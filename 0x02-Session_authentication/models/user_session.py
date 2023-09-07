#!/usr/bin/env python3
""" This module contains a class for Session storage """
from models.base import Base


class UserSession(Base):
    """ The user session class for the Session authentication db """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a user session object """

        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
