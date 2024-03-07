"""
The Python bot helper
"""

from models import AddressBook
from utils import (
    parse_input,
    handle_add,
    show_all_addresess,
    change_record_phone,
    show_phone,
    add_birthday,
    show_birthday,
    show_coming_birthdays,
    get_current_book,
    save_current_book,
)


def main():
    """Main function in Home work #3"""
    print("Welcome to the assistant bot!")
    book = AddressBook(get_current_book())
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_current_book(book)
            print("Good bye!")
            break
        if command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(handle_add(book, *args))
        elif command == "change":
            print(change_record_phone(book, *args))
        elif command == "phone":
            print(show_phone(book, *args))
        elif command == "all":
            print(
                show_all_addresess(
                    book,
                )
            )
        elif command == "add-birthday":
            print(add_birthday(book, *args))
        elif command == "show-birthday":
            print(show_birthday(book, *args))
        elif command == "birthdays":
            print(show_coming_birthdays(book, *args))
        else:
            print("Invalid command.")
        save_current_book(book)

if __name__ == "__main__":
    main()
