"""GMS(OpenAI 호환) LLM 직접 호출 모듈. sync_products 배치에서만 사용.

(예외: AI 챗봇은 유저 요청 시 실시간 호출 — 별도 모듈/뷰에서 다룬다.)
"""
import json
import logging
import re

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

_TIMEOUT = 60  # 초 (gpt-5-mini 추론 응답이 가끔 느려 여유를 둠)


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
                # temperature는 보내지 않는다 — gpt-5 계열은 기본값(1)만 허용,
                # 0 등 커스텀 값을 보내면 400을 반환한다.
                "model": settings.GMS_MODEL,
                # 추론량을 낮춰 응답 속도·비용을 줄인다(단순 분류/요약 작업이라 low로 충분).
                "reasoning_effort": "low",
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
    except requests.HTTPError as exc:
        # 400 등은 응답 본문에 원인이 들어있으므로 같이 로깅(디버깅용).
        body = exc.response.text[:300] if exc.response is not None else ""
        logger.warning("GMS 호출 실패: %s | %s", exc, body)
        return None
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


# ── 1) 매칭 태그 + 연령 제한 분류 ──────────────────────────────
_TAGS_DEVELOPER = """
너는 적금 상품의 우대조건 원문과 가입 대상을 읽고,
정해진 4가지 우대조건 태그 해당 여부와 가입 연령 제한을 뽑아내는 분류기야.

태그 4개 — 이 상품이 그 우대조건을 "제공하면" true, 아니면 false:
- salary_transfer (급여이체): 이 은행 계좌로 급여/연금을 이체하면 우대받는 조건.
- auto_transfer (자동이체): 적금 자동이체, 공과금 자동이체 등 자동이체 관련 우대.
- card_usage (카드실적): 이 은행 신용/체크카드 사용실적이 있으면 우대.
- housing_subscription (청약): 주택청약종합저축 보유(또는 미보유) 관련 우대.

연령 제한 — 가입 대상에 나이 제한이 있으면 만 나이로 추출:
- 예: "만 19세~34세" → age_min=19, age_max=34
- 예: "만 65세 이상" → age_min=65, age_max=null
- 예: "만 19세 이상" → age_min=19, age_max=null
- 나이 제한이 없으면 age_min, age_max 모두 null.

규칙:
- 원문에 근거가 있을 때만 태그를 true로 한다. 추측·과잉판단 금지.
- "사원증/사원카드" 같은 증빙 서류는 카드실적이 아니다(false).
- 반드시 JSON 객체 하나만 출력. 마크다운·설명 금지.
- 키: salary_transfer, auto_transfer, card_usage, housing_subscription, age_min, age_max.

퓨샷 예시:
입력:
가입 대상: 만 19세 이상 만 34세 이하 실명의 개인
우대조건: -당행 급여이체 실적 보유: 0.3%p / -자동이체 6회 이상: 0.2%p

출력:
{"salary_transfer": true, "auto_transfer": true, "card_usage": false, "housing_subscription": false, "age_min": 19, "age_max": 34}

입력:
가입 대상: 실명의 개인
우대조건: -당행 주택청약종합저축 보유: 0.2%p / -당행 신용카드 월 30만원 이상 이용: 0.3%p

출력:
{"salary_transfer": false, "auto_transfer": false, "card_usage": true, "housing_subscription": true, "age_min": null, "age_max": null}
"""

_TAG_KEYS = (
    "salary_transfer",
    "auto_transfer",
    "card_usage",
    "housing_subscription",
)


def _to_age(value):
    """LLM이 준 나이 값을 int 또는 None으로 정규화."""
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def generate_tags(product):
    """상품 → {4개 태그 bool, age_min, age_max}. 실패 시 빈 dict.

    우대조건 원문(special_condition_raw)으로 태그를, 가입 대상(join_member)으로
    연령 제한을 뽑는다. 한 번의 GMS 호출로 처리한다.
    """
    user = (
        f"가입 대상: {product.join_member or '정보 없음'}\n"
        f"우대조건:\n{product.special_condition_raw or '없음'}\n\n"
        '출력: {"salary_transfer": ..., "auto_transfer": ..., '
        '"card_usage": ..., "housing_subscription": ..., '
        '"age_min": ..., "age_max": ...}'
    )
    data = _parse_json(_chat(_TAGS_DEVELOPER, user))
    if not data:
        return {}
    result = {key: bool(data.get(key)) for key in _TAG_KEYS}
    result["age_min"] = _to_age(data.get("age_min"))
    result["age_max"] = _to_age(data.get("age_max"))
    return result


# ── 2) AI 한줄 요약("이런 분께 좋아요") ────────────────────────
_AI_SUMMARY_DEVELOPER = """
너는 적금 상품을 한 줄로 요약해, 어떤 사람에게 잘 맞는 상품인지 알려주는 도우미야.

상품의 가입대상·가입방법·납입한도·만기이자·유의사항·우대조건을 종합해서,
"이 상품은 이런 특징이라 이런 분께 좋아요" 형태의 한 문장을 만들어.

작성 규칙:
- 한 문장, 80자 이내, 해요체.
- 상품의 실제 특징(대상·우대조건 등)과 어울리는 사용자 유형을 알려줘.
- 광고처럼 과장하지 말고, 원문에 없는 내용은 지어내지 마.
- 반드시 JSON 객체 하나만 출력. 마크다운·설명 금지. 키: ai_summary.

퓨샷 예시:
입력:
상품명: 청년도약적금 (행복은행)
가입 대상: 만 19~34세 청년
우대조건: 급여이체, 자동이체 시 우대

출력:
{"ai_summary": "급여이체·자동이체를 꾸준히 할 수 있는 청년이 우대금리를 챙기기 좋은 적금이에요."}
"""


def generate_ai_summary(product):
    """상품 → AI 한줄 요약 문자열. 실패 시 None."""
    user = (
        f"상품명: {product.product_name} ({product.bank.bank_name})\n"
        f"가입 대상: {product.join_member or '정보 없음'}\n"
        f"가입 방법: {product.join_way or '정보 없음'}\n"
        f"납입 한도: {product.max_limit or '정보 없음'}\n"
        f"만기 후 이자: {product.maturity_interest or '정보 없음'}\n"
        f"기타 유의사항: {product.etc_note or '정보 없음'}\n"
        f"우대조건:\n{product.special_condition_raw or '없음'}\n\n"
        '출력: {"ai_summary": "..."}'
    )
    data = _parse_json(_chat(_AI_SUMMARY_DEVELOPER, user))
    if not data:
        return None
    return (data.get("ai_summary") or "").strip() or None
