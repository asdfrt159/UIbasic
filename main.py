import sys
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup
import requests
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import ui_design     
import searchOrbi



###### 부모 UI 정보 받아오기 ######
class SearchBot(ui_design.MyApp, searchOrbi.Crawling):   # 상속했을 때는 그냥 self.함수명() 해서 바로 부모의 함수를 들고 올 수 있다.

    def __init__(self):
        super().__init__()  
###################################



################# 버튼 기능부 ####################

    #### 검색 받아오기 ####
    def getInfo(self) :
        self.usr_search = self.searchEdit.text()   # 검색어
        self.usr_search_from = self.datefromEdit.text()   # 검색 date min 값 (format = 'MMdd')  
        self.usr_search_to = self.datetoEdit.text()   # 검색 date max 값 (format = 'MMdd')

    def showTotal(self) :       
        self.getInfo()
        self.getPageList()  # searchOrbi 상속
        self.mainfunc()     # searchOrbi 상속

        #### TextBrowser 에 출력하기 ####
        self.textBrowser.clear()
        self.textBrowser.append("[total 확인]")
        self.textBrowser.append("검색어 : " + self.usr_search)
        self.textBrowser.append("시작일 : " + self.usr_search_from + "  |  종료일 : " + self.usr_search_to)
        self.textBrowser.append("total 검색량 : <b>[" + str(self.count_no - 1) + "]</b>")
        
    def showSpread(self) :
        self.getInfo()
        self.getPageList()  # searchOrbi 상속
        self.mainfunc()     # searchOrbi 상속
        self.setSpread()    # searchOrbi 상속

        #### TextBrowser 에 출력하기 ####
        self.textBrowser.clear()
        self.textBrowser.append("[Spread sheet에 raw data 전송]")
        self.textBrowser.append("검색어 : " + self.usr_search)
        self.textBrowser.append("시작일 : " + self.usr_search_from + "  |  종료일 : " + self.usr_search_to)
        self.textBrowser.append("<b>"+str(self.count_no-1)+"개 등록 완료!!</b>")
        self.textBrowser.append("Spread Sheet를 확인하세요.")   


#######################################################



###### UI 창 열기 ######
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SearchBot()    
    sys.exit(app.exec_())
########################