""" Execption for CLI bot"""


class PhoneNotCorrectError(Exception):
    """Phone not match error"""

class PhoneNotGiven(Exception):
    """Phone number not given"""

class ContactAlredyExist(Exception):
    """Contac alredy exist in address book"""


class ContactNotFound(Exception):
    """Contact not found"""


class PhoneNotFound(Exception):
    """Not found phones in records"""


class BirthDayNotCorrect(Exception):
    """Not correct format for birthday , need to use DD.MM.YYYY format"""
