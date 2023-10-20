import csv
import re
from datetime import date, datetime, timedelta
from custom_errors import WrongInputError
import pandas as pd
import os.path
import pandas

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
        if not new_phone: return
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
        if not new_email: return
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
        if not new_date_of_birth: return
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

        self.field_names = ["name", "last_name", "_phone", "_email", "_date_of_birth", "address", "note", "tags"]

        if not os.path.isfile(self.contact_book_file_path):
            df = pandas.DataFrame(columns=self.field_names)
            df.to_csv(self.contact_book_file_path)

    def add_contact(self, new_contact):
        new_contact = [new_contact.__dict__]
        for contact in new_contact:
            if contact["note"]:
                contact["note"] = contact["note"].note_contents
        df = pandas.DataFrame(new_contact, columns=self.field_names)
        df.index=[df.index[-1]+1]
        df.to_csv(self.contact_book_file_path, mode="a", index=True, header=False)

    def edit_contact(self, no_contact, data_modified, something):
        reader = pandas.read_csv(self.contact_book_file_path)
        reader.loc["id_contact", data_modified] = something
        reader.to_csv((self.contact_book_file_path))

    def remove_contact(self, no_contact):
        pass

    def search_contact(self, phrase):
        with open(self.contact_book_file_path, "r", newline="") as fh:
            reader = csv.reader(fh)
            results = []
            next(reader)
            for row in reader:
                row_string = ",".join(row[:-2]).casefold()
                if row_string.find(phrase.casefold()) >= 0:
                    results.append(dict(zip(['id']+self.field_names, row)))
        if results:
            return results
        else:
            return "Contact not found"

    def show_all_contacts(self):
        with open('contact_book.csv', newline='') as fh:
            list_of_contacts = []
            reader = csv.DictReader(fh)
            for row in reader:
                list_of_contacts.append(row)
            return list_of_contacts

  def search_note_by_tags(self,searched_tags)->dict[str:str]:
            if isinstance(searched_tags,str):
                searched_tags=searched_tags.split('#')[1:]
            answer_dict=dict()
            with open(self.contact_book_file_path,'r') as fh:
                list_of_contacts=csv.DictReader(fh,self.field_names)
                for contact in list_of_contacts:
                    is_tag_in_notetags=True
                    tags=contact['tags'].split('#')
                    if not tags: continue
                    for tag in searched_tags:
                        if not contact['note'] or tag not in tags:
                            is_tag_in_notetags=False
                    if is_tag_in_notetags: answer_dict.update({" ".join([contact['name'],contact['last_name']]):contact['note']})
            return answer_dict

    def birthdays_in_days_range(self, days_range):
        start_date = datetime.now()
        end_date = datetime.now() + timedelta(days=days_range)
        init_list = []
        with open('contact_book.csv', newline='') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                if row["_date_of_birth"]:
                    date_obj = datetime.strptime(
                        row["_date_of_birth"], '%Y-%m-%d')

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
                    init_list, key=lambda row: row["_date_of_birth"][5:])
                final_list = []
                for element in list_sorted:
                    date_obj = datetime.strptime(
                        element["_date_of_birth"], '%Y-%m-%d')
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

    def search_note_by_tags(self,searched_tags)->dict[str:str]:
        if isinstance(searched_tags,str):
            searched_tags=searched_tags.split('#')[1:]
        answer_dict=dict()
        with open(self.contact_book_file_path,'r') as fh:
            list_of_contacts=csv.DictReader(fh,[' ']+self.field_names)
            for contact in list_of_contacts:
                is_tag_in_notetags=True
                if not contact['tags']: continue
                tags=contact['tags'].split('#')[1:]
                for tag in searched_tags:
                    if not contact['note'] or tag not in tags:
                        is_tag_in_notetags=False
                if is_tag_in_notetags: answer_dict.update({" ".join([contact['name'],contact['last_name']]):contact['note']})
        return answer_dict
   
