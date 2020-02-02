from text_processing.Web_Crawler import*

#html variables
Economics_html  = 'https://kr.investing.com/news/'
General_html = 'https://www.yna.co.kr/news'
My_webdriver_loc = '/Users/J.J.Park/Desktop/KAIST/KAIST 2학년 겨울학기/Project_SuperDuperTradingBot/chromedriver.exe'
My_parser = 'html.parser'
category_tag = 'nav.subMenuWrapper a'
content_tag = 'div.largeTitle > article.js-article-item.articleItem > div.textDiv > a'
detail_content_tag = 'div.WYSIWYG.articlePage > p'
table_name = 'Crawlingtestrealfinal'


if __name__== "__main__":
    crawler = Crawler(Economics_html, My_webdriver_loc, My_parser, category_tag, content_tag,detail_content_tag,table_name)

    categories = crawler.GetContent()

