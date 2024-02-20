#!/usr/bin/env python3
"""Hash pasword module"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Generate a salted hash for the hash password"""
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Init"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            new_user = self._db.add_user(email, _hash_password(password))
            return new_user
