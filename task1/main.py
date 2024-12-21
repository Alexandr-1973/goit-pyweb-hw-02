from contacts_functions import (parse_input, add_contact, change_contact, show_phone,
show_all, add_birthday_func, show_birthday, birthdays, save_data, load_data)
from abc import ABC, abstractmethod

class UserView(ABC):

    @abstractmethod
    def show_welcome_message(self):
        pass

    @abstractmethod
    def show_error_message(self, message: str):
        pass

    @abstractmethod
    def show_message(self, message: str):
        pass

    @abstractmethod
    def show_contacts(self, contacts: str):
        pass

    @abstractmethod
    def show_upcoming_birthdays(self, birthdays: str):
        pass

    @abstractmethod
    def show_contact_info(self, contact_info: str):
        pass

class ConsoleView(UserView):

    def show_welcome_message(self):
        print("Welcome to the assistant bot!")

    def show_error_message(self, message: str):
        print(f"Error: {message}")

    def show_message(self, message: str):
        print(message)

    def show_contacts(self, contacts: str):
        print(contacts)

    def show_upcoming_birthdays(self, birthdays: str):
        print(birthdays)

    def show_contact_info(self, contact_info: str):
        print(contact_info)

def main():
    book = load_data()
    view = ConsoleView()
    view.show_welcome_message()
    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            print("Please enter a command.")
            continue
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            view.show_message("Good bye!")
            break
        elif command == "hello":
            view.show_message("How can I help you?")
        elif command == "add":
            view.show_message(add_contact(args, book))
        elif command == "change":
            view.show_message(change_contact(args, book))
        elif command == "phone":
            view.show_contact_info(show_phone(args, book))
        elif command == "all":
            view.show_contacts(show_all(book))
        elif command == "add-birthday":
            view.show_message(add_birthday_func(args, book))
        elif command == "show-birthday":
            view.show_message(show_birthday(args, book))
        elif command == "birthdays":
            view.show_upcoming_birthdays(birthdays(book))
        else:
            view.show_error_message("Invalid command.")

if __name__ == "__main__":
    main()