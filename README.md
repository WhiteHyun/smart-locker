# Smart Locker

INU 20-21 캡스톤 디자인, Smart Locker

## git-flow

- [링크](https://woowabros.github.io/experience/2017/10/30/baemin-mobile-git-branch-strategy.html)

## 구현 사항

### 아두이노

- [x] 라즈베리파이와 시리얼 통신
  - [아두이노 코드](./src/locker_test.ino)
  - [라즈베리파이 코드](./main.py)
- [ ] 사물함과 연결

### 라즈베리파이

#### QR코드

- [x] [아두이노에서 받아온 사물함 정보와 유저의 정보를 도합해서 해시값 url 생성](./src/encrypt.py)
- [x] [url 해시값을 이용하여 QR코드 만들고 저장하기](./src/qrcodes/README.md)
- [x] [QR코드 인식하기](./src/qrcodes/README.md)
- [x] QR코드 인식 후 관련 사물(택배)함 문 열기
  - [아두이노 코드](./src/locker_test.ino)
  - [라즈베리파이 코드](./main.py)

### 응용프로그램

- [ ] 파이썬 tkinter로 메인 화면 구현

### 서버

- [ ] 데이터베이스 설계 및 구축
- [x] [클라이언트로부터 받아온 쿼리문을 가지고 데이터베이스 설정](./src/sql.py)

### 앱 (Swift)

- [ ] 사물(택배)함 앱 기초
- [ ] 서버(데이터베이스)와 앱간 통신 구현
