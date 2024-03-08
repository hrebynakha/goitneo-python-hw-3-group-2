""" Models for CLI bot assistan"""

from collections import UserDict, defaultdict
from datetime import datetime, timedelta
from exceptions import PhoneNotCorrectError, PhoneNotFound, BirthDayNotCorrect


class Field:
    """Base class for field"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Name class"""


class Birthday(Field):
    """Birthday class"""

    def __init__(self, date):
        self.__date = None
        self.date = date
        super().__init__(date)

    def __str__(self):
        return self.__date.strftime("%d.%m.%Y")

    @property
    def date(self):
        """Return datetime.date() of birthday object"""
        return self.__date.date()

    @date.setter
    def date(self, date):
        """Setter for birthday date"""
        try:
            datetime_object = datetime.strptime(date, "%d.%m.%Y")
        except ValueError as exc:
            raise BirthDayNotCorrect from exc
        self.__date = datetime_object


class Phone(Field):
    """Phone class"""

    def __init__(self, phone):
        if not len(phone) == 10 or not phone.isnumeric():
            raise PhoneNotCorrectError
        super().__init__(phone)


class Record:
    """Class for record"""

    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def __str__(self):
        return (
            f"Contact name: {self.name.value}, "
            + f"birthday {self.birthday}, "
            + f"phones: {'; '.join(p.value for p in self.phones)}"
        )

    def add_phone(self, phone):
        """Add new phone object"""
        phone = Phone(phone)
        self.phones.append(phone)

    def remove_phone(self, phone):
        """Remvoe phone from list"""
        self.phones.remove(phone)

    def edit_phone(self, current_phone, new_phone):
        """Edit exist phone object"""
        for phone in self.phones:
            if phone.value == current_phone:
                phone.value = new_phone

    def find_phone(self, searching_phone):
        """Find phone in records"""
        for phone in self.phones:
            if phone.value == searching_phone:
                return phone
        raise PhoneNotFound

    def add_birthday(self, birthday):
        """Add birthday method"""
        self.birthday = Birthday(birthday)


class AddressBook(UserDict):
    """Address book"""

    def list_contacts(self):
        """Return list of contacts"""
        return self.data

    def add_record(self, record):
        """Adding record to address book"""
        self.data.update({record.name.value: record})

    def find(self, record_key):
        """Find record in list"""
        return self.data.get(record_key)

    def delete(self, record):
        """Deleting record from liss"""
        self.data.pop(record)

    def get_birthdays_per_week(self):
        """Return names of users that you need to greet with birstday"""
        days_of_birthday = defaultdict(list)
        today = datetime.today().date()
        for _, user in self.data.items():
            if not user.birthday:
                continue
            name = user.name.value
            birthday = user.birthday.date
            birthday_this_year = birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
            delta_days = (birthday_this_year - today).days
            if delta_days < 7:
                if birthday_this_year.weekday() in range(5, 7):
                    days_to_append = 7 % birthday_this_year.weekday()
                    birthday_this_year = birthday_this_year + timedelta(
                        days=days_to_append
                    )
            delta_days = (birthday_this_year - today).days
            if delta_days < 7:
                day_of_week = birthday_this_year.strftime("%A")
                days_of_birthday[day_of_week] += [name]

        return days_of_birthday
