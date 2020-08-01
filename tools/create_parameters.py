# -*- coding: utf-8 -*-
"""Searches input files in the random_csv_files folder according
to the given argument number_of_files.
Then the module appends this files as parameters in the paramaters.txt file for further use."""

import argparse
import os
import sys
import random

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))
TEST_ROOT_FOLDER = os.path.join(THIS_FOLDER, "random_csv_files")
PARAMETERS_FILE = "parameters.txt"


class NoFolderFound(Exception):
    """Raises an expection when the random_csv_files folder doesn't exist."""


class NotEnoughFiles(Exception):
    """Raises an exception when the number of input files aren't enough
    comparing them to the number_of_files argument."""


def get_input_files():
    """Returns a list with all of input files.

    Returns
        (list): All random files created
    """
    input_files = []
    try:
        if not os.path.isdir(TEST_ROOT_FOLDER):
            raise NoFolderFound(
                "{} folder doesn't exists".format(TEST_ROOT_FOLDER))
        for root, _, files in os.walk(TEST_ROOT_FOLDER):
            for file in files:
                if file.endswith(".in"):
                    input_files.append(os.path.join(root, file))

        if len(input_files) < arguments.number_of_files:
            raise NotEnoughFiles("""There aren't enough input files to create the parameters
        number_of_files {} < input files {}""".format(arguments.number_of_files, len(input_files)))

    except NoFolderFound as error:
        print(error)
        sys.exit(0)

    except NotEnoughFiles as error:
        print(error)
        sys.exit(0)

    return input_files


def append_parameters(input_files):
    """Creates or appends paramaters to the parameters.txt file
    according to the number_of_files argument.

    Args:
        input_files (list): All random files created
    """
    write_list = []
    while len(write_list) < arguments.number_of_files:
        input_file_choice = random.choice(input_files)
        write_list.append(input_file_choice)
        input_files.remove(input_file_choice)
    execution_line = "python csv_interpreter_dict_map.py {}".format(
        " ".join(write_list))
    print("You can execute the csv_interpreter_dict_map.py with this parameters:")
    print(execution_line)
    parameters_file = open(PARAMETERS_FILE, "a")
    parameters_file.write(execution_line + "\n")
    parameters_file.close()
    print("The {} file has been updated".format(PARAMETERS_FILE))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Searches input files in the random_csv_files folder.
        Then the module append this files as parameters in the parameters.txt
        file for further use""")
    parser.add_argument('number_of_files', type=int,
                        help="""number of files that will be used as arguments
                        for the csv_interpreter.py script""")
    arguments = parser.parse_args()
    random_files = get_input_files()
    append_parameters(random_files)
