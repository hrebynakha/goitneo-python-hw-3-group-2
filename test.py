""" File for tests"""

from datetime import datetime
from models import AddressBook, Record

book = AddressBook()
value = "10.12.2000"
datetime_object = datetime.strptime(value, "%d.%m.%Y")

# print(datetime_object)
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane", birthday="07.03.2000")
jane_record.add_phone("9876543210")
print("jane record", jane_record.birthday.date)
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")
john.add_birthday("06.03.2022")


ls = book.list_contacts()
print(ls)
days_of_birthday = book.get_birthdays_per_week()
print("daye", days_of_birthday)
for day, users_to_greet in days_of_birthday.items():
    print(f"{day}:", end=" ")
    print(*users_to_greet, sep=", ")
print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555
john.remove_phone(found_phone)
# Видалення запису Jane
print(book.delete("Jane"))
