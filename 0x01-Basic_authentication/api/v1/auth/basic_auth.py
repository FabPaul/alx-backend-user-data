#!/usr/bin/env python3
"""Baisc auth class module"""

from api.v1.auth.auth import Auth
import base64


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
