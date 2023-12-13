import requests
import json
import re
import pandas as pd

from kss import split_sentences
from lib.bkm import predict

import crawler

# 네이버 감정분석 config (추후에 yaml로 변경)
sentiment_url = 'https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze'
headers = {
    "X-NCP-APIGW-API-KEY-ID": "8fpmu1g52k",
    "X-NCP-APIGW-API-KEY": "qWUoG68iREE1Fc3mLhhHyFxSx28OewaJeYeG2sn6",
    "Content-Type": "application/json"
}

def preprocess(article):
    article = remove_tag(article)
    article = remove_lfcr(article)
    
    article_split = split_sentences(article, backend='mecab')
    
    return article_split

def remove_tag(text):
    tags = re.compile('<.*?>')
    return re.sub(tags, '', text)

def remove_lfcr(text):
    lfcr = re.compile('[\t\n\r\f\v"]')
    return re.sub(lfcr, '', text)

def pick_sentence(sentences, indexes):
        sum_text = ""
        for idx in indexes:
            sum_text += sentences[idx]
        return sum_text


def main():
    company_name = input('회사명을 입력해 주세요 : ')
    
    # 크롤링 단계
    print("1. 크롤링 시작, 회사명 : " + company_name)
    crawler.crawler_controller(keyword=company_name)
    # print(df.head())

    # 전처리 수행
    print("2. 전처리 시작, 회사명 : " + company_name)
    df = pd.read_csv('./article_before_preprocess_'+company_name+'.csv', delimiter='|')
    df['text'] = df['text'].apply(preprocess) # 전처리(태그삭제, 불필요한 개행문자 등 삭제)
    df['extractive'] = "" # 임시속성
    df['sum_text'] = ""
    df['sentiment'] = ""
    for i in range(len(df)):
        df['extractive'].loc[i] = [9999] # 비사용 단어 마킹용(무조건 해야하서 작성)

    # 문서요약(추출요약) 수행, 문장 idx 반환
    print("3. 문서요약 시작, 회사명 : " + company_name)
    prediction = predict.predict_wrapper(df=df)
    df = df.drop(['extractive'], axis=1) # 임시속성 삭제

    # 예측한 문장 인덱스를 바탕으로 요약문 생성
    for idx in range(len(prediction)):
        df['sum_text'].loc[idx] = pick_sentence(df['text'].loc[idx], prediction[idx])
        
    # 요약문 바탕, 감정분석 수행
    print("4. 감정분석 시작, 회사명 : " + company_name)
    data = {}
    for row in range(len(df)):
        data['content'] = df['sum_text'].loc[row]
        if len(data['content']) >= 1000:
            data['content'] = data['content'][:1000]
        response = requests.post(sentiment_url, headers=headers, data=json.dumps(data))

        if response.status_code != 200:
            print("error")
            raise Exception("네이버 감정분석 연결 실패")
            
        r = response.json()
        df['sentiment'].loc[row] = r['document']['sentiment']
        
    df.set_index("id")
    df.to_excel('./article_after_summary_'+company_name+'.xlsx', index=False)

if __name__ == "__main__":
    main()
