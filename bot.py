from classes import AddressBook, Record, Birthday, Phone, Name, Field

def input_erorr(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError as e:
            return f"key {e} not found, try again"
        except IndexError:
            return "Index not found, write again"
    return inner 

@input_erorr
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_erorr
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.get(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."
    
    record.add_phone(phone)
    return message

@input_erorr
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.get(name)
 
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"Contact {name} updated."
    else:
        return f"Contact {name} not found."
    
@input_erorr
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.get(name)
    if record:
        return f"{name}: {', '.join(p.value for p in record.phones)}"
    else:
        return f"Contact {name} not found."

@input_erorr
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts found."
    
    return "\n".join(f"{name}: {', '.join(p.value for p in record.phones)}" for name, record in book.data.items())


@input_erorr
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.get(name)
    
    if record:
        record.birthday = Birthday(birthday)
        return f"Birthday for {name} added: {birthday}"
    else:
        return "Contact not found."
    

@input_erorr
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.get(name)

    if record and record.birthday:
        return f"Birthday {name}: {record.birthday.value.strftime('%d.%m.%Y')}"
    else:
        return "Contact not found or birthday not set."

@input_erorr
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "No greetings for next week"
    result = "Gretting for next week:\n"
    for item in upcoming:
        result += f"{item['name']}: {item['birthday']}\n"

    return result.strip()

def main():
    book = AddressBook()
    print("Welcome to the assistance bot!")

    while True:
        user_input = input("Enter a command: ").strip()
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()