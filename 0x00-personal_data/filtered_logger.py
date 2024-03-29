#!/usr/bin/env python3
"""Module for log data"""


import re
from typing import List
import logging
import mysql.connector
import os

# fields to fetch PII fields from
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Returns the log messaged obfuscated"""
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the redaction formater"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log message and redact sensitive fields"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        filters = super(RedactingFormatter, self).format(record)
        return filters


def get_logger() -> logging.Logger:
    """Logger funtion"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database"""
    db = mysql.connector.connect(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD"),
        host=os.getenv("PERSONAL_DATA_DB_HOST"),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )
    return db


def main():
    """Main function to retriev logs, takes nothing and returns nothing"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    names = [name[0] for name in cursor.description]

    logger = get_logger()
    for row in cursor:
        row_info = ''.join(f'{i}={str(j)}; ' for i, j in zip(row, row_info))
        logger.info(row_info.strip())

    cursor.close()
    db.close()
