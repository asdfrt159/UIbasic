import sys
from PyQt5.QtWidgets import *


class MyApp(QWidget):   

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.formbox = QFormLayout()
        self.button1 = QPushButton("button1")
        self.button1.clicked.connect(self.button1click)
        self.formbox.addRow("hi: ", QLineEdit())
        self.formbox.addRow(self.button1)
        self.setLayout(self.formbox)


        self.setWindowTitle('My First Application')
        self.move(300, 300)
        self.resize(400, 200)
        self.show()

    def button1click(self):
        print("myapp buttonclick")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())