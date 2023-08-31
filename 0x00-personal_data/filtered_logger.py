#!/usr/bin/env python3
""" A Module contauining an obfuscated log message """
import logging
import os
import re
from mysql.connector import connection
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """ returns the log message obfuscated """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction + separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """
        Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = None):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = list(fields) if fields else []

    def format(self, record: logging.LogRecord) -> str:
        return filter_datum(self.fields,
                            RedactingFormatter.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            RedactingFormatter.SEPARATOR)


def get_logger() -> logging.Logger:
    """ Returns a logger object from the logging module """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """ returns a connection object to a database """
    return connection.MySQLConnection(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME', 'holberton'))


def main() -> None:
    """ Main function to run the nodule if not imported """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = [desc[0] for desc in cursor.description]
    for row in cursor.fetchall():
        message = '; '.join(
            f'{fields[idx]}={row[idx]}' for idx in range(len(fields)))
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
