import sqlite3
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import (QMainWindow, QTableWidgetItem, QPushButton, QTableWidget, QStatusBar)
from UI.addEditCoffeeForm import *

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 300)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.move(0, 50)
        self.tableWidget.resize(800, 300)

        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.con = sqlite3.connect("data/coffee")
        self.modified = {}
        self.titles = None
        self.update_result()

        self.addcoffee = QPushButton(self)
        self.addcoffee.setText('Добавить')
        self.addcoffee.clicked.connect(self.add_coffee)
        self.addcoffee.move(0, 0)

        self.editcoffee = QPushButton(self)
        self.editcoffee.setText('Изменить')
        self.editcoffee.clicked.connect(self.edit_coffee)
        self.editcoffee.move(100, 0)

        self.deletecoffee = QPushButton(self)
        self.deletecoffee.setText('Удалить')
        self.deletecoffee.clicked.connect(self.delete_coffee)
        self.deletecoffee.move(200, 0)
    
    def add_coffee(self):
        dlg = CoffeeDialog()
        dlg.exec()
        self.update_result()
    
    def edit_coffee(self):
        id_ = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        print(id_)
        dlg = CoffeeDialog(id_)
        dlg.exec()
        self.update_result()
    
    def delete_coffee(self):
        id_ = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        print(id_)
        cur = self.con.cursor()
        cur.execute(f"DELETE FROM coffee WHERE id = {id_}")
        self.con.commit()
        self.update_result()
        

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute(f"SELECT * FROM coffee").fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        # Если запись не нашлась, то не будем ничего делать
        if not result:
            self.statusbar.showMessage('По этому запросу ничего не найдено')
            return
        else:
            self.statusbar.showMessage('')
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}
