#!/usr/bin/env python3
"""Session auth module"""


from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """Session auth class"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for a user_id"""
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user id based on session id"""
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None

        userId = self.user_id_by_session_id.get(session_id)
        return userId

    def current_user(self, request=None):
        """Returns a user instance based on a cookie value"""
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        user = User.get(user_id)

        return user

    def destroy_session(self, request=None):
        """Deletes the user session/logout"""
        if request is None:
            return False
        session_id_cookie = self.session_cookie(request)
        if session_id_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_id_cookie)
        if user_id is None:
            return False
        del(self.user_id_by_session_id[session_id_cookie])
        return True
