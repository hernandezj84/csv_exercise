"""Returns (as an output) one column list of numbers that exists
 in at least 75% of csv files received as arguments.
"""
import argparse
import csv
import os
import sys
import magic


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


def read_csv_file():
    """Reads the first column of the csv files.

    Returns
        first_column_values (dict): Maps and adds every number on the csv_files
    """
    first_column_values = {}
    try:
        for file in arguments.csv_files:
            with open(file, newline='') as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                for number, row in enumerate(reader, 1):
                    first_column = int(row[0])
                    if first_column in first_column_values:
                        first_column_values[first_column] += 1
                    else:
                        first_column_values[first_column] = 1

    except ValueError as error:
        print(error, "Error in line {} in file {}".format(number, file))
        sys.exit(1)
    return first_column_values


def output_results(map_values):
    """Prints as an output one column list of numbers that exists in at least 75%
    of the csv files given.

    Args:
        map_values (dict): Has the values (times of existing) of the first column of every file
    """
    percentage = 0.75
    number_of_files = len(arguments.csv_files)
    ordered_values = list(set(map_values.keys()))
    for value in ordered_values:
        if map_values[value] / float(number_of_files) >= percentage:
            print(value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Returns the list of numbers that exists in
        at least 75% on given .csv format files""")
    parser.add_argument('csv_files', type=str, nargs='+',
                        help='csv files path as parameters separated by spaces')
    arguments = parser.parse_args()
    validate_arguments()
    result_dict = read_csv_file()
    output_results(result_dict)
