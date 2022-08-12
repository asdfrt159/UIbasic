from re import search
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from bs4 import BeautifulSoup
import requests
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time


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

    


  



  #################### 버튼 시그널 기능 구현 ####################
  # 값 받아오는 것 signal func 부에 와야 한다.  

  # total 확인 버튼 함수
  def showTotal(self):

    #### 검색 받아오기 ####
    self.usr_search = self.searchEdit.text()   # 검색어
    self.usr_search_from = self.datefromEdit.text()   # 검색 date min 값 (format = 'MMdd')  
    self.usr_search_to = self.datetoEdit.text()   # 검색 date max 값 (format = 'MMdd')

    #### 크롤링 부분 ####
    browser = requests.get("https://orbi.kr/search?q=" + self.usr_search + "&type=keyword")
    browser.raise_for_status()
    soup = BeautifulSoup(browser.text , "lxml")
    # usr_search 검색어로 찾아진 페이지 리스트 page_list 에 list 형식으로 저장
    pageList = soup.find("div", attrs={"class": "pagination"})
    pageListNo = pageList.find_all("a") # all 로 찾으면 뒤에 .get_text() 같은 단일 대상 함수를 붙일 수 없다.
    page_list = []
    for i in pageListNo:
      page_list.append(i.get_text())

    self.count_no = 1

    for page in page_list:
      browser = requests.get("https://orbi.kr/search?q=" + self.usr_search + "&type=keyword&page=" + page)
      browser.raise_for_status()
      soup = BeautifulSoup(browser.text , "lxml")

      # 검색 조건에 맞는 모든 list 반환
      content = soup.find("ul", attrs={"class": "post-list"})
      contentBody = content.find_all("li")

      for i in contentBody:
        content_date = i.abbr.get_text().strip()  # 날짜

        if len(content_date) == 14 :
          break
        content_date_day = content_date[:2]+content_date[3:5]
        content_date_day = int(content_date_day)

        if content_date_day >= int(self.usr_search_from) and content_date_day <= int(self.usr_search_to) :
          content_title = i.find("p", attrs={"class": "title"}).a.get_text().strip()  # 제목
          content_body = i.find(attrs={"class":"content"}).get_text().strip() # 내용
          content_link = "https://orbi.kr" + i.find("p", attrs={"class": "title"}).a['href'].strip()  # link
          final_data = [self.count_no, content_date, content_title, content_body, content_link]
          #writer.writerow(final_data)
          #rawdata_ws.append_row(final_data)
          self.count_no += 1  
        else : 
          continue
      time.sleep(1)   # 페이지 전환시 약간 대기

      # page 5 까지만 조회
      if page == '5' :
        break

    #### TextBrowser 에 출력하기 ####
    self.textBrowser.clear()
    self.textBrowser.append("[total 확인]")
    self.textBrowser.append("검색어 : " + self.usr_search)
    self.textBrowser.append("시작일 : " + self.usr_search_from + "  |  종료일 : " + self.usr_search_to)
    self.textBrowser.append("total 검색량 : <b>[" + str(self.count_no - 1) + "]</b>")


  # sheet 전송 버튼 함수
  def showSpread(self):

    #### 검색 받아오기 ####
    self.usr_search = self.searchEdit.text()   # 검색어
    self.usr_search_from = self.datefromEdit.text()   # 검색 date min 값 (format = 'MMdd')  
    self.usr_search_to = self.datetoEdit.text()   # 검색 date max 값 (format = 'MMdd')

    
    #### 구글 스프레드 시트 설정 부분 ####
    scope = ['https://spreadsheets.google.com/feeds']
    json_file_name = '/Users/silnun/community_search/avian-mile-358802-8d7f045864b7.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
    gc = gspread.authorize(credentials)
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1NCrVULDi9_NJk8iXz6ol_0cgwr1Dt8TzCZ5DI8orfEg/edit?usp=sharing'
    doc = gc.open_by_url(spreadsheet_url)
    worksheet_list = doc.worksheets()
    if len(worksheet_list) == 1 :   # 구글 시트가 1개면 rawdata sheet 만들고, 2개면 새로 안만들고 불러온다.
      rawdata_ws = doc.add_worksheet(title = "raw data", rows = 101, cols = 5)
    else : 
      rawdata_ws = doc.get_worksheet(1)
    rawdata_ws.clear()   # 안에 내용 비우기
    rawdata_ws.append_row(['No', '날짜', '제목', '내용', '링크'])



    #### 크롤링 부분 ####
    browser = requests.get("https://orbi.kr/search?q=" + self.usr_search + "&type=keyword")
    browser.raise_for_status()
    soup = BeautifulSoup(browser.text , "lxml")
    # usr_search 검색어로 찾아진 페이지 리스트 page_list 에 list 형식으로 저장
    pageList = soup.find("div", attrs={"class": "pagination"})
    pageListNo = pageList.find_all("a") # all 로 찾으면 뒤에 .get_text() 같은 단일 대상 함수를 붙일 수 없다.
    page_list = []
    for i in pageListNo:
      page_list.append(i.get_text())

    self.count_no = 1

    for page in page_list:
      browser = requests.get("https://orbi.kr/search?q=" + self.usr_search + "&type=keyword&page=" + page)
      browser.raise_for_status()
      soup = BeautifulSoup(browser.text , "lxml")

      # 검색 조건에 맞는 모든 list 반환
      content = soup.find("ul", attrs={"class": "post-list"})
      contentBody = content.find_all("li")

      for i in contentBody:
        content_date = i.abbr.get_text().strip()  # 날짜

        if len(content_date) == 14 :
          break
        content_date_day = content_date[:2]+content_date[3:5]
        content_date_day = int(content_date_day)

        if content_date_day >= int(self.usr_search_from) and content_date_day <= int(self.usr_search_to) :
          content_title = i.find("p", attrs={"class": "title"}).a.get_text().strip()  # 제목
          content_body = i.find(attrs={"class":"content"}).get_text().strip() # 내용
          content_link = "https://orbi.kr" + i.find("p", attrs={"class": "title"}).a['href'].strip()  # link
          final_data = [self.count_no, content_date, content_title, content_body, content_link]
          rawdata_ws.append_row(final_data)
          self.count_no += 1  
        else : 
          continue
      time.sleep(1)   # 페이지 전환시 약간 대기
      # page 5 까지만 조회
      if page == '5' :
        break

    #### TextBrowser 에 출력하기 ####
    self.textBrowser.clear()
    self.textBrowser.append("[Spread sheet에 raw data 전송]")
    self.textBrowser.append("검색어 : " + self.usr_search)
    self.textBrowser.append("시작일 : " + self.usr_search_from + "  |  종료일 : " + self.usr_search_to)
    self.textBrowser.append("<b>"+str(self.count_no-1)+"개 등록 완료!!</b>")
    self.textBrowser.append("Spread Sheet를 확인하세요.")


if __name__ == '__main__' :
  app = QApplication(sys.argv)
  ex = MyApp()
  sys.exit(app.exec_())