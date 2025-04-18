from datetime import datetime, timedelta
from models.fields import Name, Birthday, Phone

# class Field:
#     def __init__(self, value):
#         self.value = value

#     def __str__(self):
#         return str(self.value)


# class Name(Field):
#     def __init__(self, value):
#         super().__init__(value)


# class Birthday(Field):
#     def __init__(self, value):
#         try:
#             date_value = datetime.strptime(value, "%d.%m.%Y").date()
#             super().__init__(date_value)
#         except ValueError:
#             raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)  
        self.phones = []  
        self.birthday = None  

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        if phone_obj.value not in self.phones:
            self.phones.append(phone_obj.value)

    def change_phone(self, old_phone, new_phone):
        try:
            index = self.phones.index(old_phone)
            self.phones[index] = new_phone
        except ValueError:
            raise ValueError("Old phone number not found.")

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        if self.birthday:
            return self.birthday.value.strftime("%d.%m.%Y")
        return "No birthday set"

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.today().date()
        next_birthday = self.birthday.value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

    def __str__(self):
        phones = ', '.join(self.phones)
        birthday = self.show_birthday()
        return f"Name: {self.name.value}, Phones: {phones}, Birthday: {birthday}"


class AddressBook:
    def __init__(self):
        self.records = {}

    def add_record(self, record):
        self.records[record.name.value] = record

    def find(self, name):
        return self.records.get(name)

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.records.values():
            if record.birthday:
                next_birthday = record.birthday.value.replace(year=today.year)
                if next_birthday < today:
                    next_birthday = next_birthday.replace(year=today.year + 1)

                delta_days = (next_birthday - today).days
                if 0 <= delta_days <= 7:
                    if next_birthday.weekday() in [5, 6]:  # Saturday or Sunday
                        next_birthday += timedelta(days=(7 - next_birthday.weekday()))

                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": next_birthday.strftime("%d.%m.%Y")
                    })

        return upcoming_birthdays
