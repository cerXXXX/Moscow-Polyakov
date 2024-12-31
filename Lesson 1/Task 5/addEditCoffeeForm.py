from PyQt6.QtWidgets import *
import sqlite3


class CoffeeDialog(QDialog):
    def __init__(self, id_=None):
        super().__init__()
        self.setWindowTitle("Add Coffee")
        self.resize(300, 150)
        
        self.layout = QFormLayout(self)
        self.name = QLineEdit()
        self.grade = QLineEdit()
        self.type = QComboBox()
        self.taste = QLineEdit()
        self.price = QLineEdit()
        self.size = QLineEdit()

        self.type.addItems(["молотый", "в зернах"])

        self.but = QPushButton("Добавить")
        

        self.layout.addRow("Название", self.name)
        self.layout.addRow("Сорт", self.grade)
        self.layout.addRow("Тип", self.type)
        self.layout.addRow("Вкус", self.taste)
        self.layout.addRow("Цена", self.price)
        self.layout.addRow("Объем упаковки", self.size)
        self.layout.addRow(self.but)

        if id_:
            self.setWindowTitle("Edit Coffee")
            with sqlite3.connect("coffee") as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM coffee WHERE id=?", (id_,))
                row = cur.fetchone()
                self.name.setText(str(row[1]))
                self.grade.setText(str(row[2]))
                self.type.setCurrentText(str(row[3]))
                self.taste.setText(str(row[4]))
                self.price.setText(str(row[5]))
                self.size.setText(str(row[6]))
                self.but.setText("Изменить")
                self.but.clicked.connect(self.editCoffee)
        else:
            self.but.clicked.connect(self.addCoffee)
        
        self.id_ = id_
                
    
    def addCoffee(self):
        with sqlite3.connect("coffee") as conn:
            conn.execute("INSERT INTO coffee (grade, roasting, type, taste, price, package) VALUES (?, ?, ?, ?, ?, ?)", (self.name.text(), self.grade.text(), self.type.currentText(), self.taste.text(), self.price.text(), self.size.text()))
            conn.commit()
        self.close()
    
    def editCoffee(self):
        with sqlite3.connect("coffee") as conn:
            conn.execute("UPDATE coffee SET grade=?, roasting=?, type=?, taste=?, price=?, package=? WHERE id=?", (self.name.text(), self.grade.text(), self.type.currentText(), self.taste.text(), self.price.text(), self.size.text(), self.id_))
            conn.commit()
        self.close()
        