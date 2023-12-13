from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

def crawler_controller(keyword):
    news = {}
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)

    news = naver_list(keyword, news, driver)
    news = naver_article(news, driver)
    
    # yahoo(keyword, news, driver)

    for source, articles in news.items():
        df = pd.DataFrame.from_dict(data=articles)
        df['source'] = source
        # print(df.head())
    
    df.to_csv('./article_before_preprocess_'+keyword+'.csv', sep='|', encoding='utf-8', index=False)

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
    id = 0
    for article in news['naver']:
        driver.get(article['url'])
        article['id'] = id
        id += 1
        article['title'] = driver.find_element(By.CLASS_NAME, "media_end_head_headline").find_element(By.XPATH, "./span").text
        article['text'] = driver.find_element(By.TAG_NAME, "article").get_attribute("innerHTML")

    return news

def yahoo(keyword, dict, driver):
    '''
    티커 검색하는거 만들어야함
    '''
    
    url = 'https://finance.yahoo.com/quote/'
    ticker = '005930.KS'
    dict['yahoo'] = []
    
    driver.get(url + ticker)
    news = driver.find_elements(By.CLASS_NAME, "js-stream-content Pos(r)")
    for article in news:
        '''
        광고 전처리 필요
        '''
        dict['yahoo'].append({"url":""})
        
    return dict

def yahoo_article(news, driver):
    pass
