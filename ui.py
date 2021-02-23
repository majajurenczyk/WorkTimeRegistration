import system


def add_emp():
    print('Enter name:')
    name = input()
    print('Enter last name:')
    last_name = input()
    if not system.add_employee(name, last_name):
        print("Error")
    else:
        print("Done")


def del_emp():
    print('Enter id:')
    id_emp = input()
    if id_emp.isnumeric():
        int(id_emp)
        if system.delete_employee(id_emp):
            print("Done")
        else:
            print("Error")
    else:
        print("employee id has to be a number\nError")


def add_assign():
    print('Enter card id:')
    id_card = input()
    print("Enter employee id: ")
    id_emp = input()
    if id_emp.isnumeric():
        int(id_emp)
        if not system.assign_card(id_card, id_emp):
            print("Error")
        else:
            print("Done")
    else:
        print("employee id has to be a number\nError")


def del_assign():
    print("Enter employee id: ")
    id_emp = input()
    if id_emp.isnumeric():
        int(id_emp)
        if not system.delete_assignment(id_emp):
            print("Error")
        else:
            print("Done")
    else:
        print("employee id has to be a number\nError")


def add_term():
    print("Enter terminal location: ")
    location = input()
    if not system.add_terminal(location):
        print("Error")
    else:
        print("Done")


def del_term():
    print("Enter terminal id:")
    id_term = input()
    if id_term.isnumeric():
        int(id_term)
        if not system.delete_terminal(id_term):
            print("Error")
        else:
            print("Done")
    else:
        print("term id has to be a number\nError")


def gen_report():
    print("Enter employee id: ")
    id_emp = input()
    print("date: Y-M-D H:M:S")
    print("From date: ")
    date_from = input()
    print("To date: ")
    date_to = input()
    if id_emp.isnumeric():
        int(id_emp)
        if system.generate_report(id_emp, date_from, date_to):
            print("Done")
        else:
            print("Error")
    else:
        print("employee id has to be a number\nError")


def show_options():
    print("""
         1 - TO ADD AN EMPLOYEE\n
         2 - TO DELETE AN EMPLOYEE\n
         3 - TO ADD AN ASSIGNMENT\n
         4 - TO DELETE AN ASSIGNMENT\n
         5 - TO ADD TERMINAL\n
         6 - TO DELETE TERMINAL\n
         7 - TO GENERATE RAPORT\n
         8 - TO SHOW OPTIONS\n
         9 - TO CLOSE SYSTEM
         """)


def string_to_func(pressed):
    if pressed == "1":
        add_emp()
    elif pressed == "2":
        del_emp()
    elif pressed == "3":
        add_assign()
    elif pressed == "4":
        del_assign()
    elif pressed == "5":
        add_term()
    elif pressed == "6":
        del_term()
    elif pressed == "7":
        gen_report()
    elif pressed == "8":
        show_options()


def user_interface():
    print("HELLO")
    show_options()
    while True:
        print("CHOOSE OPTION: ")
        pressed = input()
        if pressed == "9":
            break
        string_to_func(pressed)

    print("SYSTEM CLOSED")
