from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sqlite3
from sqlite3 import Error
import sys

ui, _ = loadUiType('main.ui')


def create_conn():
    conn = None
    try:
        conn = sqlite3.connect('persons.db')
    except Error as e:
        print(f'Error: "{e}"')
    finally:
        if conn:
            conn.close()


def create_table():
    conn = sqlite3.connect('persons.db')
    try:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS persons (
                id INTEGER NOT NULL PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                address TEXT NOT NULL,
                phone TEXT NOT NULL,
                dob TEXT NOT NULL,
                gender TEXT NOT NULL
            )
        ''')
    except Error as e:
        print(f'Error: "{e}"')


def insert_data(data):
    conn = sqlite3.connect('persons.db')
    try:
        c = conn.cursor()
        c.execute('''
            INSERT INTO persons (
                id, first_name, last_name, address, phone, dob, gender
            ) VALUES (
                ?,?,?,?,?,?,?
            )
        ''', data)
    except Error as e:
        print(f'Error: "{e}"')
    conn.commit()


def delete_data(del_id):
    conn = sqlite3.connect('persons.db')
    try:
        c = conn.cursor()
        c.execute('''
            DELETE FROM persons WHERE id=?
        ''', del_id)
        conn.commit()
    except Error as e:
        print(f'Error: "{e}"')


def display_all():
    conn = sqlite3.connect('persons.db')
    c = conn.cursor()
    c.execute("SELECT * FROM persons")
    rows = c.fetchall()
    res = []
    for row in rows:
        res.append(row)
    return res


class MainWin(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        create_conn()
        create_table()
        self.handle_buttons()
        self.setStyleSheet('''
        
        ''')

    def handle_buttons(self):
        self.ADD.clicked.connect(self.handle_add)
        self.DELETE.clicked.connect(self.handle_delete_by_id)
        self.VIEWALL.clicked.connect(self.handle_view_all)

    def handle_add(self):
        data = (
            self.ID.text(),
            self.FIRSTNAME.text(),
            self.LASTNAME.text(),
            self.ADDRESS.text(),
            self.PHONE.text(),
            self.DOB.text(),
            self.GENDER.text()
        )
        insert_data(data)
        print("ENTRY ADDED")
        self.ID.setText('')
        self.FIRSTNAME.setText('')
        self.LASTNAME.setText('')
        self.ADDRESS.setText('')
        self.PHONE.setText('')
        self.DOB.setText('')
        self.GENDER.setText('')

    def handle_delete_by_id(self):
        delete_data(self.DELID.text())
        print(f"ENTRY #{self.DELID.text()} DELETED")
        self.DELID.setText('')

    def handle_view_all(self):
        self.DATAVIEW.setPlainText('')
        dataset = display_all()
        for data in dataset:
            self.DATAVIEW.appendPlainText('-'*25)
            self.DATAVIEW.appendPlainText(
                f'ID >> {str(data[0])}\nNAME >> {str(data[1])} {str(data[2])}\nADDRESS >> {str(data[3])}\nPHONE >> {str(data[4])}\nDoB >> {str(data[5])}\nGENDER >> {str(data[6])}'
            )
            self.DATAVIEW.appendPlainText('-'*25)
        print("DATA DISPLAY DONE")


def main():
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    app.exec()


if __name__ == '__main__':
    main()
