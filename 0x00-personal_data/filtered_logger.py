#!/usr/bin/env python3
"""Module for log data"""


import re


def filter_datum(fields, redaction, message, separator):
    """Returns the log messaged obfuscated"""
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message
