""" Main functions for CLI bot"""

import pickle
from exceptions import (
    PhoneNotCorrectError,
    PhoneNotGiven,
    ContactAlredyExist,
    ContactNotFound,
    BirthDayNotCorrect,
)
from models import Record


def input_error(func):
    """Return error message if some function does not work with given args"""

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Given name not found in contacts"
        except TypeError:
            return "Given format not supported"
        except IndexError:
            return "Enter user name"
        except PhoneNotCorrectError:
            return "Given telephone number not correct"
        except ContactAlredyExist:
            return "Cannot add new contact. Alredy exist"
        except ContactNotFound:
            return "Cannot not found."
        except BirthDayNotCorrect:
            return "Give me correct date format DD.MM.YYYY"
        except PhoneNotGiven:
            return "Give me new telephone number"

    return inner


def load_error(func):
    """Return nothing if some function does not work"""

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            return None

    return inner


@input_error
def parse_input(user_input):
    """Parse user inputed commands"""
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def handle_add(book, *args):
    """Add record to address book"""
    name, phone = args
    if book.find(name):
        raise ContactAlredyExist
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)

    return "Contact added."


@input_error
def show_all_addresess(
    book,
):
    """Show all records in book"""
    info = ""
    for _, record in book.data.items():
        info += f"{record}\n"
    return info.removesuffix("\n")


@input_error
def find_record(book, name):
    """Show all address record in book"""
    record = book.find(name)
    if not record:
        raise ContactNotFound
    return record


@input_error
def show_phone(book, name):
    """Show phone by name"""
    record = book.find(name)
    if not record:
        raise ContactNotFound
    return record


@input_error
def change_record_phone(book, name, phone, new_phone=None):
    """Change phone for record"""
    record = book.find(name)
    if not record:
        raise ContactNotFound
    if not new_phone and len(record.phones) > 1:
        raise PhoneNotGiven("Give me new telephone number")
    if len(record.phones) == 1:
        new_phone = phone
        phone = record.phones[0].value
    record.edit_phone(phone, new_phone)
    return "Phone has been updated."


@input_error
def add_phone(book, name, phone):
    """Adding new other phone to contact record"""
    record = book.find(name)
    if not record:
        raise ContactNotFound
    record.add_phone(phone)
    book.add_record(record)
    return "Phone has been added."


@input_error
def remove_phone(book, name, phone):
    """Removing phone form contact record"""
    record = book.find(name)
    if not record:
        raise ContactNotFound
    record.remove_phone(phone)
    book.add_record(record)
    return "Phone has been deleted."


@input_error
def delete_address(book, name):
    """Deleting address in book"""
    book.delete(name)
    return "Contact deleted."


@input_error
def add_birthday(book, name, birthday):
    """Adding birthday to record"""
    record = book.find(name)
    if not record:
        raise ContactNotFound
    record.add_birthday(birthday)
    return "Birthday has been added."


@input_error
def show_birthday(book, name):
    """Adding birthday to record"""
    record = book.find(name)
    if not record:
        raise ContactNotFound
    return (
        record.birthday if record.birthday else "Birthday not defined for this contact"
    )


def show_coming_birthdays(
    book,
):
    """Return string of contatcs to greet with birthday in a week"""
    info = ""
    days_of_birthday = book.get_birthdays_per_week()
    for day, users_to_greet in days_of_birthday.items():
        info += f"{day}: "
        for user in users_to_greet:
            info += f" {user},"
        info = info.removesuffix(",")
        info += "\n"
    info = info.removesuffix("\n")
    return info if info else "There are no contacts to congratulate this week"


@load_error
def get_current_book():
    """Return serialized objects from local file if it exist"""
    file_name = "databot.bin"
    with open(file_name, "rb") as fh:
        unpacked = pickle.load(fh)
    return unpacked


@load_error
def save_current_book(book):
    """Save current state of address book to file"""
    file_name = "databot.bin"
    with open(file_name, "wb") as fh:
        pickle.dump(book, fh)
