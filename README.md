# 💙 OurWish

> 목표만 알려주면 내게 맞는 예·적금, 빠르게 찾아드릴게요.

**OurWish**는 기간과 금액, 우대조건을 입력하면 조건에 맞는 예·적금 상품을 추천하고, 예상 수령액과 상품 정보를 쉽게 확인할 수 있도록 돕는 AI 금융 서비스입니다.  
복잡한 금리 조건과 약관은 AI가 쉬운 말로 설명해주고, 가입 후에는 마이페이지에서 진행률과 만기 일정을 관리할 수 있습니다.

<br />

## 🔗 서비스 링크

| 구분        | 링크                                |
| ----------- | ----------------------------------- |
| 배포 사이트 | https://our-wish.site/              |
| GitHub      | https://github.com/Our-Wish/ourwish |

<br />

## 📌 목차

- [팀원 정보 및 역할 분담](#-팀원-정보-및-역할-분담)
- [서비스 주요 기능](#-서비스-주요-기능)
- [서비스 흐름](#-서비스-흐름)
- [기술 스택](#️-기술-스택)
- [프로젝트 구조](#-프로젝트-구조)
- [프론트엔드 컴포넌트 구조](#-프론트엔드-컴포넌트-구조)
- [실행 방법](#-실행-방법)
- [금융 상품 추천 알고리즘 기술적 설명](#-금융-상품-추천-알고리즘-기술적-설명)
- [생성형 AI 활용 내용](#-생성형-ai-활용-내용)
- [프로젝트 후기 및 느낀 점](#-프로젝트-후기-및-느낀-점)

<br />

## 🧑🏻‍💻 팀원 정보 및 역할 분담

| 이름   | 담당          | 주요 역할                                                                               |
| ------ | ------------- | --------------------------------------------------------------------------------------- |
| 김주우 | Backend · AI  | Django REST API, DB 모델링, 금융 상품 데이터 처리, 추천 알고리즘, AI 기능 연동          |
| 안서진 | Frontend · AI | Vue 3 UI/UX, TypeScript, Pinia 상태관리, 반응형 화면 구현, 상품 추천/상세/마이페이지 UI |

<br />

<table>
  <tbody>
    <tr>
      <td align="center">
        <a href="https://github.com/kimzoo5676-del">
          <img alt="kimzoo5676-del" src="https://avatars.githubusercontent.com/kimzoo5676-del" width="140" />
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/xxj15">
          <img alt="xxj15" src="https://avatars.githubusercontent.com/u/63233128?v=4" width="140" />
        </a>
      </td>
    </tr>
    <tr>
      <td align="center">
        <a href="https://github.com/kimzoo5676-del"><b>김주우</b></a><br />
        Backend · AI<br />
        <sub>추천 알고리즘 · Django REST API · DB 모델링</sub>
      </td>
      <td align="center">
        <a href="https://github.com/xxj15"><b>안서진</b></a><br />
        Frontend · AI<br />
        <sub>Vue 3 UI/UX · Pinia 상태관리 · 반응형 디자인</sub>
      </td>
    </tr>
  </tbody>
</table>

<br />

## ✨ 서비스 주요 기능

### 🏠 랜딩 페이지

사용자가 서비스에 처음 진입했을 때 예금/적금 추천 기능으로 자연스럽게 이동할 수 있도록 구성했습니다.  
데스크탑과 모바일 화면을 각각 고려해 랜딩 화면을 분리하고, 목표 기반 금융 추천 서비스라는 핵심 메시지를 전달합니다.

|                   랜딩 페이지                    |
| :----------------------------------------------: |
| ![랜딩 페이지](docs/screenshots/landingPage.gif) |

<br />

### 💰 예·적금 상품 추천

사용자가 기간, 금액, 우대조건을 입력하면 조건에 맞는 예·적금 상품을 추천합니다.  
적금과 예금은 납입 방식이 다르기 때문에 목표 설정 흐름을 분리했고, 사용자가 입력한 조건을 기준으로 예상 수령액을 계산할 수 있도록 구성했습니다.

#### 주요 기능

- 적금 / 예금 추천 플로우 분리
- 기간, 금액, 우대조건 입력
- 은행 및 상품 조건 필터링
- 세후 예상 수령액 계산
- 기본금리 / 최고금리 / 예상 수령액 기준 비교
- 선택한 우대조건을 모두 충족하는 상품 확인

|               목표 설정 STEP 1               |                목표 설정 STEP 2                |
| :------------------------------------------: | :--------------------------------------------: |
| ![goalSetUp](docs/screenshots/goalSetUp.png) | ![goalSetUp2](docs/screenshots/goalSetUp2.png) |

|                     상품 추천 결과                     |
| :----------------------------------------------------: |
| ![recommendation](docs/screenshots/recommendation.png) |

<br />

### 🔍 상품 상세

추천된 금융 상품의 상세 정보를 한 페이지에서 확인할 수 있습니다.  
금융감독원 원문 정보, 금리 정보, 우대조건, 세후 수익 계산, 영업점 검색, AI 챗봇을 함께 제공해 상품 이해부터 가입 전 확인까지 이어질 수 있도록 구성했습니다.

#### 주요 기능

- 상품 기본 정보 확인
- 기본금리 / 최고금리 확인
- 우대조건 및 가입 제한 정보 확인
- AI 쉬운말 상품 요약
- 예금 / 적금 세후 수익 계산
- 카카오맵 기반 영업점 검색
- 상품 관련 질문이 가능한 AI 챗봇
- 관심 상품 등록 및 해제

|                       상품 상세                        |
| :----------------------------------------------------: |
| ![productDetail1](docs/screenshots/productDetail1.png) |

|                      상세 정보 1                       |                      상세 정보 2                       |                      상세 정보 3                       |
| :----------------------------------------------------: | :----------------------------------------------------: | :----------------------------------------------------: |
| ![productDetail2](docs/screenshots/productDetail2.png) | ![productDetail3](docs/screenshots/productDetail3.png) | ![productDetail4](docs/screenshots/productDetail4.png) |

<br />

### 👤 마이페이지

사용자가 가입한 상품과 관심 상품을 관리할 수 있는 개인화 페이지입니다.  
가입 상품의 달성률, 만기 일정, 금리 비교 차트를 제공해 사용자가 자신의 저축 현황을 한눈에 확인할 수 있도록 했습니다.

#### 주요 기능

- 가입 상품 등록 및 관리
- 상품별 납입 진행률 확인
- 만기 일정 확인
- 내 금리 / 기본금리 / 최고금리 / 한국은행 평균금리 비교
- 관심 상품 목록 확인
- 시청한 금융 영상 확인
- 작성한 커뮤니티 글 확인

|               마이페이지 1               |               마이페이지 2               |
| :--------------------------------------: | :--------------------------------------: |
|  ![myPage](docs/screenshots/myPage.png)  | ![myPage2](docs/screenshots/myPage2.png) |
| ![myPage3](docs/screenshots/myPage3.png) | ![myPage4](docs/screenshots/myPage4.png) |

<br />

### 📺 금융 라운지

금융 관련 콘텐츠를 한곳에서 확인할 수 있는 페이지입니다.  
금융 유튜브 영상, 커뮤니티 글, 금·은 시세 차트를 제공해 사용자가 금융 정보를 가볍게 탐색할 수 있도록 구성했습니다.

#### 주요 기능

- 금융 유튜브 영상 목록 제공
- 영상 상세 페이지 제공
- 커뮤니티 피드 제공
- 금·은 시세 차트 제공
- 금융 정보 탐색 공간 제공

|                  금융 영상                   |                   금·은 시세                   |
| :------------------------------------------: | :--------------------------------------------: |
| ![financeTV](docs/screenshots/financeTV.png) | ![goldSilver](docs/screenshots/goldSilver.png) |

<br />

### 💬 커뮤니티

사용자가 금융 정보나 궁금한 점을 공유할 수 있는 게시판 기능입니다.  
게시글 작성, 수정, 상세 조회, 댓글 기능을 통해 사용자 간 금융 관련 소통이 가능하도록 구성했습니다.

#### 주요 기능

- 게시글 목록 조회
- 게시글 작성 및 수정
- 게시글 상세 조회
- 댓글 작성
- 마이페이지에서 작성 글 확인

|                   커뮤니티                   |
| :------------------------------------------: |
| ![community](docs/screenshots/community.png) |

<br />

## 🧭 서비스 흐름

```txt
사용자 목표 입력
    ↓
예금 / 적금 선택
    ↓
기간, 금액, 우대조건 입력
    ↓
조건에 맞는 상품 필터링
    ↓
예상 수령액 계산
    ↓
추천 상품 리스트 제공
    ↓
상품 상세 정보 확인
    ↓
AI 요약 / 챗봇 / 영업점 검색
    ↓
관심 상품 또는 가입 상품 등록
    ↓
마이페이지에서 진행률과 만기 일정 관리
```

<br />

## 🛠️ 기술 스택

### Frontend

![Vue](https://img.shields.io/badge/Vue.js_3-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS_v4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Pinia](https://img.shields.io/badge/Pinia-FFD859?style=for-the-badge&logo=vue.js&logoColor=black)
![Vue Router](https://img.shields.io/badge/Vue_Router-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D)
![Axios](https://img.shields.io/badge/Axios-5A29E4?style=for-the-badge&logo=axios&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)

| 기술         | 사용 목적                           |
| ------------ | ----------------------------------- |
| Vue 3        | 컴포넌트 기반 UI 구현               |
| TypeScript   | 타입 기반 프론트엔드 개발           |
| Vite         | 빠른 개발 서버 및 빌드 환경 구성    |
| Tailwind CSS | 반응형 UI 및 스타일링               |
| Pinia        | 로그인, 사용자 정보, 상품 상태 관리 |
| Vue Router   | 페이지 라우팅 관리                  |
| Axios        | 백엔드 API 통신                     |
| Chart.js     | 금리 비교 및 시세 차트 시각화       |

<br />

### Backend

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django_5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST_Framework-ff1709?style=for-the-badge&logo=django&logoColor=white)
![JWT](https://img.shields.io/badge/Simple_JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Swagger](https://img.shields.io/badge/drf--spectacular-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)

| 기술                  | 사용 목적                         |
| --------------------- | --------------------------------- |
| Django                | 백엔드 서버 및 비즈니스 로직 구현 |
| Django REST Framework | REST API 설계 및 구현             |
| Simple JWT            | JWT 기반 인증 처리                |
| SQLite                | 프로젝트 데이터 저장              |
| drf-spectacular       | Swagger API 문서 자동화           |
| requests              | 외부 API 데이터 요청              |

<br />

### Infra & AI

![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)
![AWS EC2](https://img.shields.io/badge/AWS_EC2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white)
![Claude](https://img.shields.io/badge/Claude_API-CC785C?style=for-the-badge&logo=anthropic&logoColor=white)

| 기술           | 사용 목적                            |
| -------------- | ------------------------------------ |
| Vercel         | 프론트엔드 배포                      |
| AWS EC2        | 백엔드 서버 배포                     |
| Claude API     | 상품 설명, 약관 요약, 챗봇 응답 생성 |
| Kakao Map API  | 은행 영업점 검색                     |
| 금융감독원 API | 예·적금 상품 데이터 수집             |
| 한국은행 API   | 평균금리 및 금융 지표 데이터 활용    |

<br />

## 📁 프로젝트 구조

```txt
ourwish
├── frontend_dir
│   ├── public
│   ├── src
│   │   ├── assets
│   │   ├── components
│   │   ├── router
│   │   ├── stores
│   │   ├── views
│   │   └── main.ts
│   ├── package.json
│   ├── vite.config.ts
│   └── vercel.json
│
├── backend_dir
│   ├── apps
│   ├── config
│   ├── manage.py
│   └── requirements.txt
│
├── docs
│   └── screenshots
│
└── README.md
```

<br />

## 🧩 프론트엔드 컴포넌트 구조

```txt
App.vue
├── [레이아웃] Navbar.vue
│   └── EditProfileModal.vue
│       └── Chat.vue
│
├── [페이지] <RouterView>
│   ├── / → HomeView.vue
│   │   ├── LandingHero.vue
│   │   ├── LandingFeatures.vue
│   │   └── MobileLanding.vue
│   │
│   ├── /GoalSetup         → GoalSetupView.vue  (type: savings)
│   ├── /depositgoalsetup  → GoalSetupView.vue  (type: deposit)
│   │
│   ├── /recommendation        → RecommendationView.vue  (type: savings)
│   ├── /depositrecommendation → RecommendationView.vue  (type: deposit)
│   │   ├── ProductCard.vue
│   │   ├── BankFilterDropdown.vue
│   │   ├── FilterChips.vue
│   │   └── LevelInfoModal.vue
│   │
│   ├── /products/:id → SavingsDepositDetailView.vue
│   │   ├── ProductHeaderCard.vue
│   │   │   ├── DepositCalcModal.vue
│   │   │   └── SavingsCalcModal.vue
│   │   ├── ProductBasicInfo.vue
│   │   └── KakaoMap.vue
│   │       └── BranchMapModal.vue
│   │
│   ├── /mypage → MyPageView.vue
│   │   ├── SavingsCard.vue
│   │   ├── MarketRate.vue
│   │   ├── ProductsSection.vue
│   │   ├── WishlistSection.vue
│   │   ├── PostsSection.vue
│   │   ├── VideosSection.vue
│   │   └── EnrolledProductCard.vue
│   │       └── EnrollmentModal.vue
│   │
│   ├── /community/write    → CommunityWriteView.vue
│   ├── /community/:id/edit → CommunityWriteView.vue
│   ├── /community/:id      → CommunityPostDetailView.vue
│   │   └── CommentBody.vue
│   │
│   ├── /videos/:videoId → VideoDetailView.vue
│   │
│   └── /financelounge → FinanceLoungeView.vue
│       ├── VideoSection.vue
│       │   └── VideoCard.vue
│       ├── GoldSilverSection.vue
│       └── CommunitySection.vue
│
└── [오버레이] GlobalModals.vue
    ├── LoginModal.vue
    └── SignupModal.vue
```

<br />

## 🚀 실행 방법

### 1. Repository Clone

```bash
git clone https://github.com/Our-Wish/ourwish.git
cd ourwish
```

<br />

### 2. Frontend 실행

```bash
cd frontend_dir
npm install
npm run dev
```

<br />

### 3. Backend 실행

```bash
cd backend_dir
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Windows 환경에서는 아래 명령어로 가상환경을 활성화할 수 있습니다.

```bash
venv\Scripts\activate
```

<br />

### 4. 환경변수 설정

실행을 위해 프론트엔드와 백엔드에 필요한 환경변수를 설정해야 합니다.

#### Frontend `.env`

```env
VITE_API_BASE_URL=
VITE_KAKAO_MAP_KEY=
```

#### Backend `.env`

```env
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=
CORS_ALLOWED_ORIGINS=

FSS_API_KEY=
BANK_OF_KOREA_API_KEY=
CLAUDE_API_KEY=
```

> API Key와 Secret Key는 GitHub에 업로드하지 않습니다.

<br />

## 💡 금융 상품 추천 알고리즘 기술적 설명

> 작성: 김주우

<!--
이 섹션은 Backend / AI 담당자가 작성 예정입니다.

작성 예시 항목:
- 추천 알고리즘 개요
- 예금 / 적금 계산 방식 차이
- 사용자 입력값 처리 방식
- 금융 상품 필터링 기준
- 우대조건 매칭 방식
- 세후 예상 수령액 계산 방식
- 추천 결과 정렬 기준
- 외부 금융 데이터 수집 및 저장 흐름
-->

<br />

## 🤖 생성형 AI 활용 내용

> 작성: 김주우

<!--
이 섹션은 Backend / AI 담당자가 작성 예정입니다.

작성 예시 항목:
- 금융 상품 데이터 가공에 AI를 활용한 방식
- 우대조건 난이도 분류 방식
- 상품 설명 및 약관 쉬운말 요약 방식
- 상품 상세 AI 챗봇 응답 생성 방식
- 추천 로직 개선 과정에서 AI를 활용한 방식
- 코드 개선 및 프롬프트 개선 내용
-->

<br />

## 💬 프로젝트 후기 및 느낀 점

### 김주우

<!-- 작성 예정 -->

<br />

### 안서진

<!-- 작성 예정 -->

<br />
