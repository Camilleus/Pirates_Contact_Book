from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

from contactbook import Contact, ContactBook
from notes import Note

INFO = "green"
QUESTION = "bold blue"
COMMAND_ERROR = "red"

MARKDOWN = ('''
# Welcome to **Contact-book** \n
I am your bot-assistant.\n
Let me know how can I help you? (type-in 'h' for help)\n
''')

console = Console(color_system="truecolor")
md = Markdown(MARKDOWN)

console.print(md, style = INFO)
console.rule()

contact_book = ContactBook()

while True:

    command = console.input(f"Enter [{QUESTION}]command[/]: ")
    command = command.casefold()
    if command == "h":

        table = Table(title="List of commands", expand=True)
        table.add_column("No", justify="right", style=INFO, no_wrap=True)
        table.add_column("Command", justify="right", style=INFO, no_wrap=True)
        table.add_column("Description", justify="left", style=INFO, no_wrap=True)

        table.add_row("1", "all", "Show all contacts")
        table.add_row("2", "add", "Add new contact to your Contact-book")
        table.add_row("3", "edit", "Enter editing mode")
        table.add_row("4", "delete", "Enter deleting mode")
        table.add_row("5", "birthday <days>", "Check who has birthday in coming <days>")
        table.add_row("6", "notes", "Start managing your notes")
        table.add_row("7", "exit", "Exit your Contact-book")

        console.print(table)

    elif command == "all":

        table = Table(title="All contacts", expand=True)
        table.add_column("No", justify="left", style=INFO)
        table.add_column("Name", justify="left", style=INFO)
        table.add_column("Last name", justify="left", style=INFO)
        table.add_column("Address", justify="left", style=INFO)
        table.add_column("Phone", justify="left", style=INFO)
        table.add_column("E-mail", justify="left", style=INFO)
        table.add_column("Date of birth", justify="left", style=INFO)

        # list_of_contacts =
        # no = 1
        # for contact in list_of_contacts:
        #     table.add_row(no, contact.name, contact.last_name,....)
        #     no += 1

        console.print(table)
        pass

    elif command == "add":

        name = console.input(f"Enter [{QUESTION}]name[/]: ")
        last_name = console.input(f"Enter [{QUESTION}]last name[/]: ")
        address = console.input(f"Enter [{QUESTION}]address[/]: ")
        phone = console.input(f"Enter [{QUESTION}]phone number[/]: ")
        e_mail = console.input(f"Enter [{QUESTION}]e-mail[/]: ")
        date_of_birth = console.input(f"Enter date of birth [{QUESTION}]<dd.mm.rrrr>[/]: ")

        new_contact = Contact(name, last_name, address, phone, e_mail, date_of_birth)
        contact_book.add_contact(new_contact)

    elif command == "edit":
        contact_to_edit = console.input(f"Which contact do you want to edit [{QUESTION}]<name last_name>[/]: ").casefold()
        contact_book.edit_contact(contact_to_edit)
        pass

    elif command == "delete":
        contact_to_delete = console.input(f"Which contact do you want to delete [{QUESTION}]<name last_name>[/]: ").casefold()
        contact_book.remove_contact(contact_to_delete)
        pass

    elif command.startswith("birthday") :
        no_of_days = command.replace("birthday", "").strip()
        if no_of_days.isdigit():
            console.print(f"Here is the list of your contacts who have birthday in coming {no_of_days} days: ")

            table = Table(title="All contacts", expand=True)
            table.add_column("No", justify="left", style=INFO)
            table.add_column("Name", justify="left", style=INFO)
            table.add_column("Last name", justify="left", style=INFO)
            table.add_column("Date of birth", justify="left", style=INFO)
            table.add_column("Will have a birthday in days", justify="left", style=INFO)

            # list_of_contacts_with_bday =
            # no = 1
            # for contact in list_of_contacts_with_bday:
            #     table.add_row(no, contact.name, contact.last_name,....)
            #     no += 1

            console.print(table)

        else:
            console.print(f"Incorrect command. To see the list of commands enter [{QUESTION}]'h'[/]", style=COMMAND_ERROR)

    elif command == "notes":

        table = Table(title="Choose what do you want to do")
        table.add_column("Command", justify="right", style=INFO, no_wrap=True)
        table.add_column("Description", justify="left", style=INFO)

        table.add_row("add", "Add new note")
        table.add_row("edit", "Edit note")
        table.add_row("tag", "Add tags to note")
        table.add_row("rtag", "Remove tags from note")
        table.add_row("search", "Search by tags")
        table.add_row("exit", "Exit")
        console.print(table)

        while True:
            option = console.input("Enter command according to notes: ").casefold()

            if option == "add":
                note_content = console.input(f"Enter [{QUESTION}]content[/] of your note: ")
                while True:
                    decision = console.input(f"Do you want to add some tags to your note? [{QUESTION}]<y/n>[/]: ").casefold()
                    if decision == "y":
                        tags = console.input(f"Enter tags separated by comma [{QUESTION}]<tag1, tag2, ...>[/]: ").casefold()
                        tags = [tag.strip() for tag in tags.split(",")]
                        console.print(f"The note has been tagged: {tags} ")
                        break
                    elif decision == "n":
                        break
                    else:
                        console.print(f"Incorrect command. Type-in correct command [{QUESTION}]<y/n>[/]",
                                      style=COMMAND_ERROR)

            elif option == 'edit':
                pass

            elif option == 'tag':
                pass

            elif option == 'rtag':
                pass

            elif option == "search":
                tags = console.input(f"Search notes by tags - enter tags separated by comma [{QUESTION}]<tag1, tag2, ...>[/]: ").casefold()
                tags = [tag.strip() for tag in tags.split(",")]
                console.print(f"Searching for notes by given tags: {tags}")

            elif option == "exit":
                break
            else:
                console.print("Incorrect command. See the table above and type-in correct command.", style=COMMAND_ERROR)

    elif command == "exit":
        exit()
    else:
        console.print(f"Incorrect command. To see the list of commands enter [{QUESTION}]'h'[/]", style = COMMAND_ERROR)

