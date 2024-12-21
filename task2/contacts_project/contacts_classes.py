from collections import UserDict
from datetime import datetime, date, timedelta

class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError(f"Invalid phone number: {value}. "
                             f"It must contain exactly 10 digits.")
        super().__init__(value)
    def __str__(self):
        return f"{self.value}"


class Birthday(Field):
    def __init__(self, value):
        try:
            birthday_datatime=datetime.strptime(value,"%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    def add_birthday_method(self, birthday):
            self.birthday = Birthday(birthday)
    def add_phone(self,phone):
        self.phones.append(Phone(phone))
    def edit_phone(self, old_phone, new_phone):
        for idx, phone in enumerate(self.phones):
            if phone.value==old_phone:
                self.phones[idx]=Phone(new_phone)
                return
        raise ValueError(f"Phone number {old_phone} not found")
    def find_phone(self,search_phone):
        for phone in self.phones:
            if phone.value == search_phone:
                return phone
        return None
    def remove_phone(self,deleted_phone):
        self.phones = [phone for phone in self.phones if phone.value != deleted_phone]
    def __str__(self):
        return (f"Contact name: {self.name.value},"
                f" phones: {'; '.join(p.value for p in self.phones)},"
                f" birthday: {self.birthday if self.birthday else 'No information'}")


class AddressBook(UserDict):
    def __str__(self):
        return "\n".join(str(self.data.get(name)) for name in self.data.keys())
    def add_record(self,record):
        self.data.update({record.name.value:record})
    def find(self,name):
        return self.data.get(name)
    def delete(self,name):
        self.data.pop(name)
    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()
        for record in self.data.values():
            if record.birthday:
                birthday_this_year =datetime.strptime(record.birthday.value,"%d.%m.%Y").date().replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                if 0 <= (birthday_this_year - today).days <= days:
                    if birthday_this_year.weekday() >= 5:
                        birthday_this_year += timedelta(days=(7 - birthday_this_year.weekday()))
                    upcoming_birthdays.append(f"{record.name.value}: "
                                              f"congratulation {birthday_this_year.strftime('%d.%m.%Y')}")
        return upcoming_birthdays
