from selenium import webdriver
from selenium.webdriver.common.by import By

def crawler_controller(keyword):
    news = {}
    
    driver = webdriver.Chrome()
    naver(keyword, news, driver)
    yahoo(keyword, news, driver)

def naver(keyword, dict, driver):
    url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query="
    dict['naver'] = []

    driver.get(url + keyword)
    
    # 뉴스 리스트 추출
    driver.find_element(By.CLASS_NAME, "list_news")
    news = driver.find_elements(By.TAG_NAME, "li")
    
    for article in news:
        print(article)
    
    

def yahoo(keyword, dict, driver):
    dict['yahoo'] = []
    

crawler_controller("삼성전자")