from models.address_book import AddressBook
from models.record import Record
from utils.command_handlers import add_birthday, show_birthday, birthdays
from utils.storage import load_data, save_data

# book = load_address_book("contacts.bin")
book = load_data()
if book is None:
    book = AddressBook()

def main(book):
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.split()

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            if len(args) >= 2:
                name, phone = args[0], args[1]
                try:
                    record = book.records.get(name)
                    message = "Contact updated."
                    if record is None:
                        record = Record(name)
                        book.add_record(record)
                        message = "Contact added."
                    record.add_phone(phone)
                    print(message)
                except ValueError as e:
                    print(f"Error: {e}")

        elif command == "change":
            if len(args) == 3:
                name, old_phone, new_phone = args
                record = book.records.get(name)
                if record and old_phone in record.phones:
                    record.change_phone(old_phone, new_phone)
                    print(f"Phone for {name} updated to {new_phone}.")
                else:
                    print("Phone number not found for contact.")

        elif command == "phone":
            if args:
                name = args[0]
                record = book.records.get(name)
                if record:
                    print(f"Phone numbers for {name}: {', '.join(record.phones)}")
                else:
                    print("Contact not found.")

        elif command == "all":
            print("Contacts:")
            for name, record in book.records.items():
                print(f"{name}: {', '.join(record.phones)}")

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main(book)
