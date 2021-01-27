import sqlite3
from sqlite3 import Error
from datetime import datetime

connection = None


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


create_nmb_table = """
CREATE TABLE IF NOT EXISTS numbers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  number INTEGER NOT NULL,
  datetime TEXT NOT NULL
);
"""

create_log_table = """
CREATE TABLE IF NOT EXISTS logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  number INTEGER NOT NULL,
  datetime TEXT NOT NULL,
  info TEXT
);
"""


def add_numbers(n):
    return """
INSERT INTO
  numbers (number, datetime)
VALUES
  ({},'{}');""".format(n, str(datetime.now()))


def add_logs(n, info):
    return """
INSERT INTO
  logs (number, datetime, info)
VALUES
  ({},'{}','{}');
""".format(n, str(datetime.now()), info)


def number_is(n):
    return """
SELECT
  number, datetime
FROM
  numbers
WHERE
  number={} or number = {}
""".format(n, n+1)


def create_tables():
    execute_query(connection, create_nmb_table)
    execute_query(connection, create_log_table)


def add_number(n):
    return execute_query(connection, add_numbers(n))


def add_log(n, info):
    execute_query(connection, add_logs(n, info))


def number_in(n):
    number = execute_read_query(connection, number_is(n))
    if (len(number) > 0):
        return True
    else:
        return False


def logs():
    return execute_read_query(connection, """SELECT * FROM logs""")


def numbers():
    return execute_read_query(connection, """SELECT * FROM numbers""")


def delete():
    execute_read_query(connection, """DELETE FROM numbers""")
    execute_read_query(connection, """DELETE FROM logs""")
    return True
