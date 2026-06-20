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


# ── 2) AI 쉬운말 소개(친절한 핵심 + 어려운 용어 1개 풀이) ──
# 서비스 목적: 금융 용어를 잘 모르는 사회초년생도 상품을 이해하게 돕는 것.
# 그래서 AI는 "추천 카피"가 아니라 "어려운 상품 설명을 친절하게 풀어주는 통역기".
# 사회초년생이 '진짜로' 막히는 전문용어(평잔·고시금리 등)만 골라 풀어준다(없으면 비움).
# LLM에는 {용어, 뜻}만 받고, "'OOO'는 ~라는 뜻이에요!" 친절한 문장은 파이썬이
# 조립한다. 조사(은/는·라는/이라는)도 받침을 보고 직접 붙여 맞춤법 오류를 없앤다.
_AI_SUMMARY_DEVELOPER = """
너는 금융을 처음 접하는 사회초년생에게, 어려운 적금 상품 설명을
중학생도 알아들을 만큼 쉽고 친절하게 풀어주는 도우미야.

상품의 가입대상·가입방법·납입한도·만기이자·유의사항·우대조건을 읽고
summary 한 문장과 terms(진짜 어려운 용어 풀이)를 만들어.

- summary: 이 적금의 핵심을 쉽고 다정한 말로 한 문장(70자 이내, '~요!'로 끝낸다).
  우대조건이 있으면 "무슨 행동을 하면 우대받는지"를 구체적으로 짚어줘.
  예) "이 은행으로 월급 받고, 공과금 자동이체 걸고, 카드까지 쓰면 우대받는 적금이에요!"
  ※ 급여이체·공과금 자동이체·카드사용·주택청약·비대면가입 등 실제 조건 이름을 말해.
  ※ 우대조건이 여러 개여도 대표적인 2~3개만 골라 간결하게. 전부 나열하지 마(문장만 길어진다).
  ※ "조건을 채우면 이자를 더 받아요"처럼 두루뭉술한 말은 금지(누구나 아는 말이라
    알맹이가 없다). 무슨 조건인지 콕 집어줘.
  ※ %p·금액("1만원"·"300만원")·기간("6개월"·"1년") 같은 숫자는 절대 쓰지 마. '무슨 행동'인지만.
  ※ 우대조건이 거의 없으면 단점(만기 후 이자 감소 등)을 끌어오지 말고,
    "누구나 쉽게 가입할 수 있는" 같은 담백한 핵심으로 적어.

- terms: 단어만 봐서는 뜻을 짐작하기 어려운 "진짜 전문용어" 중에서
  가장 어렵고 중요한 딱 1개만 골라 쉽게 풀이.
  꼭 풀어줄 만한 예: 평잔, 고시금리, 고시이율, 거치식, 비과세, 단리, 복리,
    정액적립식, 자유적립식.
  ※ 우대금리·우대이율·만기·급여이체·자동이체·카드실적·가입·통장처럼 이름만 봐도
    대충 통하는 말은 절대 넣지 마. 사회초년생도 그 정도는 안다.
  ※ 진짜 어려운 용어가 없으면 terms는 빈 배열([])로 둬. 억지로 채우지 마.
  항목은 {"term": 용어, "meaning": 뜻} 하나만. meaning에는 조사·문장부호·따옴표를 넣지 말고,
  명사로 끝나는 30자 안팎의 쉬운 풀이만 적어. (출력에 '명사구' 같은 메타표현 쓰지 마!)
  예: "일정 기간 통장에 있던 평균 잔액", "은행이 정해 공시한 기준 이자율",
      "원금에만 이자가 붙는 방식".

규칙:
- summary와 terms 모두 반드시 원문에 근거. 지어내지 마.
- 과장·광고 문구 금지. 따뜻하고 친절한 말투로.
- 반드시 JSON 객체 하나만 출력. 마크다운·설명 금지. 키: summary, terms.

퓨샷 예시:
입력:
상품명: 주거래우대적금 (행복은행)
가입 대상: 실명의 개인
우대조건: 급여이체 0.7%p / 공과금 자동이체 0.3%p / 신용·체크카드 결제 0.3%p
만기 후 이자: 만기 후에는 고시이율의 절반만 적용

출력:
{"summary": "이 은행으로 월급 받고, 공과금 자동이체 걸고, 카드까지 쓰면 우대받는 적금이에요!", "terms": [{"term": "고시이율", "meaning": "은행이 정해 공시한 기준 이자율"}]}

입력:
상품명: 자유모아적금 (든든은행)
가입 대상: 실명의 개인
납입 한도: 월 100만원 자유적립식, 단리
우대조건: 비대면 가입 / 평잔 50만원 이상 유지

출력:
{"summary": "비대면으로 가입하고 통장에 일정 금액을 꾸준히 두면 우대받는, 자유롭게 넣는 적금이에요!", "terms": [{"term": "평잔", "meaning": "일정 기간 통장에 있던 평균 잔액"}]}
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
    data = _parse_json(_chat(_AI_SUMMARY_DEVELOPER, user))
    if not data:
        return None
    summary = (data.get("summary") or "").strip()
    if not summary:
        return None
    terms = data.get("terms")
    if not isinstance(terms, list):
        terms = []
    return _render_summary(summary, terms[:1])  # 어려운 용어는 1개만 보여준다
