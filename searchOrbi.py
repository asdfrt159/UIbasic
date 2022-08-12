from bs4 import BeautifulSoup
import requests
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time


class Crawling :
    
    def inputData(self) :
        self.usr_search = "설탭"
        self.usr_search_from = "0702"
        self.usr_search_to = "0802"


    def setSpread(self) :
        #### 구글 스프레드 시트 설정 부분 ####
        scope = ['https://spreadsheets.google.com/feeds']
        self.json_file_name = '/Users/silnun/searchBot_ui/avian-mile-358802-8d7f045864b7.json'
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.json_file_name, scope)
        gc = gspread.authorize(credentials)
        self.spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1NCrVULDi9_NJk8iXz6ol_0cgwr1Dt8TzCZ5DI8orfEg/edit?usp=sharing'
        doc = gc.open_by_url(self.spreadsheet_url)
        worksheet_list = doc.worksheets()
        if len(worksheet_list) == 1 :   # 구글 시트가 1개면 rawdata sheet 만들고, 2개면 새로 안만들고 불러온다.
            self.rawdata_ws = doc.add_worksheet(title = "raw data", rows = 101, cols = 5)
        else : 
            self.rawdata_ws = doc.get_worksheet(1)
        self.rawdata_ws.clear()   # 안에 내용 비우기
        self.rawdata_ws.append_row(['No', '날짜', '제목', '내용', '링크'])
        for i in self.final_data :
            self.rawdata_ws.append_row(i)


    def getPageList(self) :
        browser = requests.get("https://orbi.kr/search?q=" + self.usr_search + "&type=keyword")
        browser.raise_for_status()
        soup = BeautifulSoup(browser.text , "lxml")
        # usr_search 검색어로 찾아진 페이지 리스트 page_list 에 list 형식으로 저장
        pageList = soup.find("div", attrs={"class": "pagination"})
        pageListNo = pageList.find_all("a") # all 로 찾으면 뒤에 .get_text() 같은 단일 대상 함수를 붙일 수 없다.
        self.page_list = []
        for i in pageListNo:
            self.page_list.append(i.get_text())


    def mainfunc(self) :
        self.count_no = 1
        self.final_data = []

        for page in self.page_list:
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
                    self.final_data.append([self.count_no, content_date, content_title, content_body, content_link])
                    self.count_no += 1  
                else : 
                    continue
            time.sleep(1)   # 페이지 전환시 약간 대기
            # page 5 까지만 조회
            if page == '5' :
                break



if __name__ == '__main__':
    orbi = Crawling()
    orbi.inputData()
    orbi.getPageList()
    orbi.mainfunc()
    orbi.setSpread()