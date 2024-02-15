#!/usr/bin/env python3
"""Session expiration module"""

from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Sessio expiration class"""

    def __init__(self):
        """Overload"""
        session_duration = getenv('SESSION_DURATION')
        try:
            self.session_duration = int(session_duration)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Creates a session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns id for a given session"""
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        user_id = session_dict.get("user_id")
        if self.session_duration <= 0:
            return user_id

        created_at = session_dict.get("created_at")
        if created_at is None:
            return None

        exp_time = created_at + timedelta(seconds=self.session_duration)
        if exp_time < datetime.now():
            return None
        return user_id
