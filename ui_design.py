import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MyApp(QWidget):   

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):

        formbox = QFormLayout()
        vbox = QVBoxLayout()
        textbox = QVBoxLayout()

        frontLabel = QLabel("<b>Search Bot</b>")
        frontLabel.setAlignment(Qt.AlignCenter)
        frontLabel.setStyleSheet("font-size: 20px")
        orbiLabel = QLabel("[Orbi]\n")
        orbiLabel.setAlignment(Qt.AlignCenter)

        self.searchEdit = QLineEdit()
        self.datefromEdit = QLineEdit()
        self.datetoEdit = QLineEdit()

        self.totalButton = QPushButton("total 확인")
        self.totalButton.clicked.connect(self.showTotal)
        self.sheetButton = QPushButton("sheet 전송")
        self.sheetButton.clicked.connect(self.showSpread)
        vbox.addWidget(self.totalButton)
        vbox.addWidget(self.sheetButton)
        browserLabel = QLabel("상태창 :")
        self.textBrowser = QTextBrowser()
        vbox.addWidget(browserLabel)
        vbox.addWidget(self.textBrowser)
        
        textLabel1 = QLabel("<b>사용방법</b>")
        textLabel2 = QLabel("1. 주어진 조건을 입력")
        textLabel3 = QLabel("2. 날짜는 반드시 MMdd 형식으로 입력")
        textLabel4 = QLabel("3. total 확인 : 간단한 총량 확인")
        textLabel5 = QLabel("4. sheet 전송 : 스프레드 시트에 raw data 전송")
        textbox.addWidget(textLabel1)
        textbox.addWidget(textLabel2)
        textbox.addWidget(textLabel3)
        textbox.addWidget(textLabel4)
        textbox.addWidget(textLabel5)

        formbox.addRow(frontLabel)
        formbox.addRow(orbiLabel)
        formbox.addRow("검색어 : ", self.searchEdit)
        formbox.addRow("시작일 : ", self.datefromEdit)
        formbox.addRow("종료일 : ", self.datetoEdit)
        formbox.addRow(vbox)
        #formbox.addRow(textbox)
        self.setLayout(formbox)

        # 화면띄우기
        self.setWindowTitle("Search Bot")
        self.resize(200,300)
        self.show() 

    def showTotal(self):
        pass

    def showSpread(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())