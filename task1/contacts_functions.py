from contacts_classes import AddressBook, Record
import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError):
            start_phrase="Enter the correct argument for the command\nCorrect format for input: "
            errors_dict={"add_contact":"'add [name] [phone number]\nPhone number must contain exactly 10 digits'",
                         "change_contact":"'change [name] [new phone number]\nPhone must contain exactly 10 digits'",
                         "show_phone":"'phone [name]'",
                         "add_birthday_func":"'add-birthday [name] [birthday in format: DD.MM.YYYY]'",
                         "show_birthday":"'show-birthday [name]'",
                         "birthdays":"'birthdays'"}
            return start_phrase+errors_dict[func.__name__]
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book:AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        return "Error. Contact not found"

@input_error
def show_phone(args, book:AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        phones = ", ".join(str(phone) for phone in record.phones)
        return phones
    else:
        return "Error. Contact not found"

def show_all(book:AddressBook):
    contacts_pretty_string="\n All contacts:\n"
    for v in book.values():
        contacts_pretty_string+=f"{v}\n"
    return contacts_pretty_string if book.values() else "\nAddressBook is empty.\n"

@input_error
def add_birthday_func(args, book:AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    record.add_birthday_method(birthday)
    return "Birthday added"

@input_error
def show_birthday(args, book:AddressBook):
    name, *_ = args
    record = book.find(name)
    return record.birthday.value if record.birthday else 'No information'

@input_error
def birthdays(book:AddressBook):
    upcoming_birthdays=book.get_upcoming_birthdays()
    return "\n".join(upcoming_birthdays) if upcoming_birthdays else "No upcoming birthdays."
