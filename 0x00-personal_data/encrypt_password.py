#!/usr/bin/env python3
"""password encryption"""


import bcrypt


def hash_password(password: str) -> bytes:
    """Function to hash password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
