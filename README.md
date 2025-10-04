# 🌱 국립경국대학교 디지털새싹 웹 플랫폼

본 프로젝트는 **Flask + SQLite** 기반으로 제작된  
**국립경국대학교 디지털새싹 교육사업 웹사이트**입니다.  
교사, 관리자, 학생이 함께 사용할 수 있는 통합형 플랫폼으로  
프로그램 소개, 게시판, 관리자 승인 시스템을 포함하고 있습니다.

---

## 📁 프로젝트 구조

📦 DigitalSeed-GKNU
├── app.py # Flask 메인 서버 파일
├── static/
│ ├── style.css # 전체 페이지 공통 스타일
│ ├── image/
│ │ ├── GKNU.png # 상단 CI 로고
│ │ ├── basic.jpg # 기본 썸네일 이미지
│ └── uploads/ # 게시물 업로드 이미지 저장 폴더
├── templates/
│ ├── index.html # 메인 페이지
│ ├── login.html # 로그인 페이지
│ ├── new_p.html # 회원가입 페이지
│ ├── admin.html # 관리자 페이지
│ ├── upload.html # 게시물 작성 페이지
│ ├── notice.html # 공지사항 페이지
│ ├── news.html # 보도자료 페이지
│ ├── imagepage.html # 활동사진 페이지
│ ├── support.html # 강사지원 안내 페이지
│ └── post_detail.html # 게시물 상세 페이지
├── database.db # SQLite 데이터베이스 파일
└── README.md # 깃허브 설명용 파일

yaml
코드 복사

---

## ⚙️ 기술 스택

| 구분 | 사용 기술 |
|------|------------|
| 백엔드 | Flask (Python 3.10), Flask_SQLAlchemy |
| 프론트엔드 | HTML5, CSS3 (기본 템플릿 기반) |
| 데이터베이스 | SQLite3 |
| 서버 구조 | Python Flask 내장 서버 |
| 배포 환경 | 카페24 / Synology / 로컬 테스트 지원 |

---

## 🧩 주요 기능

### 1. 사용자 시스템
- **회원가입 (new_p.html)**  
  - 이름, 소속, 아이디, 비밀번호 입력  
  - 첫 번째 가입자는 자동으로 `admin` 권한 부여  
  - 이후 가입자는 `pending` 상태 → 관리자 승인 필요  

- **로그인/로그아웃 (login.html)**  
  - 세션 기반 로그인 유지  
  - 승인 전 회원은 로그인 가능하지만 게시물 작성 불가  

---

### 2. 게시판 관리
- **카테고리별 업로드**  
  - `보도자료(news)`  
  - `공지사항(notice)`  
  - `강사지원(support)`  
  - `활동사진(photo)`  
- 파일 업로드 시 `/static/uploads/[카테고리]/` 폴더에 자동 저장  
- 이미지 미첨부 시 기본 이미지(`basic.jpg`)로 대체  

---

### 3. 관리자 페이지 (admin.html)
- 회원 등급 관리 (`admin`, `manager`, `user`, `pending`)
- 게시물 승인/삭제 기능
- 승인된 게시물만 일반 사용자에게 노출
- 모든 사용자와 게시물 데이터 표로 확인 가능

---

### 4. 시각적 디자인
- 상단 고정 메뉴바 (CI 로고 + 주요 메뉴)
- 각 게시판 및 상세 페이지에서 **둥근 모서리 / 그림자** 디자인 유지
- 모든 페이지 배경에 `background` 클래스 적용
- 반응형 지원 (800px 이하 자동 정렬)

---

## 🔐 권한 구조

| 역할 | 설명 | 주요 기능 |
|------|------|------------|
| **admin** | 최고 관리자 | 회원 등급 변경 / 게시물 승인 / 삭제 가능 |
| **manager** | 운영 관리자 | 게시물 승인 가능 |
| **user** | 일반 사용자 | 승인된 게시물 열람 / 댓글 (추후 기능) |
| **pending** | 대기 회원 | 관리자 승인 전까지 제한된 접근 |

---

## 🧠 프로그램 목적

본 플랫폼은  
**국립경국대학교 디지털새싹 사업단**의  
교육 프로그램, 보도자료, 강사 모집 및 사진 기록을  
한곳에서 관리하기 위한 **통합 웹 시스템**입니다.

- 프로그램 관리 자동화  
- 강사 및 교사 승인 절차 효율화  
- 공공 데이터 및 교육 프로그램의 투명한 운영 지원

---

## 🧩 향후 개선 예정

- 비밀번호 암호화 및 이메일 인증 절차 추가  
- 게시판 페이징 처리 및 댓글 기능 추가  
- 관리자 전용 대시보드 시각화 (통계 그래프 포함)  
- 회원 활동 로그 기록 기능

---

## 🖼️ 참고 이미지

| 구분 | 예시 |
|------|------|
| **메인 페이지** | ![index preview](https://github.com/baikjuwon/DigitalSeed-GKNU/blob/main/static/image/back2.png) |
| **활동사진 페이지** | ![photo page](https://github.com/baikjuwon/DigitalSeed-GKNU/blob/main/static/image/basic.jpg) |
| **CI 로고** | ![GKNU Logo](https://github.com/baikjuwon/DigitalSeed-GKNU/blob/main/static/image/GKNU.png) |

---

## 🏫 기관 정보

**국립경국대학교 디지털새싹 사업단**  
📧 이메일: swaicamp@naver.com  
📞 문의: 010-5812-8513  
📍 사업 개요 및 신청 안내: [공식 네이버 카페](https://cafe.naver.com/airoboedu/39)

---

## 🪄 실행 방법

```bash
# 1. 환경 설정
pip install flask flask_sqlalchemy

# 2. 데이터베이스 생성
python app.py  # 최초 실행 시 자동 생성

# 3. 로컬 서버 실행
python app.py

# 4. 웹 브라우저에서 접속
http://127.0.0.1:5000
