
from bs4 import BeautifulSoup
from selenium import webdriver

#driver = webdriver 객체
driver_google_news = webdriver.Chrome('/Users/J.J.Park/Desktop/KAIST/KAIST 2학년 겨울학기/Project_SuperDuperTradingBot/chromedriver.exe')
driver_yeonhab_news = webdriver.Chrome('/Users/J.J.Park/Desktop/KAIST/KAIST 2학년 겨울학기/Project_SuperDuperTradingBot/chromedriver.exe')
#driver_sbs_news = webdriver.Chrome('/Users/J.J.Park/Desktop/KAIST/KAIST 2학년 겨울학기/Project_SuperDuperTradingBot/chromedriver.exe')

#웹 자원 로드를 위해 기다리는 시간 설정 - 기본적으로는 다 로드 될 때까지 기다려줌
driver_google_news.implicitly_wait(100)
driver_yeonhab_news.implicitly_wait(100)
#driver_sbs_news.implicitly_wait(100)

#웹 연결
driver_google_news.get('https://news.google.com/?hl=ko&gl=KR&ceid=KR%3Ako')
driver_yeonhab_news.get('https://www.yna.co.kr/')
#driver_sbs_news.get('https://news.sbs.co.kr/news/newsMain.do')

##목표 1. 눈에 보이는 모든 텍스트 순차적으로 crawling

html_google_news = driver_google_news.page_source
html_yeonhab_news = driver_yeonhab_news.page_source
#html_sbs_news = driver_sbs_news.page_source

soup_google_news = BeautifulSoup(html_google_news,'html.parser')
google_news_contents_main = soup_google_news.select('article > h3 > a')
google_news_contents_sub = soup_google_news.select('h4 > a')

soup_yeonhab_news = BeautifulSoup(html_yeonhab_news,'html.parser')
yeonhab_news_contents = soup_yeonhab_news.select('div.news-con > h1 > a')
yeonhab_news_contents.append(soup_yeonhab_news.select(''))
yeonhab_news_contents.append(soup_yeonhab_news.select(''))
for main_content in google_news_contents_main:
    print(main_content.text)
for sub_content in google_news_contents_sub:
    print(sub_content.text)
for content in yeonhab_news_contents:
    print(content.text)
#yDmH0d > c-wiz > div > div.FVeGwb.CVnAc > div.ajwQHc.BL5WZb.RELBvb.zLBZs > div > main > c-wiz > div.lBwEZb.BL5WZb.xP6mwf > div.NiLAwe.mi8Lec.gAl5If.sMVRZe.Oc0wGc.R7GTQ.keNKEd.j7vNaf.nID9nc > div > article > h3 > a
#yDmH0d > c-wiz > div > div.FVeGwb.CVnAc > div.ajwQHc.BL5WZb.RELBvb.zLBZs > div > main > c-wiz > div.lBwEZb.BL5WZb.xP6mwf > div.NiLAwe.mi8Lec.gAl5If.sMVRZe.Oc0wGc.R7GTQ.keNKEd.j7vNaf.nID9nc > div > article > div.Da10Tb.Rai5ob > span
#yDmH0d > c-wiz > div > div.FVeGwb.CVnAc > div.ajwQHc.BL5WZb.RELBvb.zLBZs > div > main > c-wiz > div.lBwEZb.BL5WZb.xP6mwf > div.NiLAwe.mi8Lec.gAl5If.sMVRZe.Oc0wGc.R7GTQ.keNKEd.j7vNaf.nID9nc > div > div.SbNwzf > article:nth-child(1) > h4 > a
#yDmH0d > c-wiz > div > div.FVeGwb.CVnAc > div.ajwQHc.BL5WZb.RELBvb.zLBZs > div > main > c-wiz > div.lBwEZb.BL5WZb.xP6mwf > div.NiLAwe.mi8Lec.gAl5If.sMVRZe.Oc0wGc.R7GTQ.keNKEd.j7vNaf.nID9nc > div > div.SbNwzf > article:nth-child(2) > h4 > a
#yDmH0d > c-wiz > div > div.FVeGwb.CVnAc > div.ajwQHc.BL5WZb.RELBvb.zLBZs > div > main > c-wiz > div.lBwEZb.BL5WZb.xP6mwf > div.NiLAwe.mi8Lec.gAl5If.sMVRZe.Oc0wGc.R7GTQ.keNKEd.j7vNaf.nID9nc > div > div.SbNwzf > article:nth-child(4) > h4 > a
#yDmH0d > c-wiz > div > div.FVeGwb.CVnAc > div.ajwQHc.BL5WZb.RELBvb.zLBZs > div > main > c-wiz > div.lBwEZb.BL5WZb.xP6mwf > div:nth-child(3) > div > article > h3 > a
#yDmH0d > c-wiz > div > div.FVeGwb.CVnAc > div.ajwQHc.BL5WZb.RELBvb.zLBZs > div > main > c-wiz > div.lBwEZb.BL5WZb.xP6mwf > div:nth-child(3) > div > div.SbNwzf > article:nth-child(2) > h4 > a
#yDmH0d > c-wiz > div > div.FVeGwb.CVnAc > div.ajwQHc.BL5WZb.RELBvb.zLBZs > div > main > c-wiz > div.lBwEZb.BL5WZb.xP6mwf > div:nth-child(4) > div > article > h3 > a
#yDmH0d > c-wiz > div > div.FVeGwb.CVnAc > div.ajwQHc.BL5WZb.RELBvb.zLBZs > div > main > c-wiz > div.lBwEZb.BL5WZb.xP6mwf > div.NiLAwe.mi8Lec.gAl5If.sMVRZe.Oc0wGc.R7GTQ.keNKEd.j7vNaf.nID9nc > div > div.SbNwzf > article:nth-child(4) > h4 > a
#content > div.column-wrap > div.column-wide > div > div > div > div.img-con.img-cover.imgLiquid_bgSize.imgLiquid_ready > a > img
#content > div.column-wrap > div.col-cont.column-headline > div.column-area01 > div > ul > li:nth-child(1) > div.img-con.img-cover.imgLiquid_bgSize.imgLiquid_ready > a > img
#content > div.column-wrap > div.col-cont.column-headline > div.column-area01 > div > ul > li:nth-child(1) > div.news-con > h2 > a
#content > div.column-wrap > div.column-wide > div > div > div > div.news-con > h1 > a
#content > div.column-wrap > div.col-cont.column-headline > div.column-area02 > div.contents-box.list-type19.factcheck-zone > div > ul > li:nth-child(1) > a

