#!/usr/bin/env python3
""" Data Base module for managing the sessions
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

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
            user = User(
                    email=email,
                    hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs) -> User:
        """ Takes the keyword arguments and returns the first matching row """
        keys = []
        values = []
        for k, v in kwargs.items():
            if not hasattr(User, k):
                raise InvalidRequestError()
            else:
                keys.append(getattr(User, k))
                values.append(v)

        res = self._session.query(User).filter(
                tuple_(*keys)).in_([tuple(values)]).first()
        if res is none:
            raise NoResultFound()
        return res

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Updates a user based on its integer ID """

        user = self.find_user_by(id=user_id)
        if user is None:
            return
        updates = {}
        for k, v in kwargs.items():
            if hasattr(User, k):
                updates[getattr(User, k)] = v
            else:
                raise ValueError()
        self._session.query(User).filter(User.id == user_id).update(
            updates,
            synchronize_session=False,
        )
        self._session.commit()
