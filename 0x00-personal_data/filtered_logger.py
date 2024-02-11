#!/usr/bin/env python3
"""Module for log data"""


import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str):
    """Returns the log messaged obfuscated"""
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message
