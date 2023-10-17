from rich.style import Style
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from contactbook import Contact, ContactBook
from notes import Note

INFO = Style(color="bright_green")
COMMAND = Style(color="blue", bold=True)
TITLE = Style(color="green", bold=True, italic=True, reverse=True)
TABLE = Style(color="gray50")
HEADER = Style(color="gold1", bold=True)
RULER = Style(color="purple4")
COMMAND_ERROR = Style(color="red", bold=True)

console = Console(color_system="truecolor")
error_console = Console(stderr=True, style="bold red")


console.print(Panel(title="Welcome to Contact-book", renderable= f"I am your Bot-Assistant.\nLet me know how can I help you? (type-in '[{COMMAND}]h[/]' for help)"), style = INFO, justify = "center")
console.print("made by: *****", style=HEADER, justify="right")
console.rule(style = RULER)

contact_book = ContactBook()

while True:

    command = console.input(f"Enter [{COMMAND}]command[/]: ")
    command = command.casefold()
    if command == "h":

        table = Table(title="List of commands", expand=True, title_style=TITLE, header_style= HEADER, border_style=TABLE, title_justify="center", caption_justify= "center", show_lines=True)
        table.add_column("Command", justify="right", style=INFO, no_wrap=True)
        table.add_column("Description", justify="left", style=INFO, no_wrap=True)

        table.add_row( "all", "Show all contacts")
        table.add_row( "add", "Add new contact to your Contact-book")
        table.add_row( f"search <[{COMMAND}]text or number[/]>", "Search for a contact/-s by given phrase")
        table.add_row( f"birthday <[{COMMAND}]days[/]>", "Check who has his birthday in coming <days>")
        table.add_row( f"notes <[{COMMAND}]#tag1, #tag2...[/]>", "Search notes by #tag/-s")
        table.add_row( "exit", "Exit your Contact-book")

        console.print(table)
        console.rule(style=RULER)

    elif command == "all":

        table = Table(title="All contacts", expand=True, title_style=TITLE, header_style= HEADER, border_style=TABLE, title_justify="center", caption_justify= "center", show_lines=True)
        # table.add_column("No", justify="left", style=INFO)
        table.add_column("Name", justify="left", style=INFO, no_wrap=True)
        table.add_column("Last name", justify="left", style=INFO, no_wrap=True)
        table.add_column("Phone", justify="left", style=INFO, no_wrap=True)
        table.add_column("E-mail", justify="left", style=INFO, no_wrap=True)
        table.add_column("Date of birth", justify="left", style=INFO, no_wrap=True)
        table.add_column("Address", justify="left", style=INFO)
        table.add_column("Notes", justify="left", style=INFO)
        # TODO 0: Figure it out how to expand width of console to ensure all columns and data fits in
        # TODO 1: Add numerator "no" to the contacts returned with method "show_all_contacts()"

        list_of_contacts = contact_book.show_all_contacts()
        for contact in list_of_contacts:
            table.add_row(contact["name"], contact["last name"], contact["phone"], contact["email"],contact["date_of_birth"], contact["address"], contact["note"])


        console.print(table)
        console.rule(style = RULER)

#--------------------------------------------ADDING NEW CONTACT--------------------------------------------#
    elif command == "add":


        name = console.input(f"Enter [{COMMAND}]name[/]: ")
        last_name = console.input(f"Enter [{COMMAND}]last name[/]: ")
        phone = console.input(f"Enter [{COMMAND}]phone number[/]: ")

        # TODO 2: Fix issue with checking e-mail and b-day date format in case they are by default: None

        #creating new_contact has been commented because at this moment it generates errors
        # new_contact = Contact(name.capitalize(), last_name.capitalize(), phone)

        console.print(f"The following parameters are optional, if you want to skip them press [{COMMAND}]enter[/] ", style=INFO)

        e_mail = console.input(f"Enter [{COMMAND}]e-mail[/] [{TABLE}](optional)[/]: ")
        # new_contact.email = e_mail

        date_of_birth = console.input(f"Enter [{COMMAND}]date of birth <dd.mm.rrrr>[/] [{TABLE}](optional)[/]: ")
        # new_contact.date_of_birth = date_of_birth

        address = console.input(f"Enter [{COMMAND}]address[/] [{TABLE}](optional)[/]: ")
        # new_contact.address = address

        note = console.input(f"Enter [{COMMAND}]note[/] [{TABLE}](optional)[/]: ")
        if note:
            while True:
                decision = console.input(
                    f"Do you want to add some tags to your note? <[{COMMAND}]y[/]/[{COMMAND}]n[/]>: ").casefold()
                if decision == "y":
                    tags = console.input(f"Enter tags with # and separate them by comma <[{COMMAND}]#tag1, #tag2, ...[/] >: ").casefold()
                    tags = [tag.replace(",", "").strip() for tag in tags.split(",")]

                    try:
                        # new_contact.note = Note(note, *tags)
                        console.print(f"The note has been added and tagged by: {tags} ")
                        break
                    except:
                        console.print(":warning: Something went wrong. Try again.", style=COMMAND_ERROR)

                    finally:
                        console.rule(style=RULER)

                elif decision == "n":
                    break

                else:
                    console.print(f":warning: Incorrect command. Type-in correct command [{COMMAND}]<y/n>[/]",
                                  style=COMMAND_ERROR)
                    console.rule(style=RULER)


        try:
            # contact_book.add_contact(new_contact)
            grid = Table.grid(expand=True)
            grid.add_column(style=INFO)
            grid.add_column(justify="right")
            grid.add_row("New contact was added to your Contact-book.",
                         f"[{COMMAND}]COMPLETED [{INFO}]:heavy_check_mark:")
            console.print(grid)

        except:
            console.print(":warning: Something went wrong. Try again.", style = COMMAND_ERROR)

        finally:
            console.rule(style = RULER)

# --------------------------------------------CONTACT SEARCHING--------------------------------------------#
    elif command.startswith("search"):
        phrase = command.replace("search", "").strip()
        searched_contacts = contact_book.search_contact(phrase)
        # console.print(searched_contacts)

        table = Table(title=f"Contacts searched by phrase: {phrase}", expand=True, title_style=TITLE, header_style=HEADER, border_style=TABLE,
                      title_justify="center", caption_justify="center", show_lines=True)

        # TODO 3: Add numerator "no" to the contacts returned with method "search_contact(text)"
        #Below colum has been commented because there isn't "No" parameter at this moment
        # table.add_column("No", justify="left", style=INFO)

        table.add_column("Name", justify="left", style=INFO)
        table.add_column("Last name", justify="left", style=INFO)
        table.add_column("Address", justify="left", style=INFO)
        table.add_column("Phone", justify="left", style=INFO)
        table.add_column("E-mail", justify="left", style=INFO)
        table.add_column("Date of birth", justify="left", style=INFO)

        for contact in searched_contacts:
            table.add_row(contact["name"], contact["last name"], contact["address"], contact["phone"], contact["email"],contact["date_of_birth"])

        console.print(table)
        console.rule(style=RULER)

        table = Table(title="Choose what do you want to do with your contacts", expand=True, title_style=TITLE,
                      header_style=HEADER, border_style=TABLE, title_justify="center", caption_justify="center",
                      show_lines=True)

        table.add_column("Command", justify="right", style=INFO, no_wrap=True)
        table.add_column("Description", justify="left", style=INFO, no_wrap=True)

        table.add_row( f"edit <[{COMMAND}]No[/]>", f"Edit contact <[{COMMAND}]No[/]>")
        table.add_row( f"delete <[{COMMAND}]No[/]>", f"Delete contact <[{COMMAND}]No[/]>")
        table.add_row( "exit", "Exit")
        console.print(table)
        console.rule(style=RULER)

        option = console.input(f"Enter [{COMMAND}]command[/] according to contact: ").casefold()


        if option.startswith("edit"):
            contact_to_edit = option.replace("edit", "").strip()

            try:
                #TODO 4: Method "edit_contact" takes only one argument "info" but it has to takes at least two: (contact, new_data) - we have to figure it out how to do it. Maybe the best option is to completely replace edited_contact with new_contact.
                contact_book.edit_contact(contact_to_edit)

                grid = Table.grid(expand=True)
                grid.add_column(style=INFO)
                grid.add_column(justify="right")
                grid.add_row("Contact was edited.",
                             f"[{COMMAND}]COMPLETED [{INFO}]:heavy_check_mark:")
                console.print(grid)

            except:
                console.print(":warning: Something went wrong. Try again.", style = COMMAND_ERROR)

            finally:
                console.rule(style=RULER)


        elif option.startswith("delete"):
            contact_to_delete = option.replace("delete", "").strip()

            try:
                # TODO 5: Method "remove_contact" takes no arguments but it has to take: contact_to_delete
                contact_book.remove_contact(contact_to_delete)

                grid = Table.grid(expand=True)
                grid.add_column(style=INFO)
                grid.add_column(justify="right")
                grid.add_row("Contact was deleted.",
                             f"[{COMMAND}]COMPLETED [{INFO}]:heavy_check_mark:")

            except:
                console.print(":warning: Something went wrong. Try again.", style=COMMAND_ERROR)

            finally:
                console.rule(style=RULER)

        elif option == "add_note":
            pass
        else:
            console.print(":warning: Incorrect command. See the table above and type-in correct command.",
                          style=COMMAND_ERROR)
            console.rule(style=RULER)

# --------------------------------------------BIRTHDAY SEARCHING--------------------------------------------#
    elif command.startswith("birthday") :
        no_of_days = command.replace("birthday", "").strip()
        if no_of_days.isdigit():

            table = Table(title=f"List of your contacts who have birthday in coming {no_of_days} days", expand=True, title_style=TITLE, header_style= HEADER, border_style=TABLE, title_justify="center", caption_justify= "center", show_lines=True)

            # TODO 6: Add numerator "no" to the contacts returned with method "birthdays_in_dyas_range(days_range)"
            # Below colum has been commented because there isn't "No" parameter at this moment
            # table.add_column("No", justify="left", style=INFO)

            table.add_column("Name", justify="left", style=INFO)
            table.add_column("Last name", justify="left", style=INFO)
            table.add_column("Date of birth", justify="left", style=INFO)


            list_of_contacts_with_bday = contact_book.birthdays_in_dyas_range(no_of_days)

            for contact in list_of_contacts_with_bday:
                table.add_row( contact["name"], contact["last name"], contact["date_of_birth"])


            console.print(table)
            console.rule(style=RULER)

        else:
            console.print(f":warning: Incorrect command. To see the list of commands enter '[{COMMAND}]h[/]'", style=COMMAND_ERROR)
            console.rule(style=RULER)

# --------------------------------------------NOTES SEARCHING--------------------------------------------#
    elif command.startswith("notes"):
        tags = [tag.strip() for tag in command.split(",")]

        #Searching for notes by given tags and print out to the table.
        # TODO 7: Add method which allows user to search notes by given tags
        # TODO 8: Add numerator "no" to the contacts returned with above method


        table = Table(title="Choose what do you want to do with your notes", expand=True, title_style=TITLE, header_style= HEADER, border_style=TABLE, title_justify="center", caption_justify= "center", show_lines=True)
        table.add_column("Command", justify="right", style=INFO, no_wrap=True)
        table.add_column("Description", justify="left", style=INFO, no_wrap=True)


        table.add_row( f"tag <[{COMMAND}]No[/]>", f"Add tag/-s to note <[{COMMAND}]No[/]>")
        table.add_row( f"rtag <[{COMMAND}]No[/]>", f"Remove tags from note <[{COMMAND}]No[/]>")
        table.add_row( f"delete <[{COMMAND}]No[/]>", f"Delete the note <[{COMMAND}]No[/]>")
        table.add_row( "exit", "Exit")
        console.print(table)
        console.rule(style=RULER)


        while True:
            option = console.input(f"Enter [{COMMAND}]command[/] according to notes: ").casefold()

            if option.startswith("tag"):
                note_to_tag = option.replace("tag", "").strip()

                while True:
                    new_tags = console.input(
                        f"Enter tags with # sign and separate them by single space<[{COMMAND}]#tag1 #tag2 ...[/]>: ").casefold()
                    new_tags = [tag.strip() for tag in new_tags.split(" ")]

                    try:
                        #TODO 9: Method add_tags has to take two arguments: note, *tags; instead of only *tags

                        console.print(f"The tags: {new_tags} has been added to note.")
                        break
                    except:
                        console.print(":warning: Something went wrong. Try again.", style=COMMAND_ERROR)

                    finally:
                        console.rule(style=RULER)


            elif option.startswith("rtag"):
                note_to_rtag = option.replace("rtag", "").strip()

                try:
                    #TODO 10: Method remove_tags has to take two arguments: note, *tags; instead of only *tags

                    console.print(f"The tags has been removed.")
                    break
                except:
                    console.print(":warning: Something went wrong. Try again.", style=COMMAND_ERROR)

                finally:
                    console.rule(style=RULER)


            elif option.startswith("delete"):
                note_to_delete = option.replace("delete", "").strip()
                # TODO 11: Add method to delete whole note

            elif option == "exit":
                break

            else:
                console.print(":warning: Incorrect command. See the table above and type-in correct command.", style=COMMAND_ERROR)
                console.rule(style=RULER)

    elif command == "exit":
        exit()

    else:
        console.print(f":warning: Incorrect command. To see the list of commands enter [{COMMAND}]'h'[/]", style = COMMAND_ERROR)
        console.rule(style=RULER)

