import sys
from PyQt5.QtWidgets import *
import ui_design     


###### 부모 UI 정보 받아오기 ######
class SearchBot(ui_design.MyApp):   # 부모 class 명 입력

    def __init__(self):
        super().__init__()  
###################################



################### 버튼 기능 구현 ###################

    def showTotal(self) :       
        pass

    def showSpread(self) :
        pass




#######################################################



###### UI 창 열기 ######
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SearchBot()    
    sys.exit(app.exec_())
########################