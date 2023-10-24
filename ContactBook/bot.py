from rich.style import Style
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

try:
    from ContactBook.contactbook import Contact, ContactBook
    from ContactBook.notes import Note
    from ContactBook.custom_errors import WrongInputError
except ModuleNotFoundError:
    from contactbook import Contact, ContactBook
    from notes import Note
    from custom_errors import WrongInputError

#--------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------STYLE CONSTANTS--------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#

INFO = Style(color="bright_green")
COMMAND = Style(color="blue", bold=True)
TITLE = Style(color="green", bold=True, italic=True, reverse=True)
TABLE = Style(color="gray50")
HEADER = Style(color="gold1", bold=True)
RULER = Style(color="purple4")
COMMAND_ERROR = Style(color="red", bold=True)

#--------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------CLASS INSTANCES--------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#

console = Console(color_system="truecolor", width=220)
contact_book = ContactBook()


#--------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------FUNCTIONS-----------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#


# --------------------------------------------------CREATING GRID----------------------------------------------------#
def create_grid(text):
    grid = Table.grid(expand=True)
    grid.add_column(style=INFO)
    grid.add_column(justify="right")
    grid.add_row(text,
                 f"[{COMMAND}]COMPLETED [{INFO}]:heavy_check_mark:")
    return grid


# --------------------------------------------------------HELP-------------------------------------------------------#
def print_help_screen():

    table = Table(title="List of commands", expand=True, title_style=TITLE, header_style=HEADER, border_style=TABLE,
                  title_justify="center", caption_justify="center", show_lines=True, min_width=120)

    table.add_column("Command", justify="right", style=INFO, no_wrap=True, width=15)
    table.add_column("Description", justify="left", style=INFO, no_wrap=True, width=35)

    table.add_row("all", "Show all contacts")
    table.add_row("add", "Add new contact to your Contact-book")
    table.add_row(f"search <[{COMMAND}]text or number[/]>", "Search for a contact/-s by given phrase to view, edit or delete it")
    table.add_row(f"sn", "Search for a contact/-s with notes")
    table.add_row(f"birthday <[{COMMAND}]days[/]>", "Check who has his birthday in coming <days>")
    table.add_row(f"notes <[{COMMAND}]#tag1, #tag2...[/]>", "Search notes by #tag/-s to view or delete it")
    table.add_row("exit", "Exit your Contact-book")

    console.print(table)
    console.rule(style=RULER)


# -----------------------------------------------PRINTING ALL CONTACTS-----------------------------------------------#
def print_all_contacts():

    table = Table(title="All contacts", expand=True, title_style=TITLE, header_style=HEADER, border_style=TABLE,
                  title_justify="center", caption_justify="center", show_lines=True, min_width=210)

    table.add_column("No", justify="left", style=INFO, no_wrap=True, width=3)
    table.add_column("Name", justify="center", style=INFO, no_wrap=True, width=20)
    table.add_column("Last name", justify="center", style=INFO, no_wrap=True, width=20)
    table.add_column("Phone", justify="center", style=INFO, no_wrap=True, width=15)
    table.add_column("E-mail", justify="center", style=INFO, no_wrap=True, width=35)
    table.add_column("Date of birth", justify="center", style=INFO, no_wrap=True, width=15)
    table.add_column("Address", justify="center", style=INFO, width=35)
    table.add_column("Notes", justify="center", style=INFO)
    table.add_column("Tags", justify="center", style=INFO)

    list_of_contacts = contact_book.show_all_contacts()
    for no, contact in enumerate(list_of_contacts):
        contact["note"] = contact["note"].replace("_", ",")
        contact["address"] = contact["address"].replace("_", ",")
        table.add_row(str(no + 1), contact["name"], contact["last_name"], contact["_phone"], contact["_email"],
                      contact["_date_of_birth"], contact["address"], contact["note"], contact["tags"])

    console.print(table)
    console.rule(style=RULER)


#-------------------------------------------------ADDING NEW CONTACT-------------------------------------------------#

def add_new_contact():


    name_is_empty = True
    while name_is_empty:
        name = console.input(f"Enter [{COMMAND}]name[/]: ")
        if len(name) >= 2 and name.isalpha():
            name_is_empty = False
        else:
            console.print(f":warning: Name has to have at least 2 letters", style=COMMAND_ERROR)

    last_name_is_empty = True
    while last_name_is_empty:
        last_name = console.input(f"Enter [{COMMAND}]last name[/]: ")
        last_name = last_name.replace("-", 'Q')

        if len(last_name) >= 2 and last_name.isalpha():
            last_name = last_name.replace("Q", '-')
            last_name_is_empty = False
        else:
            console.print(f":warning: Last name has to have at least 2 letters", style=COMMAND_ERROR)

    phone_is_valid = False
    while not phone_is_valid:
        phone = str(console.input(f"Enter [{COMMAND}]phone number[/]: "))
        try:
            new_contact = Contact(name.capitalize(), last_name.capitalize(), phone)
            phone_is_valid = True
        except WrongInputError as ce:
            console.print(f":warning: {ce.message}", style=COMMAND_ERROR)

    console.print(f"The following parameters are optional, if you want to skip them press [{COMMAND}]enter[/]",
                  style=INFO)

    email_is_valid_or_empty = False
    while not email_is_valid_or_empty:
        e_mail = console.input(f"Enter [{COMMAND}]e-mail[/] [{TABLE}](optional)[/]: ")
        if e_mail == "":
            email_is_valid_or_empty = True
        else:
            try:
                new_contact.email = e_mail
                email_is_valid_or_empty = True
            except WrongInputError as ce:
                console.print(f":warning: {ce.message}", style=COMMAND_ERROR)

    date_is_valid_or_empty = False
    while not date_is_valid_or_empty:
        date_of_birth = console.input(f"Enter [{COMMAND}]date of birth <DD.MM.YYYY>[/] [{TABLE}](optional)[/]: ")
        if date_of_birth == "":
            date_is_valid_or_empty = True
        else:
            try:
                new_contact.date_of_birth = date_of_birth
                date_is_valid_or_empty = True
            except WrongInputError as ce:
                console.print(f":warning: {ce.message}", style=COMMAND_ERROR)

    address = console.input(f"Enter [{COMMAND}]address[/] [{TABLE}](optional)[/]: ")
    address = address.replace(",", "_")
    new_contact.address = address

    note = console.input(f"Enter [{COMMAND}]note[/] [{TABLE}](optional)[/]: ")
    note = note.replace(",", "_")

    if note:
        while True:
            decision = console.input(
                f"Do you want to add some tags to your note? <[{COMMAND}]y[/]/[{COMMAND}]n[/]>: ").casefold()
            if decision == "y":
                tags = console.input(
                    f"Enter tags with # and separate them by comma <[{COMMAND}]#tag1, #tag2, ...[/] >: ").casefold()
                tags = [tag.replace(",", "").strip() for tag in tags.split(",")]

                try:
                    new_contact.note = Note(note, *tags)
                    console.print(f"The note has been added and tagged by: {tags} ", style=INFO)
                    break
                except ValueError:
                    console.print(":warning: Something went wrong with adding notes. Try again.", style=COMMAND_ERROR)

                finally:
                    console.rule(style=RULER)

            elif decision == "n":
                break

            else:
                console.print(f":warning: Incorrect command. Type-in correct command [{COMMAND}]<y/n>[/]",
                              style=COMMAND_ERROR)
                console.rule(style=RULER)

    try:
        contact_book.add_contact(new_contact)

        grid = create_grid("New contact has been added to your Contact-book.")
        console.print(grid)

    except ValueError:
        console.print(":warning: Something went wrong with adding contact. Try again.", style=COMMAND_ERROR)

    finally:
        console.rule(style=RULER)


# -------------------------------------------------CONTACT SEARCHING-------------------------------------------------#
def search_contacts_by_phrase(phrase):
    searched_contacts = contact_book.search_contact(phrase)

    if not searched_contacts:
        console.print(f"No contact with the keyword: [{COMMAND}]{phrase}[/] was found", style=INFO)

    else:
        no_of_contacts = len(searched_contacts)

        table = Table(title=f"Contacts searched by phrase: {phrase}", expand=True, title_style=TITLE,
                      header_style=HEADER, border_style=TABLE,
                      title_justify="center", caption_justify="center", show_lines=True, min_width=210)

        table.add_column("No", justify="left", style=INFO, no_wrap=True, width=3)
        table.add_column("Name", justify="center", style=INFO, no_wrap=True, width=20)
        table.add_column("Last name", justify="center", style=INFO, no_wrap=True, width=20)
        table.add_column("Phone", justify="center", style=INFO, no_wrap=True, width=15)
        table.add_column("E-mail", justify="center", style=INFO, no_wrap=True, width=35)
        table.add_column("Date of birth", justify="center", style=INFO, no_wrap=True, width=15)
        table.add_column("Address", justify="center", style=INFO, width=35)
        table.add_column("Notes", justify="center", style=INFO)
        table.add_column("Tags", justify="center", style=INFO)

        for no, contact in enumerate(searched_contacts):
            contact["note"] = contact["note"].replace("_", ",")
            contact["address"] = contact["address"].replace("_", ",")
            table.add_row(str(no + 1), contact["name"], contact["last_name"], contact["_phone"], contact["_email"],
                          contact["_date_of_birth"], contact["address"], contact["note"], contact["tags"])

        console.print(table)
        console.rule(style=RULER)

        table = Table(title="Choose what do you want to do with your contacts", expand=True, title_style=TITLE,
                      header_style=HEADER, border_style=TABLE, title_justify="center", caption_justify="center",
                      show_lines=True, min_width=100)

        table.add_column("Command", justify="right", style=INFO, no_wrap=True)
        table.add_column("Description", justify="left", style=INFO, no_wrap=True)

        table.add_row(f"edit <[{COMMAND}]No[/]>", f"Edit contact <[{COMMAND}]No[/]>")
        table.add_row(f"delete <[{COMMAND}]No[/]>", f"Delete contact <[{COMMAND}]No[/]>")
        table.add_row("exit", "Exit")
        console.print(table)
        console.rule(style=RULER)

        while True:
            option = console.input(f"Enter [{COMMAND}]command[/] according to contact: ").casefold()

            if option.startswith("edit"):
                edit_contact(option, no_of_contacts, searched_contacts)

            elif option.startswith("delete"):
                delete_contact(option, no_of_contacts, searched_contacts)

            elif option == "exit":
                break

            else:
                console.print(":warning: Incorrect command. See the table above and type-in correct command.",
                              style=COMMAND_ERROR)
                console.rule(style=RULER)


# ----------------------------------------SEARCHING FOR CONTACTS WITH B-DAYS-----------------------------------------#
def search_contacts_with_birthdays(no_of_days):

    table = Table(title=f"List of your contacts who have birthday in coming {no_of_days} days", expand=True,
                  title_style=TITLE, header_style=HEADER, border_style=TABLE, title_justify="center",
                  caption_justify="center", show_lines=True, min_width=120)

    table.add_column("No", justify="left", style=INFO, no_wrap=True, width=3)
    table.add_column("Name", justify="center", style=INFO, no_wrap=True, width=20)
    table.add_column("Last name", justify="center", style=INFO, no_wrap=True, width=20)
    table.add_column("Date of birth", justify="center", style=INFO, no_wrap=True, width=15)
    table.add_column("No of days until birthday", justify="center", style=INFO, no_wrap=False, width=15)

    list_of_contacts_with_bday = contact_book.birthdays_in_days_range(int(no_of_days))

    if not list_of_contacts_with_bday:
        console.print(f'No one has a birthday in the given range of {no_of_days} days', style=INFO)

    else:
        for no, contact in enumerate(list_of_contacts_with_bday):
            table.add_row(str(no + 1), contact["name"], contact["last_name"], contact["_date_of_birth"],
                          contact['to_birthday'])
        console.print(table)

    console.rule(style=RULER)


# -----------------------------------------SEARCHING FOR CONTACTS WITH NOTES-----------------------------------------#

def search_contacts_with_notes():

    searched_contacts_with_notes = contact_book.search_contacts_with_notes()

    if not searched_contacts_with_notes:
        console.print("No contact with the note was not found", style=INFO)

    else:
        table = Table(title=f"Contacts with notes", expand=True, title_style=TITLE, header_style=HEADER,
                      border_style=TABLE,
                      title_justify="center", caption_justify="center", show_lines=True, min_width=120)

        table.add_column("No", justify="left", style=INFO, no_wrap=True, width=3)
        table.add_column("Name", justify="center", style=INFO, no_wrap=True, width=20)
        table.add_column("Last name", justify="center", style=INFO, no_wrap=True, width=20)
        table.add_column("Notes", justify="center", style=INFO, width=100)

        for no, contact in enumerate(searched_contacts_with_notes):
            contact["note"] = contact["note"].replace("_", ",")
            table.add_row(str(no + 1), contact["name"], contact["last_name"], contact["note"])

        console.print(table)

    console.rule(style=RULER)


# --------------------------------------------SEARCHING FOR NOTES BY TAGS--------------------------------------------#

def search_notes_by_tags(tags):

    list_of_notes = contact_book.search_note_by_tags(tags)
    no_of_notes = len(list_of_notes)

    if list_of_notes:

        table = Table(title=f"Notes searched by given tags: {tags}", expand=True, title_style=TITLE,
                      header_style=HEADER,
                      border_style=TABLE, title_justify="center", caption_justify="center", show_lines=True,
                      min_width=150)

        table.add_column("No", justify="left", style=INFO, no_wrap=True, width=3)
        table.add_column("Notes", justify="center", style=INFO)
        table.add_column("Name", justify="center", style=INFO, no_wrap=True, width=20)
        table.add_column("Last name", justify="center", style=INFO, no_wrap=True, width=20)

        for no, note in enumerate(list_of_notes):
            note["note"] = note["note"].replace("_", ",")
            table.add_row(str(no + 1), note["note"], note["name"], note["last_name"])

        console.print(table)
        console.rule(style=RULER)

        table = Table(title="Choose what do you want to do with your notes", expand=True, title_style=TITLE,
                      header_style=HEADER,
                      border_style=TABLE, title_justify="center", caption_justify="center", show_lines=True,
                      min_width=100)
        table.add_column("Command", justify="right", style=INFO, no_wrap=True)
        table.add_column("Description", justify="left", style=INFO, no_wrap=True)

        table.add_row(f"delete <[{COMMAND}]No[/]>", f"Delete the note <[{COMMAND}]No[/]>")
        table.add_row("exit", "Exit")
        console.print(table)
        console.print(f"Notes editing is available by editing contacts -> search for a contact and enter editing mode",
                      style=INFO)
        console.rule(style=RULER)

        while True:
            option = console.input(f"Enter [{COMMAND}]command[/] according to notes: ").casefold()

            if option.startswith("delete"):
                delete_note(option, no_of_notes, list_of_notes)

            elif option == "exit":
                break

            else:
                console.print(":warning: Incorrect command. See the table above and type-in correct command.",
                              style=COMMAND_ERROR)
                console.rule(style=RULER)

    else:
        console.print(f"There are no notes tagged by: {tags}", style=INFO)


#--------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------SUB-FUNCTIONS---------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#

# --------------------------------------------------EDITING CONTACT--------------------------------------------------#

def edit_contact(option, no_of_contacts, searched_contacts):

    try:
        contact_to_edit = int(option.replace("edit", "").strip()) - 1
        if 0 <= contact_to_edit <= no_of_contacts:
            id_to_edit = int(searched_contacts[contact_to_edit].get('id'))

            name_is_empty = True
            while name_is_empty:

                name = edit_field('name', searched_contacts, contact_to_edit, mandatory=True)
                if len(name) >= 2 and name.isalpha():
                    name_is_empty = False
                else:
                    console.print(f":warning: Name has to have at least 2 letters", style=COMMAND_ERROR)

            last_name_is_empty = True
            while last_name_is_empty:
                last_name = edit_field('last_name', searched_contacts, contact_to_edit, mandatory=True)
                last_name = last_name.replace("-", 'Q')
                if len(last_name) >= 2 and last_name.isalpha():
                    last_name = last_name.replace("Q", '-')
                    last_name_is_empty = False
                else:
                    console.print(f":warning: Last name has to have at least 2 letters", style=COMMAND_ERROR)

            phone_is_valid = False
            while not phone_is_valid:
                phone = str(edit_field('_phone', searched_contacts, contact_to_edit, mandatory=True))
                try:
                    new_contact = Contact(name.capitalize(), last_name.capitalize(), phone)
                    phone_is_valid = True
                except WrongInputError as ce:
                    console.print(f":warning: {ce.message}", style=COMMAND_ERROR)

            email_is_valid_or_empty = False
            while not email_is_valid_or_empty:
                e_mail = edit_field('_email', searched_contacts, contact_to_edit, mandatory=False)
                if e_mail == "":
                    email_is_valid_or_empty = True
                else:
                    try:
                        new_contact.email = e_mail
                        email_is_valid_or_empty = True
                    except WrongInputError as ce:
                        console.print(f":warning: {ce.message}", style=COMMAND_ERROR)

            date_is_valid_or_empty = False
            while not date_is_valid_or_empty:
                date_of_birth = edit_field('_date_of_birth', searched_contacts, contact_to_edit, mandatory=False)
                date_of_birth = date_of_birth.split("-")
                date_of_birth.reverse()
                date_of_birth = ".".join(date_of_birth)
                console.print(date_of_birth)

                if date_of_birth == "":
                    date_is_valid_or_empty = True
                else:
                    try:
                        new_contact.date_of_birth = date_of_birth
                        date_is_valid_or_empty = True
                    except WrongInputError as ce:
                        console.print(f":warning: {ce.message}", style=COMMAND_ERROR)

            address = edit_field('address', searched_contacts, contact_to_edit, mandatory=False)
            address = address.replace(",", "_")
            new_contact.address = address

            note = edit_field('note', searched_contacts, contact_to_edit, mandatory=False)
            note = note.replace(",", "_")

            if note:
                tags = edit_field('tags', searched_contacts, contact_to_edit, mandatory=False)
                if type(tags)==list: 
                    tags=[tag.replace(",", "").strip() for tag in tags]
                else:
                    tags = [tag.replace(",", "").strip() for tag in tags.split(",")]
            else:
                tags = ""
            new_contact.note = Note(note, *tags)

            try:
                contact_book.edit_contact(id_to_edit, new_contact)

                grid = create_grid("Contact has been successfully edited.")
                console.print(grid)

            except ValueError:
                console.print(":warning: Something went wrong with editing your contact. Try again.", style=COMMAND_ERROR)

            finally:
                console.rule(style=RULER)

    except IndexError:
        console.print(":warning: Index out of range. Try again.", style=COMMAND_ERROR)

    except ValueError:
        console.print(":warning: You have to enter valid number of a contact to edit. Try again.",
                      style=COMMAND_ERROR)

    finally:
        console.rule(style=RULER)


# --------------------------------------------------EDITING FIELD----------------------------------------------------#
def edit_field(field, searched_contacts, contact_to_edit, mandatory = False):

    valid_value = False
    while not valid_value:

        console.print(
            f"\nActual value for {field} is: [{COMMAND}]{searched_contacts[contact_to_edit].get(field)}[/]\n",
            style=INFO)
        console.print(f"To leave it as it is - press [{COMMAND}]Enter[/]", style=TABLE)
        console.print(f"To insert new value - enter new value and press [{COMMAND}]Enter[/]", style=TABLE)
        if mandatory:
            console.print(f"You can't delete this value because it is mandatory.", style=TABLE)
        else:
            console.print(
                f"To delete this value - type-in [{COMMAND}]'del'[/] and press [{COMMAND}]Enter[/]",
                style=TABLE)
        if field == '_date_of_birth':
            new_data = console.input(f"Enter [{COMMAND}]date of birth <DD.MM.YYYY>[/] [{TABLE}](optional)[/]: ")

        elif field == 'tags':
            new_data = console.input(
                f"Enter tags with # and separate them by comma <[{COMMAND}]#tag1, #tag2, ...[/] >: ").casefold()
            if new_data:
                new_data = [tag.replace(",", "").strip() for tag in new_data.split(",")]
            console.rule(style=RULER)
        else:
            new_data = console.input(
                f"\nEnter [{COMMAND}]data/command[/] according to above instructions: ")
            console.rule(style=RULER)


        if not new_data:
            new_data = searched_contacts[contact_to_edit].get(field)
            console.print(f"\nThe existing value: {new_data} has been left",
                          style=INFO)
            console.rule(style=RULER)
            return new_data
        elif new_data == "del":
            if not mandatory:
                new_data = ""
                console.print(f"\nThe value has been deleted", style=INFO)
                console.rule(style=RULER)
                return new_data
        else:
            console.print(f"\nThe value has been changed to: {new_data}",
                          style=INFO)
            console.rule(style=RULER)
            return new_data


# -------------------------------------------------DELETING CONTACT--------------------------------------------------#
def delete_contact(option, no_of_contacts, searched_contacts):

    decision = console.input(
        f"Do you really want to delete your contact? <[{COMMAND}]y[/]/[{COMMAND}]n[/]>: ").casefold()
    if decision == "y":
        try:

            contact_to_remove = int(option.replace("delete", "").strip()) - 1
            if 0 <= contact_to_remove <= no_of_contacts - 1:
                id_to_remove = int(searched_contacts[contact_to_remove].get('id'))

                contact_book.remove_contact(id_to_remove)
                grid = create_grid("Contact has been deleted.")
                console.print(grid)

        except IndexError:
            console.print(":warning: Index out of range. Try again.", style=COMMAND_ERROR)

        except ValueError:
            console.print(":warning: You have to enter valid number of a contact to delete. Try again.",
                          style=COMMAND_ERROR)

        finally:
            console.rule(style=RULER)


# ---------------------------------------------------DELETING NOTE---------------------------------------------------#

def delete_note(option, no_of_notes, list_of_notes):

    decision = console.input(
        f"Do you really want to delete your note? <[{COMMAND}]y[/]/[{COMMAND}]n[/]>: ").casefold()
    if decision == "y":
        try:
            note_to_delete = int(option.replace("delete", "").strip()) - 1
            if 0 <= note_to_delete <= no_of_notes - 1:
                id_of_contact = int(list_of_notes[note_to_delete].get('id'))
                contact_book.remove_or_edit_data(id_of_contact)

                grid = create_grid("Note has been deleted.")
                console.print(grid)

        except IndexError:
            console.print(":warning: Index out of range. Try again.", style=COMMAND_ERROR)

        except ValueError:
            console.print(":warning: You have to enter valid number of a note to delete. Try again.",
                          style=COMMAND_ERROR)

        finally:
            console.rule(style=RULER)


#*******************************************************************************************************************#
#------------------------------------------------MAIN FUNCTION - BOT------------------------------------------------#
#*******************************************************************************************************************#

def bot_contact_book():
    console.print("")
    console.print(Panel(title=f"Welcome to Contact-book", renderable= f"I am your Bot-Assistant.\nLet me know how can I help you?"), style = INFO, justify = "center")
    console.print("made by: *****", style=HEADER, justify="right")
    console.rule(style = RULER)

    while True:

        command = console.input(f"Enter [{COMMAND}]command[/][{TABLE}] ('h' - for help)[/]: ")
        command = command.casefold()

        if command == "h":
            print_help_screen()

        elif command == "all":
            print_all_contacts()

        elif command == "add":
            add_new_contact()

        elif command.startswith("search"):
            phrase = command.replace("search", "").strip()
            if phrase:
                search_contacts_by_phrase(phrase)
            else:
                console.print(f":warning: Enter the [{COMMAND}]phrase[/] to search for",
                              style=COMMAND_ERROR)
                console.rule(style=RULER)

        elif command == "sn":
            search_contacts_with_notes()

        elif command.startswith("birthday") :
            no_of_days = command.replace("birthday", "").strip()
            if no_of_days.isdigit():
                search_contacts_with_birthdays(no_of_days)

            else:
                console.print(f":warning: Incorrect command. To see the list of commands enter '[{COMMAND}]h[/]'", style=COMMAND_ERROR)
                console.rule(style=RULER)

        elif command.startswith("notes"):

            tags = command.replace("notes", "")
            if tags:
                tags = [tag.strip() for tag in tags.split(",")]
                search_notes_by_tags(tags)
            else:
                console.print(f":warning: Enter the [{COMMAND}]tags[/] to search for",
                              style=COMMAND_ERROR)
                console.rule(style=RULER)

        elif command == "exit":
            exit()

        else:
            console.print(f":warning: Incorrect command. To see the list of commands enter [{COMMAND}]'h'[/]", style = COMMAND_ERROR)
            console.rule(style=RULER)
