"""
error_logger.py
This file contains the error logger function.
"""

from datetime import date
ERROR_PATH = "./error.txt"


def log_error(message: str) -> None:
    """
    This function logs errors with the current date and the given error to an error file
    :param message: The message that describes the error
    :return: None
    """
    with open(ERROR_PATH, mode='a', encoding='utf-8') as error_file:
        error_file.write(f"{date.today()} {message} \n")

if __name__ == '__main__':
    log_error("test")