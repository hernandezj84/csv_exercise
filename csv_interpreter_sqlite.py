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


class DataInteractions:
    """Sqlite3 connection object"""

    def __init__(self):
        """Constructor. Exposes methods that interacts with the sqlite3 database.

        """
        self.__conn = sqlite3.connect(DATABASE_FILE)
        self.__cursor = self.__conn.cursor()
        self.__cursor.execute(
            "CREATE TABLE IF NOT EXISTS data (key INTEGER PRIMARY KEY, value INTEGER)")
        self.__conn.commit()

    def get_number(self, number):
        """Search a given number in the database.

        Args:
            number (int): Number to be searched

        Returns:
            [int/boolean]: Number found in the database (int found/boolean not found)
        """
        sql_search = "SELECT value FROM data WHERE key = {}"
        result = self.__cursor.execute(sql_search.format(number)).fetchone()
        return result[0]

    def update_key(self, key, number):
        """Update the value of a given column if the number is found again in the csv files.

        Args:
            key (int): Column that is repeated in the csv files
            number (int): Times that the column is repeated in the csv files
        """
        sql_update = "UPDATE data SET value = {} WHERE key = {}"
        self.__cursor.execute(sql_update.format(key, number))

    def insert_new_key(self, key):
        """Insert a new key in the database when is the first time that the column is found.

        Args:
            key (int): New column found in the csv files.
        """
        sql_update = "UPDATE data SET value = {} WHERE key = {}"
        self.__cursor.execute(sql_update.format(key))

    def commit_changes(self):
        """Commit the changes made in the database

        """
        self.__conn.commit()


class InvalidFileException(Exception):
    """Custom exception that will raise when a given path isn't a valid file.
    """


def validate_arguments():
    """Raises an exception if any of the arguments aren't valid files.

    Raises:
        InvalidFileException: Raises if a given argument isn't a file.
        InvalidFileException: Raises if a given argument isn't a plain text file
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
    of the csv files given.
    """

    if os.path.isfile(DATABASE_FILE):
        os.remove(DATABASE_FILE)
    top_number = math.ceil(len(arguments.csv_files) * PERCENTAGE) - 1
    buffers = [open(csv_file, "r") for csv_file in arguments.csv_files]
    data = DataInteractions()
    try:
        for lines in zip_longest(*buffers, fillvalue=''):
            for line in lines:
                number = line.split(",")[0]
                if number != '':
                    number = int(number)
                    found_number = data.get_number(number)
                    if found_number is not None:
                        if found_number == top_number:
                            print(number)

                        else:
                            new_value = found_number + 1
                            data.update_key(number, new_value)

                    else:
                        data.insert_new_key(number)

        data.commit_changes()
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
