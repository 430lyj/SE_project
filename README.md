# SE_project (부엉아 밥먹자 by. 이문동 먹짱)
한국외대 2021-2 융복합소프트웨어전공 소프트웨어공학 7조 저장소입니다. 

## 구현 내용 및 우선순위
|     대항목     |       소항목       |     담당자     |   마감일시    |우선 구현 순위|
| :---: | :---: | :---: | :--- | :---:|
| DB 관련 | DB 테이블 생성 (회원, 식당) | 이연주 | 2021.11.21(일) |1|
|        | DB 인스턴스 추가 |     | 2021.11.21(일) |2|
|  회원 가입 | 기본 회원 가입 |      | 2021.11.      |3|
|         |  사업자 등록증 파일 업로드 란 만들기 |     |         |7|
|  회원 정보 수정 | 식당 정보 입력 페이지 만들기 |      |          |4|
|          |  식당별 메뉴 입력 페이지 만들기 |       |         |5|
|  관리자 |  회원 가입 승인 |      | 2021.11.  |7|
|       |   회원 정보 수정 |      |           |7|
| 식당 검색 기능 | 지도별 검색 | 이연주 | 2021. |6|
|            | 카테고리별 검색 |        |         |4|
|| 메뉴별 검색 | | |4|
|| 랜덤 추천 | | |6|
| 식당 정렬 기능 | 별점별 정렬 | | |5|
| | 가격별 정렬 | | |5|
| 디자인 템플릿| 디자인 작업 | | |동시 진행|
| | Django 템플릿 언어 사용한 병합 작업 | | |8|

* * *

## 사용 방법 
### IDE는 VS Code를 기준으로 합니다.

#### Mac 사용하시는 분들 중 git이 설치되지 않은 경우 다음 링크를 참고해주세요.

  https://cotak.tistory.com/74?category=450979
#### Window 사용하시는 분들 중 git이 설치되지 않은 경우 다음 링크를 참고해주세요.

  https://jstar0525.tistory.com/181
<hr/>
  
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
