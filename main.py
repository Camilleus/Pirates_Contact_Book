from contactbook import Contact, ContactBook

if __name__ == "__main__":
    kontakt = Contact("Oktawian", "Czakiert", "123-321-123", "mail@wp.pl")
    ksiazka = ContactBook()

    ksiazka.add_contact(kontakt)