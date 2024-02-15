#!/usr/bin/env python3
"""Session DB auth module"""


from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from os import getenv


class SessionDBAuth(SessionExpAuth):
    """Session DB auth class"""

    def create_session(self, user_id=None):
        """Creates and stores new instance of usersession, return session_id"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_sessions = UserSession(user_id=user_id, session_id=session_id)
        user_sessions.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns user  by id requesting usersession in DB"""
        if session_id is None:
            return None
        user_sessions = UserSession.search({"session_id": session_id})
        if user_sessions:
            return user_sessions[0].user_id
        else:
            return None

    def destroy_session(self, request=None):
        """Destroy the usersession based on the session id from req cookie"""
        session_cookie_name = getenv("SESSION_NAME")
        session_id = request.cookies.get(session_cookie_name)
        if session_id:
            user_sessions = UserSession.search({"session_id": session_id})
            for session in user_sessions:
                session.remove()
