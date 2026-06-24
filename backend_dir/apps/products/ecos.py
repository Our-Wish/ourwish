"""한국은행 ECOS(경제통계시스템) — 예금은행 가중평균 수신금리 조회.

STEP1 예상 수령액에 쓰던 '평균 금리' 고정값(적금 4.0% / 예금 3.5%)을
실제 한국은행 통계로 대체한다. 통계가 월 단위 + 약 2개월 지연이라
매 요청마다 부르지 않고 하루 캐시 + 실패 시 폴백한다.

통계표 121Y002 = 예금은행 수신금리(신규취급액 기준), 월(M)
  정기예금 BEABAA211 / 정기적금 BEABAA212  (DATA_VALUE는 연 % 문자열)
"""

import datetime
import logging

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

_BASE = "https://ecos.bok.or.kr/api/StatisticSearch"
_STAT_CODE = "121Y002"
_ITEM_DEPOSIT = "BEABAA211"  # 정기예금
_ITEM_SAVINGS = "BEABAA212"  # 정기적금

_CACHE_KEY = "ecos_market_rates"
_CACHE_TTL = 60 * 60 * 24  # 24시간(통계가 월 단위라 충분)

# ECOS 실패/미설정 시 사용할 폴백(기존 화면에 박혀있던 평균 금리, 연 %)
_FALLBACK = {
    "deposit_avg": 3.5,
    "savings_avg": 4.0,
    "as_of": None,
    "source": "fallback",
    "is_fallback": True,
}


def _fetch_latest_rate(item_code):
    """해당 항목의 최근 약 12개월 중 가장 최근 값을 (연 %, 'YYYY-MM')로 반환."""
    key = settings.ECOS_API_KEY
    if not key:
        raise RuntimeError("ECOS_API_KEY 미설정")

    today = datetime.date.today()
    end = today.strftime("%Y%m")
    start = f"{today.year - 1}{today.month:02d}"  # 약 12개월 범위
    url = f"{_BASE}/{key}/json/kr/1/100/{_STAT_CODE}/M/{start}/{end}/{item_code}"

    res = requests.get(url, timeout=5)
    res.raise_for_status()
    rows = res.json().get("StatisticSearch", {}).get("row", [])

    # 최신월이 아직 비어있을 수 있어, 뒤(최근)에서부터 값이 있는 첫 행을 쓴다.
    for row in reversed(rows):
        value = row.get("DATA_VALUE")
        if value not in (None, ""):
            ym = row.get("TIME", "")  # 'YYYYMM'
            as_of = f"{ym[:4]}-{ym[4:]}" if len(ym) == 6 else ym
            return round(float(value), 2), as_of
    raise RuntimeError(f"ECOS 응답에 유효한 값 없음: {item_code}")


def get_market_rates():
    """STEP1 평균 금리(연 %). 하루 캐시, 실패하면 폴백(폴백은 캐시하지 않아 다음에 재시도)."""
    cached = cache.get(_CACHE_KEY)
    if cached is not None:
        return cached
    try:
        deposit_avg, as_of = _fetch_latest_rate(_ITEM_DEPOSIT)
        savings_avg, _ = _fetch_latest_rate(_ITEM_SAVINGS)
    except Exception as e:
        # 키 미설정·네트워크·포맷 오류 등 → 화면이 깨지지 않게 폴백
        logger.warning("ECOS 평균금리 조회 실패, 폴백 사용: %s", e)
        return _FALLBACK

    result = {
        "deposit_avg": deposit_avg,
        "savings_avg": savings_avg,
        "as_of": as_of,
        "source": "BOK ECOS 121Y002",
        "is_fallback": False,
    }
    cache.set(_CACHE_KEY, result, _CACHE_TTL)
    return result
