"""Creates multiple csv format files for testing purposes
"""

import argparse
import os
import csv_file_creator as csv_creator

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))
TEST_ROOT_FOLDER = os.path.join(THIS_FOLDER, "random_csv_files")
TEST_FOLDER_NAME = "random_csv_files"


def create_csv_files(path):
    """Creates the csv files in the path folder according to the
    arguments number_of_files and number_of_lines

        Args:
            path (str): the folder path where the files are going
            to be generated
    """
    for number, _ in enumerate(range(arguments.number_of_files), 1):
        file_path = os.path.join(path, "file{}".format(number))
        csv_creator.create_csv_file(arguments.number_of_lines, file_path)


def create_root_test_folder():
    """Creates the TEST_ROOT_FOLDER folder"""
    if not os.path.exists(TEST_ROOT_FOLDER):
        os.mkdir(TEST_ROOT_FOLDER)


def get_max_number_from_folder():
    """Returns the number of the last folder created `test_csv_files_*` if it exists.

    Returns:
        (int): The number of the last folder created
    """
    latest_folder_number = 0
    test_folders = []
    for folder in os.listdir(TEST_ROOT_FOLDER):
        if os.path.isdir(os.path.join(TEST_ROOT_FOLDER, folder)) and folder.startswith(TEST_FOLDER_NAME):
            test_folders.append(folder)
    if len(test_folders) > 0:
        latest_folder_number = max(
            [int(folder.split("_")[3])for folder in test_folders])
        latest_folder_number += 1
    return latest_folder_number


def create_test_folder():
    """Creates a new folder path according to the arguments acquired.

    Returns:
        (str): Name of the new test folder where the files will be created
    """
    latest_folder_number = get_max_number_from_folder()
    test_folder_name = TEST_FOLDER_NAME + \
        "_{}_{}_{}".format(latest_folder_number,
                           arguments.number_of_files, arguments.number_of_lines)
    test_folder_complete_name = os.path.join(
        TEST_ROOT_FOLDER, test_folder_name)
    os.mkdir(test_folder_complete_name)
    return test_folder_complete_name


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates test csv files")
    parser.add_argument('number_of_files', type=int,
                        help="number of test files to create")
    parser.add_argument('number_of_lines', type=int,
                        help="number of lines for each file")
    arguments = parser.parse_args()
    create_root_test_folder()
    test_folder = create_test_folder()
    create_csv_files(test_folder)
