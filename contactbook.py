import csv


class Contact:
    def __init__(self, name, last_name, address, phone, email, date_of_birth):
        self.name = name   # Ew. ograniczenie ilości znaków
        self.last_name = last_name  # Ew. ograniczenie ilości znaków
        self.address = address  # Ew. ograniczenie ilości znaków
        self.phone = phone  # Sprawdzanie poprawności wprowadzonego numeru telefonu
        self.email = email  # Sprawdzanie poprawności wprowadzonego email
        self.date_of_birth = date_of_birth  # Sprawdzanie poprawności formatu wprowadzonej daty urodzin
        self.contact = {
            "name": self.name,
            "last name": self.last_name,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "date_of_birth": self.date_of_birth
            }

    @property
    def phone(self):
        pass

    @phone.setter
    def phone(self, new_phone):
        pass

    @property
    def email(self):
        pass

    @email.setter
    def email(self, new_email):
        pass

    @property
    def date_of_birth(self):
        pass

    @date_of_birth.setter
    def date_of_birth(self, new_date_of_birth):
        pass


class ContactBook:
    def add_contact(self):
        with open("contact_book.csv", "a", newline="") as fh:
            field_names = ["name", "last name", "address", "phone", "email", "date_of_birth"]
            writer = csv.DictWriter(fh, fieldnames=field_names)
            writer.writeheader()
            writer.writerow() #Instancja klasy Contact w formie słownika

    def edit_contact(self):
        pass

    def remove_contact(self):
        pass

    def search(self):
        pass

    def show_all_contacts(self):
        pass

    def birthday_of_contact(self, days_to_birthday):
        pass