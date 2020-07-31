"""Module name"""
import argparse
import math
from itertools import zip_longest
import magic
import sys
import os
import sqlite3

PERCENTAGE = 0.75
DATABASE_FILE = "database.db"


class Database:
    """Sqlite3 connection object"""

    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_FILE)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS data (key INTEGER PRIMARY KEY, value INTEGER)")
        self.conn.commit()


class InvalidFileException(Exception):
    """Custom exception that will raise when a given path isn't a valid file"""


def validate_arguments():
    """Raises an exception if any of the arguments aren't valid files.
    """
    try:
        mimetype = magic.Magic(mime=True)
        for file in arguments.csv_files:
            if not os.path.isfile(file):
                raise InvalidFileException(
                    "Error path {} is not a valid file".format(file))
            if mimetype.from_file(file) != "text/plain":
                raise InvalidFileException(
                    "Error file {} is not a plain text file".format(file))

    except InvalidFileException as error:
        print(error)
        sys.exit(0)


def output_results():
    """Prints as an output one column list of numbers that exists in at least 75%
    of the csv files given."""

    if os.path.isfile(DATABASE_FILE):
        os.remove(DATABASE_FILE)
    top_number = math.ceil(len(arguments.csv_files) * PERCENTAGE) - 1
    buffers = [open(csv_file, "r") for csv_file in arguments.csv_files]
    database = Database()
    sql_search = "SELECT value FROM data WHERE key = {}"
    sql_update = "UPDATE data SET value = {} WHERE key = {}"
    sql_insert = "INSERT INTO data (key, value) VALUES ({}, 1)"
    sql_delete = "DELETE FROM data WHERE key = {}"
    try:
        for lines in zip_longest(*buffers, fillvalue=''):
            for line in lines:
                number = line.split(",")[0]
                if number != '':
                    number = int(number)
                    data = database.cursor.execute(
                        sql_search.format(number)).fetchone()
                    if data is not None:
                        if data[0] == top_number:
                            print(number)
                            database.cursor.execute(sql_delete.format(number))

                        else:
                            new_value = data[0] + 1
                            database.cursor.execute(sql_update.format(
                                new_value, number))

                    else:
                        database.cursor.execute(
                            sql_insert.format(number))
        database.conn.commit()
    except ValueError as error:
        print(error)
        sys.exit(1)


def main():
    """Module name"""
    list_numbers = []
    free_number = math.ceil(len(arguments.csv_files) * PERCENTAGE) - 1
    buffers = [open(csv_file, "r") for csv_file in arguments.csv_files]
    try:
        for lines in zip_longest(*buffers, fillvalue=''):
            for line in lines:
                number = int(line.split(",")[0])
                counter = list_numbers.count(number)
                if counter == free_number:
                    list_numbers.sort()
                    number_position = list_numbers.index(number)
                    list_numbers = list_numbers[number_position:]
                    print(number, len(list_numbers))

                    for _ in range(free_number):
                        list_numbers.remove(number)

                elif number != '':
                    list_numbers.append(number)
                    list_numbers.sort()
    except ValueError as error:
        print(error)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Returns the list of numbers that exists in
        at least 75% on given .csv format files""")
    parser.add_argument('csv_files', type=str, nargs='+',
                        help='csv files path as parameters separated by spaces')
    arguments = parser.parse_args()
    validate_arguments()
    output_results()
