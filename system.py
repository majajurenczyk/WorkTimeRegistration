import database as db
from os.path import exists
import config
import ui
from os import remove


def add_terminal(location):
    return db.add_terminal(location)


def delete_terminal(id_term):
    return db.delete_terminal(id_term)


def assign_card(id_card, id_emp):
    return db.add_assignment(id_card, id_emp)


def add_employee(name, last_name):
    return db.employ(name, last_name)


def delete_employee(id_emp):
    return db.fire(id_emp)


def delete_assignment(id_emp):
    return db.delete_assignment(id_emp)


def generate_report(id_emp, data_from, data_to):
    return db.generate_report(id_emp, data_from, data_to)


if __name__ == "__main__":
    if not exists(config.DATABASE_NAME):
        db.init_database()
    else:
        print("DO YOU WANT TO RESET DATABASE?")
        print("1 - TO RESET")
        print("ANYTHING ELSE TO SAVE OLD DATABASE")
        choice = input()

        if choice == "1":
            remove(config.DATABASE_NAME)
            db.init_database()

    ui.user_interface()
