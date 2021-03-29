from sqlite3 import OperationalError
import sqlite3
import base64
import logging
logger = logging.getLogger(__name__)

DB = 'url.db'

def init_table():
    """
    Initialize table, create it if it does not exist
    """
    create_table = """
    CREATE TABLE URL (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        URL TEXT NOT NULL
    );
    """
    with sqlite3.connect(DB) as c:
        cursor = c.cursor()
        try:
            cursor.execute(create_table)
            # print("Table succesfully")
        except OperationalError:
            logger.info("Table has been created. Nothing to do here.")
            pass

def set_url(url):
    """
    Insert URL into the table
    """
    with sqlite3.connect(DB) as c:
        cursor = c.cursor()
        try:
            record = cursor.execute(
                'INSERT INTO URL (URL) VALUES (?)',
                [base64.urlsafe_b64encode(url)]
            )
            c.commit()
        except OperationalError as e:
            logger.exception(str(e))

        return record.lastrowid

def get_url(urlId):
    """
    Get the URL by row ID
    """
    with sqlite3.connect(DB) as c:
        cursor = c.cursor()
        # print(urlId)
        record = cursor.execute(
            'SELECT URL FROM URL WHERE ID=?', [urlId]
        )
        one = record.fetchone()
        if one is not None:
            return base64.urlsafe_b64decode(one[0])
        else:
            raise Exception("No corresponding URL entry is found")