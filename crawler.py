from selnium import webdriver

def crawler_controller(keyword):
    news = {}

def naver(keyword, dict, driver):
    url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query="
    dict['naver'] = []

    driver.get(url + keyword)
    
    # 뉴스 리스트 추출
    driver.find_element(By.XPATH, "//*[@id="main_pack"]/section[1]/div/div[2]/ul")
    pass

def yahoo(keyword, dict, driver):
    dict['yahoo'] = []
    pass