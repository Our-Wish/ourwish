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
너는 {PRODUCT_LABEL} 상품의 우대조건 원문과 가입 대상을 읽고,
정해진 8가지 우대조건 태그 해당 여부, 가입 연령 제한, 최소 가입금액을 뽑아내는 분류기야.

태그 8개 — 이 상품이 그 우대조건을 "제공하면" true, 아니면 false:
- salary_transfer (급여이체): 이 은행 계좌로 급여/연금을 이체하면 우대받는 조건.
- auto_transfer (자동이체): 적금 자동이체, 공과금 자동이체 등 자동이체 관련 우대.
- card_usage (카드실적): 이 은행 신용/체크카드 사용실적이 있으면 우대.
- housing_subscription (청약): 주택청약종합저축 보유(또는 미보유) 관련 우대.
- first_transaction (첫거래): 이 은행과 처음 거래(신규 고객)하면 우대.
- online_signup (비대면가입): 인터넷뱅킹/모바일앱 등 비대면(영업점 미방문)으로 가입하면 우대.
- marketing_consent (마케팅동의): 마케팅·광고·알림(혜택알림) 수신 동의 시 우대.
- redeposit (재예치): 만기 후 재예치/재가입(다시 맡김) 시 우대.

연령 제한 — 가입 대상에 나이 제한이 있으면 만 나이로 추출:
- 예: "만 19세~34세" → age_min=19, age_max=34
- 예: "만 65세 이상" → age_min=65, age_max=null
- 예: "만 19세 이상" → age_min=19, age_max=null
- 나이 제한이 없으면 age_min, age_max 모두 null.

최소 가입금액(min_limit) — 가입 시 최소로 넣어야 하는 금액을 '원' 단위 정수로 추출:
- 적금이면 매월 최소 납입액, 예금이면 최소 예치금액 기준.
- 예: "월 10만원 이상" → min_limit=100000
- 예: "최소 가입금액 100만원" → min_limit=1000000
- 금액 명시가 없으면 min_limit=null.

규칙:
- 원문에 근거가 있을 때만 태그를 true로 하고, 금액도 명시가 있을 때만 추출한다. 추측·과잉판단 금지.
- "사원증/사원카드" 같은 증빙 서류는 카드실적이 아니다(false).
- 반드시 JSON 객체 하나만 출력. 마크다운·설명 금지.
- 키: salary_transfer, auto_transfer, card_usage, housing_subscription, first_transaction, online_signup, marketing_consent, redeposit, age_min, age_max, min_limit.

퓨샷 예시:
입력:
가입 대상: 만 19세 이상 만 34세 이하 실명의 개인
우대조건: -당행 급여이체 실적 보유: 0.3%p / -자동이체 6회 이상: 0.2%p
기타 유의사항: 월 10만원 이상 납입

출력:
{"salary_transfer": true, "auto_transfer": true, "card_usage": false, "housing_subscription": false, "first_transaction": false, "online_signup": false, "marketing_consent": false, "redeposit": false, "age_min": 19, "age_max": 34, "min_limit": 100000}

입력:
가입 대상: 실명의 개인
우대조건: -비대면(인터넷뱅킹) 가입: 0.1%p / -마케팅 정보 수신 동의: 0.1%p / -만기 후 재예치 고객: 0.1%p
기타 유의사항: 최소 가입금액 100만원

출력:
{"salary_transfer": false, "auto_transfer": false, "card_usage": false, "housing_subscription": false, "first_transaction": false, "online_signup": true, "marketing_consent": true, "redeposit": true, "age_min": null, "age_max": null, "min_limit": 1000000}
"""

_TAG_KEYS = (
    "salary_transfer",
    "auto_transfer",
    "card_usage",
    "housing_subscription",
    "first_transaction",
    "online_signup",
    "marketing_consent",
    "redeposit",
)


def _to_int(value):
    """LLM이 준 숫자 값(나이·금액 등)을 int 또는 None으로 정규화."""
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def generate_tags(product):
    """상품 → {6개 태그 bool, age_min, age_max, min_limit}. 실패 시 빈 dict.

    우대조건 원문(special_condition_raw)·기타 유의사항(etc_note)으로 태그·최소금액을,
    가입 대상(join_member)으로 연령 제한을 뽑는다. 한 번의 GMS 호출로 처리한다.
    """
    developer = _TAGS_DEVELOPER.replace(
        "{PRODUCT_LABEL}", product.get_product_type_display()
    )
    user = (
        f"가입 대상: {product.join_member or '정보 없음'}\n"
        f"우대조건:\n{product.special_condition_raw or '없음'}\n"
        f"기타 유의사항:\n{product.etc_note or '없음'}\n\n"
        '출력: {"salary_transfer": ..., "auto_transfer": ..., '
        '"card_usage": ..., "housing_subscription": ..., '
        '"first_transaction": ..., "online_signup": ..., '
        '"marketing_consent": ..., "redeposit": ..., '
        '"age_min": ..., "age_max": ..., "min_limit": ...}'
    )
    data = _parse_json(_chat(developer, user))
    if not data:
        return {}
    result = {key: bool(data.get(key)) for key in _TAG_KEYS}
    result["age_min"] = _to_int(data.get("age_min"))
    result["age_max"] = _to_int(data.get("age_max"))
    result["min_limit"] = _to_int(data.get("min_limit"))
    return result


# ── 2) AI 쉬운말 소개(친절한 핵심 + 어려운 용어 1개 풀이) ──
# 서비스 목적: 금융 용어를 잘 모르는 사회초년생도 상품을 이해하게 돕는 것.
# 그래서 AI는 "추천 카피"가 아니라 "어려운 상품 설명을 친절하게 풀어주는 통역기".
# 사회초년생이 '진짜로' 막히는 전문용어(평잔·고시금리 등)만 골라 풀어준다(없으면 비움).
# LLM에는 {용어, 뜻}만 받고, "'OOO'는 ~라는 뜻이에요!" 친절한 문장은 파이썬이
# 조립한다. 조사(은/는·라는/이라는)도 받침을 보고 직접 붙여 맞춤법 오류를 없앤다.
_AI_SUMMARY_DEVELOPER = """
너는 금융을 처음 접하는 사회초년생에게 {PRODUCT_LABEL} 상품을 쉽게 설명해주는 OURWISH AI 도우미야.

상품의 가입대상·가입방법·납입한도·만기이자·유의사항·우대조건을 읽고
summary와 terms를 만들어.

목표:
- 사용자가 상품설명서를 다 읽지 않아도
  "이 {PRODUCT_LABEL}이 어떤 사람에게 유리한지" 바로 이해하게 만든다.
- 단순히 우대조건을 나열하지 말고,
  어떤 생활 패턴을 가진 사람에게 맞는 상품인지 쉽게 말한다.

출력 형식:
반드시 JSON 객체 하나만 출력한다.
키는 summary, terms만 사용한다.
마크다운, 설명, 코드블럭은 절대 쓰지 않는다.

summary 규칙:
- 1문장, 80자 이내, 반드시 '~요!'로 끝낸다.
- 사회초년생이 딱 보고 이해할 수 있게 친절하게 쓴다.
- 우대조건이 있으면 대표 조건 2~3개만 골라 말한다.
- 조건을 나열하기보다 "어떤 사람에게 유리한 {PRODUCT_LABEL}인지"가 느껴지게 쓴다.
- 급여이체, 공과금 자동이체, 카드사용, 오픈뱅킹, 주택청약, 비대면가입, 첫거래(신규), 마케팅 동의, 만기 후 재예치 등 실제 조건명을 사용한다.
- %p, 금액, 기간 같은 숫자는 쓰지 않는다.
- "조건을 채우면 이자를 더 받아요"처럼 뻔한 표현은 금지한다.
- 과장 광고처럼 보이는 표현은 쓰지 않는다.
- 문장 안에 "누구에게 맞는지"가 드러나야 한다.
- 가능하면 "주거래로 쓰는 사람", "비대면으로 가입하려는 사람", "카드실적을 챙길 사람"처럼 생활 상황 중심으로 말한다.
- 적립식(적금)이면 "목돈을 모으려는 사람", 거치식(예금)이면 "목돈을 굴리려는·맡기려는 사람"처럼 상품 성격에 맞게 표현한다.
- "우대받기 좋은", "챙기기 좋은"만 반복하지 말고 상품마다 다른 표현을 쓴다.

좋은 summary 예:
- "우리은행을 주거래로 쓰고 월급·공과금·카드결제까지 관리하는 사람에게 잘 맞는 {PRODUCT_LABEL}이에요!"
- "스마트폰으로 간편하게 가입하고, 오픈뱅킹을 함께 쓰면 우대받기 좋은 {PRODUCT_LABEL}이에요!"
- "카드 사용과 개인정보 동의, 외화적금 가입까지 함께 할 사람에게 유리한 {PRODUCT_LABEL}이에요!"
- "비대면으로 가입하고 다른 은행 계좌를 오픈뱅킹에 연결하면 챙기기 좋은 {PRODUCT_LABEL}이에요!"

나쁜 summary 예:
- "조건을 충족하면 우대받는 {PRODUCT_LABEL}이에요!"
- "금리가 좋은 {PRODUCT_LABEL}이에요!"
- "여러 조건을 만족하면 이자를 더 받을 수 있어요!"
- "월급·연금 이체하거나 공과금 자동이체나 우리카드 결제하면 우대받는 {PRODUCT_LABEL}이에요!"

terms 규칙:
- terms는 진짜 어려운 금융용어 2개까지만 고른다.
- 어려운 용어가 없으면 빈 배열 []로 둔다.
- 우대금리, 만기, 가입, 통장, 카드실적, 자동이체, 급여이체는 설명하지 않는다.
- 가능한 용어 예: 평잔, 고시금리, 고시이율, 약정이율, 단리, 복리, 자유적립식, 정액적립식, 비과세
- meaning은 30자 안팎의 쉬운 명사구로 쓴다.
- meaning에는 따옴표, 마침표, 조사 설명, 메타표현을 넣지 않는다.

예시 1:
입력:
상품명: 우리SUPER주거래적금
우대조건: 급여/연금 이체, 공과금 자동이체, 우리카드 결제, 마케팅 동의
만기 후 이자: 만기시점 약정이율 기준

출력:
{"summary":"우리은행을 주거래로 쓰고 월급·공과금·카드결제까지 관리하는 사람에게 잘 맞는 {PRODUCT_LABEL}이에요!","terms":[{"term":"약정이율","meaning":"가입할 때 정해진 적용 이자율"}]}

예시 2:
입력:
상품명: WON적금
우대조건: 우리꿈통장 또는 WON통장 연결, 오픈뱅킹 타행계좌 등록
가입방법: 스마트폰, 전화

출력:
{"summary":"스마트폰으로 가입하고 우리은행 통장과 오픈뱅킹을 함께 쓰면 챙기기 좋은 {PRODUCT_LABEL}이에요!","terms":[]}

예시 3:
입력:
상품명: iM함께적금
우대조건: 평잔 유지, 주택청약 보유, 함께예금 동시 가입, 오픈뱅킹 타행계좌 등록, 인터넷/모바일뱅킹 가입

출력:
{"summary":"주택청약이나 오픈뱅킹을 이미 쓰고 있다면 우대조건을 챙기기 쉬운 {PRODUCT_LABEL}이에요!","terms":[{"term":"평잔","meaning":"일정 기간 통장에 있던 평균 잔액"}]}

예시 4:
입력:
상품명: 여행스케치적금
우대조건: 외화적금 동일자 가입, 카드사용실적, 개인정보 동의

출력:
{"summary":"여행자금처럼 목돈을 모으면서 외화적금과 카드사용도 함께 챙길 사람에게 어울리는 {PRODUCT_LABEL}이에요!","terms":[{"term":"고시금리","meaning":"은행이 정해 공시한 기준 이자율"}]}

예시 5:
입력:
상품명: 비대면 정기예금
우대조건: 첫거래(신규) 고객, 비대면(인터넷/모바일) 가입, 만기 후 재예치

출력:
{"summary":"비대면으로 간편하게 가입하고 목돈을 안정적으로 굴리려는 첫거래 고객에게 잘 맞는 {PRODUCT_LABEL}이에요!","terms":[]}
"""


def _josa(word, with_batchim, without_batchim):
    """word 마지막 글자의 받침 유무로 조사를 고른다(한글 아니면 받침 없는 형태)."""
    if not word:
        return without_batchim
    code = ord(word[-1])
    if 0xAC00 <= code <= 0xD7A3:  # 한글 음절 영역
        return with_batchim if (code - 0xAC00) % 28 else without_batchim
    return without_batchim


def _render_summary(summary, terms):
    """{summary, terms} → 저장용 문자열. 핵심 한 줄 + 친절한 용어 풀이 줄들.

    "'우대금리'는 ~라는 뜻이에요!"처럼 조립하되, 조사는 받침으로 직접 골라
    맞춤법 오류(예: '평잔란')를 원천 차단한다.
    """
    lines = [summary]
    for item in terms:
        term = (item.get("term") or "").strip()
        meaning = (item.get("meaning") or "").strip()
        if not (term and meaning):
            continue
        eun_neun = _josa(term, "은", "는")
        raneun = _josa(meaning, "이라는", "라는")
        lines.append(f"'{term}'{eun_neun} {meaning}{raneun} 뜻이에요!")
    return "\n".join(lines)


def generate_ai_summary(product):
    """상품 → AI 쉬운말 소개 문자열(친절한 핵심 + 용어 풀이 줄들). 실패 시 None."""
    developer = _AI_SUMMARY_DEVELOPER.replace(
        "{PRODUCT_LABEL}", product.get_product_type_display()
    )
    user = (
        f"상품명: {product.product_name} ({product.bank.bank_name})\n"
        f"가입 대상: {product.join_member or '정보 없음'}\n"
        f"가입 방법: {product.join_way or '정보 없음'}\n"
        f"납입 한도: {product.max_limit or '정보 없음'}\n"
        f"만기 후 이자: {product.maturity_interest or '정보 없음'}\n"
        f"기타 유의사항: {product.etc_note or '정보 없음'}\n"
        f"우대조건:\n{product.special_condition_raw or '없음'}\n\n"
        '출력: {"summary": "(쉽고 친절한 핵심 한 줄)", '
        '"terms": [{"term": "용어", "meaning": "쉬운 뜻"}, ...]}'
    )
    data = _parse_json(_chat(developer, user))
    if not data:
        return None
    summary = (data.get("summary") or "").strip()
    if not summary:
        return None
    terms = data.get("terms")
    if not isinstance(terms, list):
        terms = []
    return _render_summary(summary, terms[:2])  # 어려운 용어는 최대 두개까지


# ── 3) AI 챗봇 (상품 상세 실시간 Q&A, 스트리밍) ────────────────
# 다른 LLM 기능과 달리 "유저 요청 시 실시간" 호출하는 유일한 예외.
# 대화는 프론트가 보관하고 매 요청에 통째로 보내므로, 백엔드는
# (1) 최근 N턴만 자르고 (2) 그 상품 데이터를 developer 메시지로 주입해 GMS에 넘긴다.
# 답변은 조각조각(스트리밍) 흘려보낸다. (stateless: 저장 안 함)
_CHAT_TURNS = 5  # 최근 N턴(질문1+답1=1턴)만 GMS에 보냄 → 토큰·비용 가드
_CHAT_ROLES = {"user", "assistant"}  # 프론트가 보낼 수 있는 역할(이외는 무시)


def _build_chat_instruction(product):
    """상품 데이터 + 역할/답변 지침을 담은 developer 프롬프트."""
    label = product.get_product_type_display()  # "적금" 또는 "예금"
    return (
        f"너는 {label} 상품 '{product.product_name}'({product.bank.bank_name})을 "
        "금융을 잘 모르는 사회초년생에게 쉽게 풀어 설명하는 OURWISH AI 도우미야. "
        "다정한 존댓말을 쓰되, 답변은 짧고 명확하게 해. 이모지는 쓰지 마.\n\n"

        "답변 원칙:\n"
        "- 사용자의 질문에 먼저 바로 답하고, 필요한 경우에만 짧게 부연 설명해.\n"
        "- 기본 답변은 2~4문장으로 작성해. 목록이 더 이해하기 쉬울 때만 bullet을 사용해.\n"
        "- 어려운 금융 용어는 중학생도 이해할 수 있게 쉽게 설명해.\n"
        "- 사용자가 '쉽게', '요약', '한마디로'라고 물으면 핵심만 1~2문장으로 답해.\n"
        "- 사용자가 '장점/단점', '누구에게 좋아?'라고 물으면 이 상품 정보에 근거해 생활 패턴 중심으로 설명해.\n"
        "- 사용자가 '우대금리', '우대조건'을 물으면 조건을 전부 나열하지 말고 대표 조건을 먼저 설명한 뒤, 필요하면 나머지를 덧붙여.\n"
        "- 사용자가 '얼마 받아?', '이자 계산'처럼 계산을 요구하면, 제공된 금리·기간·한도 정보 안에서만 계산해. 필요한 금액이나 기간 정보가 부족하면 먼저 부족한 정보를 알려줘.\n\n"
        "- 첫 문장은 결론부터 말하면 좋아. "
        "엄격한 제한:\n"
        "- 이 상품의 구체적인 수치·조건·기간·한도·금리는 아래 [상품 정보]에 있는 내용만 말해.\n"
        "- [상품 정보]에 없는 내용은 추측하지 말고 '이 상품은 그 부분이 제공된 정보에 없어요'라고 말해.\n"
        "- 가입을 권유하지 마. '가입하세요', '추천해요', '무조건 유리해요' 같은 표현은 금지해.\n"
        "- 수익을 보장하거나 단정하지 마.\n"
        "- '은행에서 확인하세요', '참고용입니다' 같은 문구는 정보가 부족하거나 계산이 불확실할 때만 사용해.\n"
        "- 이 상품과 관련 없는 질문이면 정중하게 이 상품의 금리, 가입조건, 우대조건 관련 질문으로 안내해.\n\n"

        "답변 스타일:\n"
        "- 친근하지만 과장 없는 말투를 사용해.\n"
        "- 문장은 짧게 써.\n"
        "- 금융 초보자가 바로 이해할 수 있게 생활 예시로 설명해.\n"
        "- 같은 말을 반복하지 마.\n\n"

        "[상품 정보]\n"
        f"상품명: {product.product_name}\n"
        f"은행명: {product.bank.bank_name}\n"
        f"가입 대상: {product.join_member or '정보 없음'}\n"
        f"가입 방법: {product.join_way or '정보 없음'}\n"
        f"납입 한도: {product.max_limit or '정보 없음'}\n"
        f"만기 후 이자: {product.maturity_interest or '정보 없음'}\n"
        f"기타 유의사항: {product.etc_note or '정보 없음'}\n"
        f"우대조건:\n{product.special_condition_raw or '없음'}\n"
    )

def _trim_history(messages):
    """프론트가 보낸 대화에서 user/assistant만 추려 최근 N턴(2*N개)만 남긴다."""
    cleaned = [
        {"role": m["role"], "content": m["content"].strip()}
        for m in messages
        if isinstance(m, dict)
        and m.get("role") in _CHAT_ROLES
        and isinstance(m.get("content"), str)
        and m["content"].strip()
    ]
    return cleaned[-(_CHAT_TURNS * 2):]


def _stream_gms(messages):
    """GMS를 stream 모드로 호출 → 답변 텍스트 조각을 차례로 yield. 실패 시 안내문."""
    if not settings.GMS_API_KEY:
        logger.warning("GMS_API_KEY 미설정 — LLM 호출 건너뜀")
        yield "죄송해요, 지금은 답변을 드릴 수 없어요."
        return
    try:
        res = requests.post(
            settings.GMS_API_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {settings.GMS_API_KEY}",
            },
            json={
                "model": settings.GMS_MODEL,
                "reasoning_effort": "low",
                "messages": messages,
                "stream": True,  # ← GMS가 토큰을 조각조각(SSE)으로 보내게
            },
            stream=True,  # ← requests도 응답을 통째로 안 받고 흘려받게
            timeout=_TIMEOUT,
        )
        res.raise_for_status()
        # GMS는 'data: {json}' 줄들을 보냄. 각 줄에서 delta.content만 뽑아 흘린다.
        for line in res.iter_lines(decode_unicode=True):
            if not line or not line.startswith("data:"):
                continue
            data = line[len("data:"):].strip()
            if data == "[DONE]":  # 끝 신호
                break
            try:
                chunk = json.loads(data)
            except json.JSONDecodeError:
                continue
            piece = chunk["choices"][0].get("delta", {}).get("content")
            if piece:
                yield piece
    except requests.HTTPError as exc:
        body = exc.response.text[:300] if exc.response is not None else ""
        logger.warning("GMS 스트리밍 실패: %s | %s", exc, body)
        yield "죄송해요, 답변을 가져오지 못했어요."
    except (requests.RequestException, KeyError, ValueError) as exc:
        logger.warning("GMS 스트리밍 실패: %s", exc)
        yield "죄송해요, 답변을 가져오지 못했어요."


def stream_chat_reply(product, messages):
    """상품 + 대화 배열 → 답변 텍스트 조각을 순서대로 yield (뷰의 StreamingHttpResponse용).

    messages: 프론트가 보낸 [{"role": "user"|"assistant", "content": str}, ...].
    """
    history = _trim_history(messages)
    if not history:
        return  # 보낼 게 없으면 아무것도 안 흘림 (뷰에서 이미 400으로 거름)
    full = [
        {"role": "developer", "content": _build_chat_instruction(product)},
        *history,
    ]
    yield from _stream_gms(full)
