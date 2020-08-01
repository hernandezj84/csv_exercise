# -*- coding: utf-8 -*-
"""Helps to create random list for creating random csv_files"""
import random
import csv


def get_ordered_first_column(list_size):
    """Returns a random ordered list.

    Args:
        list_size (int): Size of the ordered list to be returned

    Returns:
        ordered_list (list): Ordered list with gaps or without gaps
    """
    ordered_list = list(range(1, int(list_size * (1 + random.random()))))

    if len(ordered_list) < list_size:
        ordered_list.append(max(ordered_list) + 1)

    while not len(ordered_list) == list_size:
        ordered_list.remove(random.choice(ordered_list))

    return ordered_list


def get_hexadecimal_random_number():
    """Returns a random hexadecimal number.

    Returns:
        random_hex_str (str): Random hexadecimal number with fixed 16 positions
    """
    return "".join([random.choice('0123456789abcdef') for _ in range(16)])


def get_text_random_column():
    """Returns a random text list given fixed values.

        Returns:
            random_text (str): Random str with already  fixed texts

    """
    texts = ["start", "xterm", "error,content_message", "warn", " "]
    return random.choice(texts)


def create_csv_file(list_size, file_path):
    """Creates a random columns csv file.

    """
    print("Creating file {}.in with {} lines".format(file_path, list_size))
    first_column = get_ordered_first_column(list_size)
    second_column = [get_hexadecimal_random_number()
                     for _ in range(list_size)]
    last_column = [get_text_random_column()
                   for _ in range(list_size)]
    csv_file = open("{}.in".format(file_path), "w")
    csv_writer = csv.writer(
        csv_file, delimiter=",", quoting=csv.QUOTE_NONE, quotechar='', escapechar=' ', lineterminator="\n")
    csv_writer.writerows(zip(first_column, second_column, last_column))
    csv_file.close()
