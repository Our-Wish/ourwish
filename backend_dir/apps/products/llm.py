"""GMS(OpenAI 호환) LLM 직접 호출 모듈. sync_products 배치에서만 사용."""
import json
import logging
import re

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

_TIMEOUT = 30  # 초

# 우대조건 난이도 분류 기준. 프롬프트에 그대로 주입한다.
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
    developer = (
        "너는 은행 적금의 우대금리 조건을 사회초년생이 한눈에 이해하도록 다듬고, "
        "그 조건을 충족하기 얼마나 쉬운지 난이도를 분류하는 도우미야. "
        "반드시 JSON 객체 하나만 출력해.\n\n" + DIFFICULTY_GUIDE
    )
    user = (
        f'다음 적금 우대조건을 분석해줘.\n조건 원문: "{label}"\n\n'
        "출력 형식(JSON):\n"
        '{"friendly_label": "조건을 한 문장으로 쉽게 풀어쓴 설명", '
        '"difficulty": "LOW 또는 MID 또는 HIGH"}'
    )
    data = _parse_json(_chat(developer, user))
    if not data:
        return None, None

    friendly = (data.get("friendly_label") or "").strip()[:500] or None
    difficulty = (data.get("difficulty") or "").strip().upper()
    if difficulty not in {"LOW", "MID", "HIGH"}:
        difficulty = None
    return friendly, difficulty


def generate_core_info(product):
    """상품 → {join_summary, maturity_summary, etc_summary}. 실패 시 빈 dict."""
    developer = (
        "너는 적금 상품의 안내문을 사회초년생이 한눈에 알 수 있게 짧게 요약하는 도우미야. "
        "각 항목은 1~2문장으로, 군더더기 없이 핵심만. 반드시 JSON 객체 하나만 출력해."
    )
    user = (
        "다음 적금 상품 정보를 요약해줘.\n"
        f"- 가입 방법: {product.join_way or '정보 없음'}\n"
        f"- 가입 대상: {product.join_member or '정보 없음'}\n"
        f"- 만기 후 이자: {product.maturity_interest or '정보 없음'}\n"
        f"- 기타 유의사항: {product.etc_note or '정보 없음'}\n\n"
        "출력 형식(JSON):\n"
        '{"join_summary": "가입 방법·대상 요약", '
        '"maturity_summary": "만기/이자 관련 요약", '
        '"etc_summary": "기타 유의사항 요약"}'
    )
    data = _parse_json(_chat(developer, user))
    if not data:
        return {}
    return {
        "join_summary": (data.get("join_summary") or "").strip() or None,
        "maturity_summary": (data.get("maturity_summary") or "").strip() or None,
        "etc_summary": (data.get("etc_summary") or "").strip() or None,
    }
