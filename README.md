<!-- 배너 이미지 추가 예정 -->
![OurWish](docs/screenshots/banner.png)

## 🌟 목표만 알려주면 내게 맞는 적금, 한눈에 찾아드릴게요.

OurWish는 기간과 월 납입 금액을 입력하면 예상 수령액을 계산하고, 조건에 맞는 적금 상품을 추천해주는 AI 금융 서비스입니다.<br />
어려운 금리 조건과 약관도 AI가 사회 초년생 눈높이에 맞게 풀어 설명해주고,<br />
가입 후에는 진행률과 만기 일정을 한눈에 관리할 수 있어요! 💸

<br />

## ✨ 주요 기능

<br />

### 🏠 랜딩 페이지
목표만 입력하면 맞춤 금융상품을 바로 추천받을 수 있어요.

| |
|:--:|
| ![랜딩 페이지](docs/screenshots/landingPage.gif) |

<br />

### 💰 예/적금 상품 추천
기간·금액과 우대조건을 입력하면 세후 수령액 순으로 맞춤 상품을 추천해드려요.<br />
한국은행 평균금리 기준 예상 수령액을 즉시 계산하고, 적금 / 예금 트랙별로 질문이 달라요.

| 목표 설정 STEP 1 | 목표 설정 STEP 2 |
|:--:|:--:|
| ![goalSetUp](docs/screenshots/goalSetUp.png) | ![goalSetUp2](docs/screenshots/goalSetUp2.png) |

| 상품 추천 결과 |
|:--:|
| ![recommendation](docs/screenshots/recommendation.png) |

<br />

### 🔍 상품 상세
FSS 원문 정보, AI 쉬운말 소개, 세후 수익 계산, 카카오맵 영업점 검색, AI 챗봇까지 한 페이지에서 확인할 수 있어요.

| |
|:--:|
| ![productDetail1](docs/screenshots/productDetail1.png) |

| | | |
|:--:|:--:|:--:|
| ![productDetail2](docs/screenshots/productDetail2.png) | ![productDetail3](docs/screenshots/productDetail3.png) | ![productDetail4](docs/screenshots/productDetail4.png) |

<br />

### 👤 마이페이지
가입 상품의 달성 게이지, 금리 비교 차트(내 금리 vs 기본 vs 최고 vs 한국은행 평균), 찜 목록, 작성 글을 한곳에서 관리할 수 있어요.

| | |
|:--:|:--:|
| ![myPage](docs/screenshots/myPage.png) | ![myPage2](docs/screenshots/myPage2.png) |
| ![myPage3](docs/screenshots/myPage3.png) | ![myPage4](docs/screenshots/myPage4.png) |

<br />

### 📺 금융 라운지
커뮤니티 피드, 금융 유튜브 영상, 금·은 시세 차트를 한 화면에서 한눈에 볼 수 있어요.

| 금융 영상 | 금·은 시세 |
|:--:|:--:|
| ![financeTV](docs/screenshots/financeTV.png) | ![goldSilver](docs/screenshots/goldSilver.png) |

| 커뮤니티 |
|:--:|
| ![community](docs/screenshots/community.png) |

<br />

## 🛠️ 기술 스택

### Frontend

![Vue](https://img.shields.io/badge/Vue.js_3-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS_v4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Pinia](https://img.shields.io/badge/Pinia-FFD859?style=for-the-badge&logo=vue.js&logoColor=black)
![Vue Router](https://img.shields.io/badge/Vue_Router_v5-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D)
![Axios](https://img.shields.io/badge/Axios-5A29E4?style=for-the-badge&logo=axios&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)

### Backend

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django_5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST_Framework-ff1709?style=for-the-badge&logo=django&logoColor=white)
![JWT](https://img.shields.io/badge/Simple_JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Swagger](https://img.shields.io/badge/drf--spectacular-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)

### Infra & AI

![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)
![AWS EC2](https://img.shields.io/badge/AWS_EC2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white)
![Claude](https://img.shields.io/badge/Claude_API-CC785C?style=for-the-badge&logo=anthropic&logoColor=white)

<br />

## 💡 금융 상품 추천 알고리즘

> 작성: 김주우

<!-- 주우가 작성 예정 -->

### 추천 방식 개요

...

### 핵심 로직 및 데이터 처리 흐름

```
사용자 입력 (목표 금액, 기간, 월 납입액)
    ↓
예상 수령액 계산 (단리/복리 공식 적용)
    ↓
조건 필터링 (은행, 금리 유형, 가입 기간)
    ↓
정렬 및 상위 N개 추천
```

<br />

## 🤖 생성형 AI 활용

> 작성: 김주우

<!-- 주우가 작성 예정 -->

### 데이터 생성에 AI 활용

...

### 추천 로직에 AI 활용

...

### 코드 개선에 AI 활용

...

<br />

## 💬 프로젝트 후기 및 느낀 점

### 김주우

> ...

### 안서진

> ...

<br />

## 🧑🏻‍💻 팀원

<table>
  <tbody>
    <tr>
      <td align="center">
        <a href="https://github.com/kimzoo5676-del">
          <img alt="kimzoo5676-del" src="https://avatars.githubusercontent.com/kimzoo5676-del" width="160" />
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/xxj15">
          <img alt="xxj15" src="https://avatars.githubusercontent.com/u/63233128?v=4" width="160" />
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
