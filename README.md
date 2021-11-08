# SE_project
한국외대 2021-2 융복합소프트웨어전공 소프트웨어공학 7조 저장소입니다. 

## IDE는 VS Code를 기준으로 합니다. 


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
