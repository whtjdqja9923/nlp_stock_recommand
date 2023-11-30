from selenium import webdriver
from selenium.webdriver.common.by import By

def crawler_controller(keyword):
    news = {}
    
    driver = webdriver.Chrome()
    news = naver_list(keyword, news, driver)
    news = naver_article(news, driver)

    yahoo(keyword, news, driver)

def naver_list(keyword, dict, driver):
    url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query="
    dict['naver'] = []
    driver.get(url + keyword)
    
    # 뉴스 리스트 추출
    news = driver.find_element(By.CLASS_NAME, "list_news").find_elements(By.XPATH, "./child::li")
    
    for article in news:
        info_group = article.find_element(By.CLASS_NAME, "info_group")
        try:
            n_url = info_group.find_element(By.PARTIAL_LINK_TEXT, "네이버뉴스").get_attribute("href")
        except:
            pass
        dict['naver'].append({"url":n_url})
    
    return dict
    
def naver_article(news, driver):
    for article in news['naver']:
        driver.get(article['url'])
        article['title'] = driver.find_element(By.CLASS_NAME, "media_end_head_headline").find_element(By.XPATH, "./span").text
        article['main_text'] = driver.find_element(By.TAG_NAME, "article").get_attribute("innerHTML")

    return news

def yahoo(keyword, dict, driver):
    dict['yahoo'] = []
    

crawler_controller("삼성전자")