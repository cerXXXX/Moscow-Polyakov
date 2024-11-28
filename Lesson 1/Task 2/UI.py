import sys
import random
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QInputDialog


class RandomFlag(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 400)
        self.setWindowTitle('Рисование')
        self.button = QPushButton('Рисовать', self)
        self.button.move(70, 20)
        self.button.clicked.connect(self.paint)
        self.num = 0
        self.do_paint = False

    def paintEvent(self, event):
        if self.do_paint:
            qp = QPainter()
            qp.begin(self)
            self.draw_flag(qp)
            qp.end()

    def paint(self):
        self.do_paint = True
        self.repaint()

    def draw_flag(self, qp):
        r = random.randint(10, 400)
        qp.setBrush(QColor(255, 255, 0))
        qp.drawEllipse(10, 10, r, r)

