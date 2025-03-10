from main import AddressBook, Record, Birthday, Phone, Name, Field

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
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_erorr
def change_contact(args, contacts):
    name, new_number = args
    if name in contacts:
        contacts[name] = new_number
        return f"Contact {name} updated"
    else:
        return f"Contact {name} not found"

@input_erorr
def show_phone(args, contacts):
    name = args[0]
    return contacts.get(name, f"{name} not found")

@input_erorr
def show_all(contacts):
        if contacts:
            return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())
        return "No contacts found" 

@input_erorr
def add_birthday(args, book):
    name, birthday = args
    record = next((r for r in book.records if r.name ==name), None)
    if record:
        record.birthday = Birthday(birthday)
        return f"Birthday for {name} appended: {birthday}"
    else:
        return "Contact not found"
    

@input_erorr
def show_birthday(args, book):
    name = args[0]
    record = next((r for r in book.records if r.name == name), None)
    if record and record.birthday:
        return f"Birthday {name}: {record.birthday.value.strftime('%d.%m.%Y')}"
    else:
        return "Contact not found or birthday not found"

@input_erorr
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "No greetings for next week"
    result = "Gretting for next week:\n"
    for item in upcoming:
        result += f"{item["name"]}: {item["birthday"]}\n"

    return result.strip()

def main():
    contacts = {}
    print("Welcome to the assistance bot")
    while True:
        user_input = input("Enter a command: ").strip()
        
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can i help you: ")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        elif command == "add_birthday":
            print(add_birthday(args, book))
        elif command == 'show-birthday':
            print(show_birthday(args, book))
        elif command == "birthday":
            print(birthdays(args, book))
        else:
            print("Invalid command")

if __name__ =="__main__":
    main()