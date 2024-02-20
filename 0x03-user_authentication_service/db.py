#!/usr/bin/env python3
"""DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add user method"""
        user_created = User(email=email, hashed_password=hashed_password)
        self._session.add(user_created)
        self.__session.commit()

        return user_created

    def find_user_by(self, **kwargs) -> User:
        """FIids a user by arbitrary keyword arguments"""
        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        if not kwargs:
            raise InvalidRequestError
        return user
