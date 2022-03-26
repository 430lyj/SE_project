# SE_project (부엉아 밥먹자 by. 이문동 먹짱)
한국외대 2021-2 융복합소프트웨어전공 소프트웨어공학 7조 저장소입니다. 

본 프로젝트는 이문동 인근의 맛집 소개를 목표로 제작되었습니다. 프로젝트는 메뉴를 검색하면 해당 메뉴를 판매하는 식당을 보여주는 기능, 카테고리별로 분류된 식당, 랜덤하게 추천하는 기능 등이 구현되어 있습니다. 음식점 소유주만이 회원 가입할 수 있으며, 인증된 사용자들은 자신의 식당 정보를 자유롭게 수정할 수 있습니다. 

## 구현 내용 이미지
|메인페이지|회원가입|
|:-:|:-:|
|<img width="390" alt="image" src="https://user-images.githubusercontent.com/75655613/160249026-4b63d324-b5a3-412b-9e01-cf3c524b053a.png">|<img width="390" alt="image" src="https://user-images.githubusercontent.com/75655613/160249021-ea09cccb-f7d5-4f83-9ba2-94a0bb525b1b.png">|
|로그인|관리자 페이지에서 회원에 대한 권한 수정 가능|
|<img width="390" alt="image" src="https://user-images.githubusercontent.com/75655613/160249079-62e5c20c-a97a-417a-aced-6d00048d89d8.png">|<img width="390" alt="image" src="https://user-images.githubusercontent.com/75655613/160249087-c6b72901-2921-4f8f-8fa9-27fe8dc1e402.png">|
|카테고리별 식당 선택|카테고리별 식당 조회 결과|
|<img width="390" alt="image" src="https://user-images.githubusercontent.com/75655613/160249132-a30c6f4d-f39d-4ddb-872d-cd7a8f27ef05.png">|<img width="390" alt="image" src="https://user-images.githubusercontent.com/75655613/160249138-c4a087db-fc66-48b8-8ef3-b1f93e9aaf1f.png">|
|위치별 검색|랜덤 추천|
|<img width="390" alt="image" src="https://user-images.githubusercontent.com/75655613/160249159-2e824517-53a1-4354-b30f-8f8e61e81cdf.png">|<img width="390" alt="image" src="https://user-images.githubusercontent.com/75655613/160250008-21d6d1dd-61b1-45c8-8d51-dfb53ed5c51f.png">|
|최소 가격별 정렬|평점별 정렬|
|<img width="390" alt="image" src="https://user-images.githubusercontent.com/75655613/160250082-b7d20b03-4093-4926-b358-47f23ad95493.png">|<img width="390" alt="image" src="https://user-images.githubusercontent.com/75655613/160250118-a5ac4d98-16d8-40bd-a53d-2fe189e37d9d.png">|

## 구현 내용 및 우선순위
|     대항목     |       소항목       |     담당자     |   마감일시    |우선 구현 순위|
| :---: | :---: | :---: | :---: | :---:|
| DB 관련 | DB 테이블 생성 (회원, 식당) | 이연주 | 완료 |1|
|        | DB 인스턴스 추가 |정성우| 완료 |2|
|  회원 가입 | 기본 회원 가입 |엄소현| 완료 |3|
|         |  사업자 등록증 파일 업로드 란 만들기 |엄소현| 완료        |7|
|  회원 정보 수정 | 식당 정보 입력 페이지 만들기 |박승리|완료|4|
|          |  식당별 메뉴 입력 페이지 만들기 |박승리|완료|5|
|  관리자 |  회원 가입 승인 |박승리|완료|7|
|       |   회원 정보 수정 |박승리|완료|7|
| 식당 검색 기능 | 지도별 검색 | 이연주 | 완료 |6|
|| 메뉴별 검색 + 카테고리 추후 추가 |엄소현| 완료 |4|
|| 랜덤 추천 |정성우|완료|6|
| 식당 정렬 기능 | 별점별 정렬 | 이연주 | 완료 |5|
| | 가격별 정렬 | 이연주| 완료 |5|
| 디자인 템플릿| 디자인 작업 | 정수현| 완료 |동시 진행|
| | Django 템플릿 언어 사용한 병합 작업 |정수현|완료|8|

* * *

## 사용 방법 
### IDE는 VS Code를 기준으로 합니다.
  
#### 깃에서 초기 파일을 내려 받는 방법 (VS code에서 빈 폴더 생성 후)
```
$ git clone https://github.com/430lyj/SE_project.git
```
#### 가상환경 생성하기 및 켜기
```
$ cd SE_project
$ python3 -m venv myvenv
$ source myvenv/bin/activate      //Mac
$ source myvenv/scripts/activate  // Windows
```
#### 프로젝트에 필요한 패키지 다운로드
```
$ pip install -r requirements.txt
```
#### .env 파일 생성 
  - 프로젝트 루트 디렉토리 (`/SE_project`)에 작성
```
$ touch .env
```
  - 필요 환경변수
  ```bash
  SECRET_KEY=
  ```
#### 잘 다운로드 받아졌는지 확인
```
$ cd imundongmukjjang
$ python manage.py runserver
```
