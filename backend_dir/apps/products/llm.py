"""GMS(OpenAI 호환) LLM 직접 호출 모듈. sync_products 배치에서만 사용."""
import json
import logging
import re

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

_TIMEOUT = 30  # 초

DIFFICULTY_GUIDE = """
난이도(difficulty) 분류 기준:

difficulty는 우대금리 조건을 사용자가 실제로 달성하기 쉬운 정도를 의미한다.
금리 혜택의 크기가 아니라, 조건을 맞추기 위해 필요한 행동, 반복 관리, 생활 패턴 변경, 기존 금융거래 여부를 기준으로 판단한다.

LOW — 가볍게 챙길 수 있는 조건.
앱 가입, 자동이체 등록처럼 대부분의 사용자가 어렵지 않게 완료할 수 있는 조건이다.
한 번 설정하거나 가입 과정에서 자연스럽게 충족되는 조건은 LOW로 분류한다.

예:
앱 가입/로그인, 자동이체 등록, 신규 고객, 마케팅 동의, 전자통장 발급,
입출금 통장 보유, 인터넷/모바일뱅킹 가입.

MID — 조금 신경 쓰면 가능한 조건.
급여이체나 카드 사용처럼 사용자의 생활 패턴에 따라 달성 여부가 달라지는 조건이다.
매월 반복 관리가 필요하거나, 특정 계좌/상품을 꾸준히 유지해야 하는 조건은 MID로 분류한다.

예:
급여이체, 카드 실적, 공과금 자동이체, 주택청약 보유, 비대면 가입,
가족 계좌 연결, 적금/예금 동시 보유.

HIGH — 조건 확인이 필요한 조건.
기존 자산, 거래 실적, 대출, 투자/퇴직연금 상품, 프리미엄 등급처럼
사용자가 단기간에 맞추기 어렵거나 부담이 큰 조건은 HIGH로 분류한다.

예:
높은 카드 사용 실적, 외환 거래 실적, 대출 보유, 자산관리 계좌 보유,
프리미엄/VIP 등급, 퇴직연금 가입, 주택담보대출 연계, 증권 연계 계좌.

판단 규칙:
- 하나의 우대조건에 여러 요구사항이 있으면 가장 어려운 요구사항을 기준으로 분류한다.
- 한 번 설정하면 끝나는 조건은 LOW로 본다.
- 매월 반복해서 관리해야 하는 조건은 최소 MID로 본다.
- 급여이체, 카드 실적, 공과금 자동이체처럼 생활 패턴에 영향을 받는 조건은 MID로 본다.
- 대출, 고액 자산, VIP 등급, 외환/증권/퇴직연금처럼 기존 금융거래나 큰 부담이 필요한 조건은 HIGH로 본다.
- 금액, 횟수, 기간 조건이 클수록 더 어렵게 본다.
- 목록에 없는 조건은 위 기준에 따라 분류한다.
- 애매하면 더 어려운 쪽으로 분류한다.
"""

_LABEL_DEVELOPER = f"""
너는 적금 우대금리 조건을 쉽게 풀어쓰는 도우미야.

이제 막 돈을 모으기 시작한 사용자도 이해할 수 있도록,
은행 약관처럼 딱딱하거나 어려운 표현을 쉬운 말로 바꿔줘.

해야 할 일:
1. 우대금리 조건 원문을 읽어.
2. 사용자가 실제로 무엇을 하면 되는지 한 문장으로 설명해.
3. 조건을 충족하기 쉬운 정도를 LOW, MID, HIGH 중 하나로 분류해.

friendly_label 작성 규칙:
- 40자 이내로 작성해.
- 해요체로 작성해. 예: ~하면 돼요, ~해야 해요
- 금융 용어는 가능한 쉽게 풀어써.
- 원문에 있는 금액, 횟수, 기간, 대상 조건은 빠뜨리지 마.
- 원문에 없는 조건이나 혜택은 추가하지 마.
- 너무 광고 문구처럼 쓰지 말고, 서비스 화면에 넣기 좋은 문장으로 써.

difficulty 작성 규칙:
- 반드시 LOW, MID, HIGH 중 하나만 사용해.
- 조건을 맞추기 위한 노력, 반복 관리, 금액 부담, 기존 금융거래 여부를 기준으로 판단해.

{DIFFICULTY_GUIDE}

출력 규칙:
- 반드시 JSON 객체 하나만 출력해.
- 마크다운, 코드블록, 추가 설명은 출력하지 마.
- 키는 friendly_label, difficulty 두 개만 사용해.

퓨샷 예시:
입력: "당행 급여이체"
출력: {{"friendly_label": "이 은행으로 월급을 받으면 돼요", "difficulty": "MID"}}

입력: "카드 월 실적 30만원 이상"
출력: {{"friendly_label": "카드를 한 달에 30만원 이상 써야 해요", "difficulty": "MID"}}

입력: "주택담보대출 연계"
출력: {{"friendly_label": "주택담보대출이 있어야 해요", "difficulty": "HIGH"}}

입력: "마케팅 수신 동의"
출력: {{"friendly_label": "혜택 안내 알림에 동의하면 돼요", "difficulty": "LOW"}}

입력: "자동이체 등록"
출력: {{"friendly_label": "자동이체를 등록하면 돼요", "difficulty": "LOW"}}
"""


_CORE_INFO_DEVELOPER = """너는 적금 상품 안내문을 사회초년생이 한눈에 이해할 수 있게 요약하는 도우미야.

규칙:
- 각 항목은 1문장(50자 이내), 해요체(~해요/~돼요)
- 해당 정보가 없으면 null 반환
- 반드시 JSON 객체 하나만 출력"""


def _chat(developer_prompt, user_prompt):
    """GMS chat/completions 호출 → 응답 본문 문자열. 실패 시 None."""
    if not settings.GMS_API_KEY:
        logger.warning("GMS_API_KEY 미설정 — LLM 호출 건너뜀")
        return None
    try:
        res = requests.post(
            settings.GMS_API_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {settings.GMS_API_KEY}",
            },
            json={
                "model": settings.GMS_MODEL,
                "temperature": 0,
                "messages": [
                    {"role": "developer", "content": developer_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "response_format": {"type": "json_object"},
            },
            timeout=_TIMEOUT,
        )
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except (requests.RequestException, KeyError, ValueError) as exc:
        logger.warning("GMS 호출 실패: %s", exc)
        return None


def _parse_json(content):
    """응답 문자열에서 JSON 객체 파싱. 코드펜스/잡텍스트 섞이면 {...}만 추출."""
    if not content:
        return None
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if not match:
            return None
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None


def generate_friendly_label(label):
    """우대조건 원문 → (friendly_label, difficulty). 실패 항목은 None."""
    user = (
        f'조건 원문: "{label}"\n'
        f'출력: {{"friendly_label": "...", "difficulty": "LOW|MID|HIGH"}}'
    )
    data = _parse_json(_chat(_LABEL_DEVELOPER, user))
    if not data:
        return None, None

    friendly = (data.get("friendly_label") or "").strip()[:500] or None
    difficulty = (data.get("difficulty") or "").strip().upper()
    if difficulty not in {"LOW", "MID", "HIGH"}:
        difficulty = None
    return friendly, difficulty


def generate_core_info(product):
    """상품 → {join_summary, maturity_summary, etc_summary}. 실패 시 빈 dict."""
    user = (
        f"상품명: {product.product_name} ({product.bank.bank_name})\n"
        f"다음 정보를 각각 1문장으로 요약해줘.\n"
        f"- 가입 방법/대상: {product.join_way or '정보 없음'} / {product.join_member or '정보 없음'}\n"
        f"- 만기 후 이자: {product.maturity_interest or '정보 없음'}\n"
        f"- 기타 유의사항: {product.etc_note or '정보 없음'}\n\n"
        f'출력: {{"join_summary": "...", "maturity_summary": "...", "etc_summary": "..."}}'
    )
    data = _parse_json(_chat(_CORE_INFO_DEVELOPER, user))
    if not data:
        return {}
    return {
        "join_summary": (data.get("join_summary") or "").strip() or None,
        "maturity_summary": (data.get("maturity_summary") or "").strip() or None,
        "etc_summary": (data.get("etc_summary") or "").strip() or None,
    }
