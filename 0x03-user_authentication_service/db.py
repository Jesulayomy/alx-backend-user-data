#!/usr/bin/env python3
""" Data Base module for managing the sessions
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from typing import Mapping

from user import (
    Base,
    User,
)


class DB:
    """ Data Base class to create the engine
    """

    def __init__(self) -> None:
        """ Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """ Memoized session object for the database
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
            Saves a user to the database using his email and hashed pass
        """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs: Mapping) -> User:
        """ Takes the keyword arguments and returns the first matching row """
        if not kwargs:
            raise InvalidRequestError
        valid_attrs = ['id', 'email',
                       'hashed_password',
                       'session_id', 'reset_token']
        for key in kwargs.keys():
            if key not in valid_attrs:
                raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs: Mapping) -> None:
        """ Updates a user based on its integer ID """
        user = self.find_user_by(id=user_id)
        if user:
            valid_attrs = [
                    'id', 'email',
                    'hashed_password',
                    'session_id', 'reset_token']
            for key, val in kwargs.items():
                if key not in valid_attrs:
                    raise ValueError
                setattr(user, key, val)
        self._session.add(user)
        self._session.commit()
