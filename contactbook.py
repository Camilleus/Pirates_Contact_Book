import csv
import re
from datetime import date, datetime, timedelta
from custom_errors import WrongInputError
import pandas as pd


class Contact:
    def __init__(self, name, last_name, address, phone, email, date_of_birth):
        self.name = name   # Ew. ograniczenie ilości znaków
        self.last_name = last_name  # Ew. ograniczenie ilości znaków
        self.address = address  # Ew. ograniczenie ilości znaków
        self.phone = phone  # Sprawdzanie poprawności wprowadzonego numeru telefonu
        self.email = email  # Sprawdzanie poprawności wprowadzonego email
        # Sprawdzanie poprawności formatu wprowadzonej daty urodzin
        self.date_of_birth = date_of_birth
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
    def add_contact(self):
        with open("contact_book.csv", "a", newline="") as fh:
            field_names = ["name", "last name", "address",
                           "phone", "email", "date_of_birth"]
            writer = csv.DictWriter(fh, fieldnames=field_names)
            writer.writeheader()
            writer.writerow()  # Instancja klasy Contact w formie słownika

    def edit_contact(self):
        pass

    def remove_contact(self, name, last_name):
        df = pd.read_csv('contact_book.csv')
        indexDelete = df[(df['name'] == name) & (
            df['last name'] == last_name)].index
        df.drop(indexDelete, inplace=True)
        df.to_csv('contact_book.csv')

    def search(self):
        pass

    def show_all_contacts(self):
        with open('contact_book.csv', newline='') as fh:
            reader = csv.DictReader(fh)
            result_list = []
            for row in reader:
                result_list.append(row)
            return result_list

    def birthdays_in_dyas_range(self, days_range):
        start_date = datetime.now()
        end_date = datetime.now() + timedelta(days=days_range)
        init_list = []
        with open('contact_book.csv', newline='') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                if row["date_of_birth"]:
                    date_obj = datetime.strptime(
                        row["date_of_birth"], '%Y-%m-%d')
                    date_start_year = datetime(year=start_date.year,
                                               month=date_obj.month, day=date_obj.day)
                    date_end_year = datetime(year=end_date.year,
                                             month=date_obj.month, day=date_obj.day)
                    if start_date < date_start_year <= end_date or start_date < date_end_year <= end_date:
                        init_list.append(row)
                else:
                    pass
            if init_list:
                list_sorted = sorted(
                    init_list, key=lambda row: row["date_of_birth"][5:])
                final_list = []
                for element in list_sorted:
                    date_obj = datetime.strptime(
                        element["date_of_birth"], '%Y-%m-%d')
                    date_to_check = datetime(year=start_date.year,
                                             month=date_obj.month, day=date_obj.day)
                    if date_to_check < start_date:
                        date_to_cal = datetime(
                            year=start_date.year+1, month=date_obj.month, day=date_obj.day)
                        delta = date_to_cal - start_date
                        element['to_birthday'] = str(delta.days)
                        final_list.append(element)
                    else:
                        date_to_cal = datetime(
                            year=start_date.year, month=date_obj.month, day=date_obj.day)
                        delta = date_to_cal - start_date
                        element['to_birthday'] = str(delta.days)
                        final_list.append(element)
                return final_list
            else:
                return 'No one has a birthday in the given range of days'
