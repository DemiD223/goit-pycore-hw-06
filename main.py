from collections import UserDict


class Field:
    # Base class for record fields
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # Contact name, required field
    pass


class Phone(Field):
    # Phone number with validation: exactly 10 digits
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)


class Record:
    # Contact with a name and a list of phones
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        # Add a new phone to the contact
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        # Remove a phone if it exists
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)

    def edit_phone(self, old_phone, new_phone):
        # Replace an old phone with a new one
        phone_obj = self.find_phone(old_phone)
        if not phone_obj:
            raise ValueError("Phone not found")
        new_phone_obj = Phone(new_phone)
        index = self.phones.index(phone_obj)
        self.phones[index] = new_phone_obj

    def find_phone(self, phone):
        # Return the Phone object or None
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    # Stores records by contact name
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        # Return a record by name or None
        return self.data.get(name)

    def delete(self, name):
        # Delete a record by name if it exists
        if name in self.data:
            del self.data[name]


if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    book.delete("Jane")