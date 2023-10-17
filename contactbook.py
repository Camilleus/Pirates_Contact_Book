import csv
import re
from datetime import date, datetime, timedelta
from custom_errors import WrongInputError
import os.path


class Contact:
    def __init__(self, name, last_name, phone, email=None, date_of_birth=None, address=None, note=None):
        self.name = name
        self.last_name = last_name
        self.address = address
        self.phone = phone
        self.email = email
        self.date_of_birth = date_of_birth
        self.note = note

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, new_phone: str) -> None:
        pattern = re.compile("(?:\+\d{1,3} ?)?(?:\d[- ]?){8}\d")
        if not pattern.fullmatch(new_phone):
            raise WrongInputError(f"Incorrect phone number: {new_phone}")
        else:
            normalized_phone_num = ''.join(
                filter(lambda char: char.isdigit(), new_phone))
            self._phone = normalized_phone_num

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email: str) -> None:
        pattern = re.compile("[a-zA-Z][\w.-]+@\w+\.\w{2,}")
        if not pattern.fullmatch(new_email):
            raise WrongInputError(f"Incorrect email: {new_email}")
        else:
            self._email = new_email

    @property
    def date_of_birth(self):
        return self._date_of_birth

    @date_of_birth.setter
    # date expected to be in dd.mm.yyyy format
    def date_of_birth(self, new_date_of_birth: str) -> None:
        pattern = re.compile("\d{2}\.\d{2}\.\d{4}")
        if not pattern.fullmatch(new_date_of_birth):
            raise WrongInputError(
                f"Incorrect date format: {new_date_of_birth}")
        ymd_int_date_of_birth = [
            int(str_number) for str_number in new_date_of_birth.split('.')][::-1]
        try:
            self._date_of_birth = date(*ymd_int_date_of_birth)
        except ValueError as e:
            if str(e) == 'month must be in 1..12':
                raise WrongInputError('Incorrect month number')
            elif str(e) == 'day is out of range for month':
                raise WrongInputError('Wrong day number for this month')
            else:
                raise ValueError(e)


class ContactBook:
    def __init__(self, contact_book_file_path="contact_book.csv"):
        self.contact_book_file_path = contact_book_file_path
        self.field_names = ["name", "last name", "phone", "email", "date_of_birth", "address", "note"]

        if not os.path.isfile(self.contact_book_file_path):
            with open(self.contact_book_file_path, 'w', newline='') as fh:
                writer = csv.DictWriter(fh, fieldnames=self.field_names)
                writer.writeheader()
    def add_contact(self, contact):
        contact = contact.__dict__
        with open(self.contact_book_file_path, "a", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=self.field_names)
            writer.writerow(contact)

    def edit_contact(self, info):
        pass

    def remove_contact(self):
        pass

    def search_contact(self, text):
        with open(self.contact_book_file_path, "r", newline="") as fh:
            reader = csv.reader(fh)

            for row in reader:
                row_string = ",".join(row[:-1]).casefold()
                if row_string.find(text.casefold()) >= 0:
                    return dict(zip(self.field_names, row))
                else:
                    return "Contact not found"

    def show_all_contacts(self):
        with open('contact_book.csv', newline='') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                print(row["name"], row['last_name'], row['address'],
                      row['phone'], row['email'], row['date_of_birth'])

    def birthdays_in_dyas_range(self, days_range):
        start_date = datetime.now()
        end_date = datetime.now() + timedelta(days=days_range)
        result_list = []
        with open('contact_book.csv', newline='') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                date_obj = datetime.strptime(
                    row["date_of_birth"], '%Y-%m-%d')
                date_start_year = datetime(year=start_date.year,
                                           month=date_obj.month, day=date_obj.day)
                date_end_year = datetime(year=end_date.year,
                                         month=date_obj.month, day=date_obj.day)
                if start_date < date_start_year or date_end_year <= end_date:
                    result_list.append(row)
        return result_list
