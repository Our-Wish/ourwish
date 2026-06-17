"""GMS(OpenAI 호환) LLM 직접 호출 모듈. sync_products 배치에서만 사용."""
import json
import logging
import re

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

_TIMEOUT = 30  # 초

DIFFICULTY_GUIDE = """난이도(difficulty) 분류 기준:
- LOW (그냥 하면 됨): 급여이체, 자사 앱 가입/로그인, 자사 체크/신용카드 발급,
  자동이체 1건 이상, 인터넷/모바일뱅킹, 신규 고객, 마케팅 동의, 전자통장,
  자사 입출금통장 보유.
- MID (좀 챙겨야 함): 카드 실적 월 N만원 이상, 주택청약 보유, 공과금 자동이체 N건 이상,
  펀드/ISA, 연금저축, 타행→자행 급여이체 변경, 적금/예금 N개 이상 동시 보유,
  패밀리뱅킹, 비대면 가입.
- HIGH (사회초년생에게 쉽지 않음): 신용카드 연 500만원 이상, 외환 거래, 대출 보유,
  자산관리 N억 이상, VIP, IRP, 주담대 연계, 증권 연계, 카드론/리볼빙,
  골프장/제휴, 탄소중립 인증, 지역화폐.
판단이 애매하면 더 어려운 쪽으로 분류한다."""

_LABEL_DEVELOPER = f"""너는 은행 적금의 우대금리 조건을 사회초년생이 쉽게 이해할 수 있도록
한 줄로 요약하고, 충족 난이도를 분류하는 도우미야.

규칙:
- friendly_label: 40자 이내, 해요체(~해요/~돼요), 금융 용어 풀어쓰기
- 반드시 JSON 객체 하나만 출력

{DIFFICULTY_GUIDE}

퓨샷 예시:
입력: "당행 급여이체"
출력: {{"friendly_label": "이 은행으로 월급을 받으면 돼요", "difficulty": "LOW"}}

입력: "카드 월 실적 30만원 이상"
출력: {{"friendly_label": "카드를 한 달에 30만원 이상 써야 해요", "difficulty": "MID"}}

입력: "주택담보대출 연계"
출력: {{"friendly_label": "주택담보대출이 있어야 해요", "difficulty": "HIGH"}}"""

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
