# 🤳🏼 5Stars Contact Book

Hello Everyone! Its Contact Book with built-in personal assitant

## 🌟 Introduction

Our personal assistant can help you with:

1. saving personal data of customers (or user contacts), such as name, phone numbers, address, email and birthdays;
2. saving notes with hashtags, with the ability to search, edit, delete, and sort them;
3. remembering who has birthday in near future, it has special command to use :D

It's made by **\*** squad (five stars squad)

## 🔧 Technologies we use

- 🐍 Python
- 📚 Poetry
- 🐼 Pandas
- 💰 Rich

## 🚀 Features

- Create, edit, and delete textual notes with titles and content
- Add multiple tags to notes for easy filtering and organization
- Search notes by title, content, tags, or status (active/inactive)
- Sort notes alphabetically by tags
- Display notes paginated for convenient viewing
- Save all notes to a CSV file and load them from there
- Intuitive command-line interface

## 📝 Installation

Installation:
It's simple, just install our app with command

```bash
pip install 5-Stars-Contact-Book==0.0.1
```

(À propos, copy it to terminal ;D)

If this doesn't work you can install it from the source code.

Download source code as zip. Unpack it and enter this to cmd terminal with correct path

```bash
pip install /path/to/repository/with/code/.
```

## 🔧 Requirements:

Python 3.6 or newer

rich library

pandas library

## 📝 How to run this Contact Book

nothing simpler as that, just write `RunContactBook` in cmd or virtual environment

## 💡 Usage

Our Personal assistant knows how to do everything necessary so that you can easily find out information about loved ones, or just people with whom you are in contact.
Our Personal assistant adds, changes and deletes records about the user (name, telephone numbers, date of birth, e-mail address, residential address). For most fields in the record, check for the veracity of the entered information is taken into account.

- The phone can be in multiple formats, for instance: +48 123 456 789, +1 555-123-4567, 123456789, 1234-5678, +44 20 7123 1234
- Date of birth is entered in "dd.mm.yyyy" format. The input format is the most common, so it is taken as a basis. Birthday class fields of datetime type.
- The e-mail has a check that the characters "@" and "." must be present, and the domain name must consist of at least two letters.
- The address can be everything you write in there
- You can find out how many days there are left to the birthday of the selected user
- Returns a date-sorted list of users who have a birthday within the entered number of days from today's date.
- A search for the entire contact book is also implemented (the condition is at least 2 characters). Returns a list of all contacts where the search query is found.
- When starting work with the contact book, the information is deserialized from the `contact_book.scv` file, if it does not exist, it is automatically created for work. And upon completion of work, all information is serialized
- Our personal assistant displays a list of all contacts, can sort them by name or age of the user. Also displays information about the selected user.

## 🧑🏻‍🤝‍🧑🏽 Creators

- [Project Manager - Kamil "Camilleus" Truszkowski](https://github.com/Camilleus)
- [Scrum Master - Oktawian Czakiert](https://github.com/OktawianCzakiert)
- [Developer - Tomasz Heese](https://github.com/Heesej)
- [Developer - Krzysztof Jaszewski](https://github.com/Greecus)
- [Developer - Szymon](https://github.com/SzHornet)

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## 📄 License

[MIT](https://choosealicense.com/licenses/mit/)

## 📁 Project Structure

```bash
5_Stars_Contact_Book
├─ ContactBook
│  ├─ bot.py
│  ├─ contactbook.py
│  ├─ custom_errors.py
│  ├─ main.py
│  ├─ notes.py
│  └─ __init__.py
├─ README.md
└─ setup.py
```

Thank you for reading it! 😺
