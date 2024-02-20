#!/usr/bin/env python3
"""Hash pasword module"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Generate a salted hash for the hash password"""
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_password
