"""Module name"""
import argparse
import math
import sys
import os
import magic
import csv
import tempfile


PERCENTAGE = 0.75


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


def write_file(file_path, data):
    """Write strings in the file provided

    Args:
        file_path (str): Path of the file
        data (str): String that will be written in the file
    """
    with open(file_path, "w") as file:
        file.write(data)
    file.close()


def output_results():
    """Prints as an output one column list of numbers that exists in at least 75%
    of the csv files given.
    """
    top_number = math.ceil(len(arguments.csv_files) * PERCENTAGE) - 1
    folder = tempfile.mktemp()
    os.mkdir(folder)
    try:
        for file in arguments.csv_files:
            with open(file, newline='') as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                for number, row in enumerate(reader, 1):
                    first_column = int(row[0])
                    data_file = os.path.join(
                        folder, "{}.txt".format(first_column))
                    if os.path.isfile(data_file):
                        data = int(open(data_file, "r").readlines()[0])
                        if data == top_number:
                            print(first_column)
                            os.remove(data_file)
                        else:
                            write_file(data_file, str(data + 1))
                    else:
                        write_file(data_file, "1")

    except ValueError as error:
        print(error, "Error in line {} in file {}".format(number, file))
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
