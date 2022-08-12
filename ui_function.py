import sys
from PyQt5.QtWidgets import *
import ui_design     

###### 프로그램 실행 순서 ######
# 1. import py 전체 스캔
# 1.a. (스캔 도중) 내부 class 스캔 ( 클래스 함수 스캔 x )
# 2. main py 전체 스캔
# 2.a. (스캔 도중) 내부 class 스캔 ( 클래스 함수 스캔 x )
# 3. if 문 내부 변수 할당만으로 class 실행
# 4. main py init 함수 실행
# 5. superinit 키워드로 부모 init 실행
# 6. 부모 init 내부 함수 실행 (ui 창 오픈)
# 7. main py 로 돌아옴
# 참고 1. 부모,자식(main)에서 같은 함수명이 연결되어 있으면 '자식함수' 실행 ( 없으면 부모 함수 실행 )
# 참고 2. import 된 모듈은 중복되어도 상관없다.




###### 부모 UI 정보 받아오기 ######
class SearchBot(ui_design.MyApp):   # 부모 class 명 입력

    def __init__(self):
        super().__init__()  
###################################



################### 버튼 기능 구현 ###################

    def button1click(self) :       
        print("1")




#######################################################



###### UI 창 열기 ######
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SearchBot()    
    sys.exit(app.exec_())
########################