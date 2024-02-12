#!/usr/bin/env python3
"""Auth class"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Module for required paths"""
        return False

    def authorization_header(self, request=None) -> str:
        """Authorized headers"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None
