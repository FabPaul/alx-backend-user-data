#!/usr/bin/env python3
"""Baisc auth class module"""

from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic auth class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract base 64 part of authorization header and return it"""
        if authorization_header is None:
            return None
        elif type(authorization_header) is not str:
            return None
        elif not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[-1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Returns decoded value of base64 string"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            decodable = base64_authorization_header.encode('utf-8')
            decoded = base64.b64decode(decodable)
            return decoded.decode('utf-8')

        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Returns the user email and password from base64 decode"""
        if decoded_base64_authorization_header is None:
            return None, None
        elif type(decoded_base64_authorization_header) is not str:
            return None, None

        colon = decoded_base64_authorization_header.find(':')
        if colon == -1:
            return None, None

        email = decoded_base64_authorization_header[:colon]
        password = decoded_base64_authorization_header[colon + 1:]

        return email, password

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Returns the user instance on his email and password"""
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None

        try:
            users = User.search({'email': user_email})
            if not users:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrieve the User instance for a request"""
        if request is None:
            return None

        auth_header = self.authorization_header(request)  # Extract AH from req
        # Extract base64 auth header
        base64_header = self.extract_base64_authorization_header(auth_header)

        if base64_header is None:
            return None

        decoded = self.decode_base64_authorization_header(base64_header)
        if decoded is None:
            return None
        users = self.extract_user_credentials(decoded)
        if users is None:
            return None
        email, password = users

        user = self.user_object_from_credentials(email, password)

        return user
