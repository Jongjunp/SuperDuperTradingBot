
from bs4 import BeautifulSoup
from selenium import webdriver
import sqlite3

class Crawler:
    def __init__(self,page_address,webdriver_address,parser,category_tag,content_tag):
        self.page_address = page_address
        self.webdriver_address = webdriver_address
        self.parser = parser
        self.category_tag = category_tag
        self.content_tag = content_tag
        self.__waiting_time = 100
        self.connection = sqlite3.connect("./news.db")

    def GetCategory(self):
        categories = []

        #My_driver = webdriver 객체
        my_driver = webdriver.Chrome(self.webdriver_address)

        #웹 자원 로드를 위해 기다리는 시간 설정 - 기본적으로는 다 로드될 때까지 기다려준다
        my_driver.implicitly_wait(self.__waiting_time)

        #web connect
        my_driver.get(self.page_address)

        #page source loading
        page_source = my_driver.page_source

        #making BeautifulSoup object
        my_soup = BeautifulSoup(page_source,self.parser)

        #카테고리 추출
        categories_source = my_soup.select(self.category_tag)

        #카테고리를 저장, csv or .db file
        for category_source in categories_source:
            categories.append(category_source.text)

        return categories

    def GetContent(self):
        #data base
        cur = self.connection.cursor()

        #db 테이블 만들기
        cur.execute("CREATE TABLE NewsContents(category, content);")

        categories = self.GetCategory()

        # My_driver = webdriver 객체
        my_driver = webdriver.Chrome(self.webdriver_address)

        # 웹 자원 로드를 위해 기다리는 시간 설정 - 기본적으로는 다 로드될 때까지 기다려준다
        my_driver.implicitly_wait(self.__waiting_time)

        # web connect
        my_driver.get(self.page_address)

        #self.__categories에서 얻은 정보 이용
        for category in categories:
            my_driver.find_element_by_link_text(category).click()
            page_source = my_driver.page_source
            my_soup = BeautifulSoup(page_source,self.parser)
            contents_source = my_soup.select(self.content_tag)

            #콘텐츠 저장, csv or .db file
            for content_source in contents_source:
                cur.execute('INSERT INTO NewsContents(?,?);', (category, content_source.text))
                self.connection.commit()

        return