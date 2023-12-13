# nlp_stock_recommand
## 프로젝트 설명
'23년 2학기 자연언어처리 프로젝트 - 주식관련 기사요약

## 설치
+ 파이썬 버전 : 3.7
+ requirements.txt 설치
```
pip install -r requirements.txt
```
+ 다운로드 : [bertsum-korean](https://github.com/Espresso-AI/bertsum-korean)
  - 설치 : lib/bkm 폴더 아래에 설치

## 사용법
+ 실행
```
python main.py
```
+ 기업이름 입력
```
회사명을 입력해 주세요 : {회사명}
```

## 학습데이터
+ [AI Hub 문서요약 텍스트](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=97)

## 학습

<img src="https://github.com/whtjdqja9923/nlp_stock_recommand/blob/main/training.png" width="850" height="350">

+ RTX4080 1대
+ CUDA 11.7
+ CuDNN 8.9.7
+ torch 1.13.1+cu117
+ torchvision 0.14.1
+ transformers 4.30.2
+ pyTorch Lightning 1.9

## 성능
|rouge1|rouge2|rougeL| 
|:---:|:---:|:---:|
|69.938|61.247|59.289|
