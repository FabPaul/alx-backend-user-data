#!/usr/bin/env python3
"""Hash pasword module"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Generate a salted hash for the hash password"""
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_password


def _generate_uuid() -> str:
    """Function to generate Uuid"""
    return str(uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """check if login credentials are valid"""
        try:
            user = self._db.find_user_by(email=email)
            hash_password = user.hashed_password
            return bcrypt.checkpw(password.encode('utf-8'), hash_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a session ID """
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            return user.session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Gets a user object using sessions ID, returns uUser or None"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys session by user ID"""
        if user_id is None:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Reset password token"""
        try:
            user = self._db.find_user_by(email=email)
            user.reset_token = _generate_uuid()
            return user.reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Function to Update password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            user.hashed_password = _hash_password(password)
            user.reset_token = None
        except NoResultFound:
            raise ValueError
