import sqlite3
import datetime
import csv
import random as rd
import config


def opendb():
    try:
        conn = sqlite3.connect(config.DATABASE_NAME)
    except sqlite3.Error:
        print("database cannot be opened")
        return False
    cur = conn.cursor()
    return [conn, cur]


def init_database():
    opened = opendb()
    if not opened:
        return False
    connection = opened[0]
    c = opened[1]

    c.execute("""CREATE TABLE employees (
            idEmp INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            lastName TEXT NOT NULL
            )""")
    connection.commit()

    c.execute("""CREATE TABLE assignments (
            idCard TEXT NOT NULL PRIMARY KEY,
            idEmp INTEGER 
            )""")
    connection.commit()

    c.execute("""CREATE TABLE terminals (
            idTerm INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT
                )""")
    connection.commit()

    c.execute("""CREATE TABLE logs (
            idLog INTEGER PRIMARY KEY AUTOINCREMENT,
            date text NOT NULL,
            idTerm INTEGER NOT NULL,
            idCard TEXT,
            idEmp INTEGER,
            event INTEGER
                )""")
    connection.commit()

    c.close()
    connection.close()
    return True


def add_terminal(location):
    opened = opendb()
    if not opened:
        return False
    connection = opened[0]
    c = opened[1]
    c.execute("INSERT INTO terminals (location) VALUES(?)", (location,))
    connection.commit()
    c.close()
    connection.close()
    return True


def employ(name, last_name):
    opened = opendb()
    if not opened:
        return False
    connection = opened[0]
    c = opened[1]
    c.execute("INSERT INTO employees (name, lastName) VALUES(?,?)", (name, last_name,))
    connection.commit()
    c.close()
    connection.close()
    return True


def fire(id_emp):
    opened = opendb()
    if not opened:
        return False
    connection = opened[0]
    c = opened[1]
    c.execute("SELECT * FROM employees WHERE idEmp=?", (str(id_emp),))
    connection.commit()
    if not c.fetchall():
        c.close()
        connection.close()
        print("There is no employee with this id")
        return False
    # when deleting an employee delete his assignments
    c.execute("SELECT * FROM assignments WHERE idEmp=?", (str(id_emp),))
    if c.fetchall():
        c.execute("UPDATE assignments SET idEmp=NULL WHERE idEmp=?", (str(id_emp),))
        connection.commit()
    c.execute("DELETE FROM employees WHERE idEmp = ?", (str(id_emp),))
    connection.commit()
    c.close()
    connection.close()
    return True


def delete_terminal(id_term):
    opened = opendb()
    if not opened:
        return False
    connection = opened[0]
    c = opened[1]
    c.execute("SELECT * FROM terminals WHERE idTerm=?", (str(id_term),))
    connection.commit()
    if not c.fetchall():
        c.close()
        connection.close()
        print("There is no terminal with this id")
        return False
    c.execute("DELETE FROM terminals WHERE idTerm = ?", (str(id_term),))
    connection.commit()
    c.close()
    connection.close()
    return True


def add_assignment(id_card, id_emp):
    # one employee can have one rfid card
    opened = opendb()
    if not opened:
        return False
    connection = opened[0]
    c = opened[1]
    # if employee exists
    c.execute("SELECT * FROM employees WHERE idEmp=?", (str(id_emp),))
    if c.fetchall():
        # if employee do not have a card
        c.execute("SELECT * FROM assignments WHERE idEmp=?", (str(id_emp),))
        if not c.fetchall():
            c.execute("SELECT * FROM assignments WHERE idCard=?", (id_card,))
            # if there is no such rfid card in database
            if not c.fetchall():
                c.execute("INSERT INTO assignments (idCard, idEmp) VALUES(?, ?)", (str(id_card), str(id_emp),))
                connection.commit()
            # if rfid card already exists
            else:
                c.execute("UPDATE assignments SET idEmp=? WHERE idCard=?", (str(id_emp), id_card,))
                connection.commit()
            c.close()
            connection.close()
            return True
        else:
            print("This employee has his card already assigned")
            c.close()
            connection.close()
            return False
    else:
        c.close()
        connection.close()
        print("There is no employee with this id")
        return False


def delete_assignment(id_emp):
    opened = opendb()
    if not opened:
        return False
    connection = opened[0]
    c = opened[1]
    c.execute("SELECT * FROM employees WHERE idEmp=?", (str(id_emp),))
    if not c.fetchall():
        print("There is no employee with this id")
        return False
    c.execute("SELECT * FROM assignments WHERE idEmp=?", (str(id_emp),))
    connection.commit()
    if c.fetchall():
        c.execute("UPDATE assignments SET idEmp=NULL WHERE idEmp=?", (str(id_emp),))
        connection.commit()
    else:
        print("This employee has not any card")
    c.close()
    connection.close()
    return True


def add_log(id_term, id_card, date):
    # assuming that terminal exists
    opened = opendb()
    if not opened:
        return False
    connection = opened[0]
    c = opened[1]
    # deciding if actual action is loggin in - 1 or out - 0
    c.execute("SELECT event FROM logs WHERE idCard=? ORDER BY datetime(date) DESC LIMIT 1", (id_card,))
    latest_event = c.fetchone()
    if not latest_event or latest_event[0] == 0:
        act_event = 1
    else:
        act_event = 0

    # if thats logging-in check if card has been already added to database
    if act_event == 1:
        c.execute("SELECT * FROM assignments WHERE idCard=?", (id_card,))
        if not c.fetchall():
            c.execute("INSERT INTO assignments (idCard) VALUES(?)", (id_card,))
            connection.commit()

    # searching for an id of employee whose card was used in action
    c.execute("SELECT idEmp FROM assignments WHERE idCard=?", (id_card,))
    # if card is assigned to an employee add with employee's id, if isn't - without
    res = c.fetchone()
    if res:
        c.execute("INSERT INTO logs (date, idTerm, idCard, idEmp, event ) VALUES(?, ?, ?, ?, ?)", (date,
                                                                                                   str(id_term),
                                                                                                   id_card, res[0],
                                                                                                   str(act_event),))
        connection.commit()
    else:
        c.execute("INSERT INTO logs (date, idTerm, idCard, event ) VALUES(?, ?, ?, ?)",
                  (date, id_card, str(act_event),))
        connection.commit()

    c.close()
    connection.close()
    return True


def generate_report(id_emp, data_from, data_to):
    try:
        datetime.datetime.strptime(data_from, "%Y-%m-%d %H:%M:%S")
        datetime.datetime.strptime(data_to, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("wrong date format")
        return False

    filename = str(id_emp) + "_" + datetime.datetime.now().strftime("raport_%Y-%m-%d_%H-%M-%S.csv")

    opened = opendb()
    if not opened:
        return False
    connection = opened[0]
    c = opened[1]

    # assuming that we can generate report only for actual employees
    c.execute("SELECT * FROM employees WHERE idEmp=?", (str(id_emp),))
    res = c.fetchone()
    if not res:
        print("There is no employee with this id")
        return False

    with open(filename, 'w', newline='') as report:
        writer = csv.writer(report, delimiter=";")
        writer.writerow(["ID: ", str(res[0]), "NAME: ", res[1], "LAST NAME: ", res[2],
                         "FROM: ", data_from, "TO: ", data_to])
        writer = csv.writer(report, delimiter=";")
        writer.writerow(["ID", "RFID", "TERMINAL-IN", "DATE-IN", "TERMINAL-OUT", "DATE-OUT", "TIME OF WORK"])
        c.execute("SELECT * FROM logs WHERE idEmp=? AND date BETWEEN ? AND ?", (str(id_emp), data_from, data_to,))
        res_log = c.fetchall()
        if res_log:
            if res_log[0][5] == 0:
                del res_log[0]

            for i in range(len(res_log)):
                datetime_format = '%Y-%m-%d %H:%M:%S'
                date_in = str(res_log[i - 1][1])
                date_out = str(res_log[i][1])
                diff = datetime.datetime.strptime(date_out, datetime_format) \
                       - datetime.datetime.strptime(date_in, datetime_format)
                if i % 2 == 1:
                    writer.writerow([str(res_log[i][0]), str(res_log[i][3]), str(res_log[i - 1][2]), date_in,
                                     str(res_log[i][2]), date_out, str(diff)])
    c.close()
    connection.close()
    return True


def rfid_scan_random():
    opened = opendb()
    if not opened:
        print("database cannot be opened")
        return ()
    connection = opened[0]
    c = opened[1]
    prob = rd.randint(1, 11)
    c.execute("SELECT idCard FROM assignments ORDER BY RANDOM() LIMIT 1")
    res_card = c.fetchone()
    if not res_card or prob > 9:
        card_id = str(rd.randint(1000, 10000))
    else:
        card_id = res_card[0]
    c.execute("SELECT idTerm FROM terminals ORDER BY RANDOM() LIMIT 1")
    res_term = c.fetchone()
    if not res_term:
        print("NO TERMINALS")
        return ()
    term_id = res_term[0]
    c.close()
    connection.close()
    return card_id, term_id
