import sqlite3
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import (QMainWindow, QTableWidgetItem, QPushButton, QTableWidget, QStatusBar)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500, 300)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.move(0, 50)
        self.tableWidget.resize(500, 300)

        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.con = sqlite3.connect("coffee")
        self.modified = {}
        self.titles = None
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
