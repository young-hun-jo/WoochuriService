# 🐮 우추리 축산 일일 매출 예측 프로젝트 🐷

## 🎯 프로젝트 목적
- 대전광역시 서구 도화공원길 21에 위치한 우추리 축산
- 2020년 2월 이후로 세계적으로 확산된 코로나 신종 바이러스로 인해 매출의 타격에 큰 영향을 입게 된 상태
- 머신 러닝을 활용하여 **일일 매출을 실시간으로 예측**해 정육 재고 관리를 최적화하고 최종적으로 **운영 비용 최소화 목적**

## 📋 데이터 명세서
- *우추리 축산 일 매출 데이터*
  * 영업 오픈일 2009-01-01 ~ 현재까지의 일 매출 데이터
  * 수기로 직접 수집
 
- *지상(종관, ASOS) 일자료 조회 서비스*
  * 공공 데이터 [Open API](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15059093)
  * 평균기온
  * 최저기온
  * 최고기온
  * 1시간 최다강수량
  * 일 강수량
  * 평균풍속
  * 최대풍속
  * 평균상대습도
  * 최소상대습도
  * 1시간 최다일사량
  * 일사량
 
- *축산물등급판정 서비스*
  * 공공 데이터 [Open API](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15058822)
  * 한우와 육우 도매 가격
    - 2009-01-01~2011-03-02 까지는 전국 도매 가격 
    - 2011-03-03~현재 까지는 중부권 도매 가격(대전이 중부권에 속함)
  * 돼지 탕박 도매 가격
    - 돼지 박피 도매 가격도 있었으나 현재 돼지고기의 약 97%가 돼지 탕박을 사용하기 때문에 박피 데이터는 제외
    - [돼지 탕박과 돼지 박피의 차이점](https://m.blog.naver.com/PostView.nhn?blogId=dsf-mall&logNo=221503684858&proxyReferer=https:%2F%2Fwww.google.com%2F)

## 🛠 데이터 전처리
- 결측치
  * 지상(종관, ASOS) 일자료 데이터
    - 해당 데이터 변수들은 서로 상관성이 높기 때문에 Pearson Correlation을 기반으로 하여 [KNN(K-Nearest-Neighbors) Imputer](https://scikit-learn.org/stable/modules/generated/sklearn.impute.KNNImputer.html) 사용
    
- 이상치
  * 한우와 육우 도매 가격
    - [한우 가격은 육우 가격의 약 1.8배](https://www.google.com/search?q=%EC%9C%A1%EC%9A%B0+%ED%95%9C%EC%9A%B0+%EA%B0%80%EA%B2%A9%EC%B0%A8%EC%9D%B4&oq=%ED%95%9C%EC%9A%B0+%EC%9C%A1%EC%9A%B0&aqs=chrome.4.69i57j69i59j35i39j0i8i30l4j69i61.3516j0j4&sourceid=chrome&ie=UTF-8)로 책정. 이를 이용해 로직 구현
    - 한우 가격이 잘못 책정된 날짜일 경우 ➡️ 해당 날짜의 육우가격을 이용해 이상치 대체
    - 육우 가격이 잘못 책정된 날짜일 경우 ➡️ 해당 날짜의 한우가격을 이용해 이상치 대체
 
 - 명절, 공휴일 파생변수 생성
  * 설, 추석 명절
    - 우추리 축산은 항상 명절 당일 직전날까지 영업 게시
    - EDA 결과, 명절 이벤트로 인해 명절 당일 직전날로부터 과거 6일간 매출이 평소와 다르게 매우 높은 것으로 관찰
    - [holidays](https://pypi.org/project/holidays/) 오픈소스를 이용해 대한민국의 명절 데이터를 미리 로드하고 해당 날짜로부터 6일 이내에 명절 당일 직전날이 존재하면 가중치를 1부터 6까지 차등적으로 부여
      - 위와 같은 로직을 사용해 
        
