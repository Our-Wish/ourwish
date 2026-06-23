"""YouTube Data API v3 호출 전담 모듈.

뷰(views.py)는 '무엇을 줄지'만 알고, '어떻게 YouTube를 부르는지'는 여기서 처리한다.
키는 .env의 YOUTUBE_API_KEY를 settings를 통해 읽어 쓴다(브라우저엔 노출되지 않음).
"""

import html

import requests
from django.conf import settings

# 검색(search.list)과 상세(videos.list)는 엔드포인트가 다르다.
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"


class YouTubeError(Exception):
    """YouTube 호출 실패(네트워크/쿼터 초과 등)를 뷰에 알리는 예외."""


def _pick_thumbnail(thumbnails):
    """썸네일 후보 중 화질 좋은 것부터 골라 URL 하나를 돌려준다."""
    for key in ("high", "medium", "default"):
        if key in thumbnails:
            return thumbnails[key]["url"]
    return ""


def _error_message(res):
    """YouTube 오류 응답(JSON)에서 사람이 읽을 메시지를 뽑는다(쿼터 초과 등)."""
    try:
        return res.json()["error"]["message"]
    except (ValueError, KeyError):
        return f"YouTube API 오류 (HTTP {res.status_code})"


VALID_ORDERS = {"relevance", "date", "viewCount", "rating"}


def search_videos(query, max_results=9, order="relevance"):
    """검색어로 영상 목록을 가져와, 화면에 필요한 필드만 정리해 리스트로 반환."""
    params = {
        "key": settings.YOUTUBE_API_KEY,
        "q": query,
        "part": "snippet",  # 제목·채널·썸네일 등 메타데이터
        "type": "video",  # 채널/재생목록 제외, 영상만
        "maxResults": max_results,
        "order": order if order in VALID_ORDERS else "relevance",
        "regionCode": "KR",
        "relevanceLanguage": "ko",
    }
    try:
        res = requests.get(YOUTUBE_SEARCH_URL, params=params, timeout=10)
    except requests.RequestException as e:
        raise YouTubeError(f"YouTube 검색 요청 실패: {e}")

    if res.status_code != 200:
        raise YouTubeError(_error_message(res))

    results = []
    for item in res.json().get("items", []):
        snippet = item["snippet"]
        results.append(
            {
                "video_id": item["id"]["videoId"],
                # YouTube는 제목·채널명을 HTML 이스케이프(&#39; 등)해 주므로 풀어준다.
                "title": html.unescape(snippet["title"]),
                "channel_name": html.unescape(snippet["channelTitle"]),
                "thumbnail_url": _pick_thumbnail(snippet["thumbnails"]),
                "published_at": snippet["publishedAt"],
            }
        )
    return results


def get_video_detail(video_id):
    """영상 1개의 상세 정보를 반환. 존재하지 않으면 None(→ 뷰에서 404)."""
    params = {
        "key": settings.YOUTUBE_API_KEY,
        "id": video_id,
        "part": "snippet",
    }
    try:
        res = requests.get(YOUTUBE_VIDEOS_URL, params=params, timeout=10)
    except requests.RequestException as e:
        raise YouTubeError(f"YouTube 상세 요청 실패: {e}")

    if res.status_code != 200:
        raise YouTubeError(_error_message(res))

    items = res.json().get("items", [])
    if not items:
        return None

    snippet = items[0]["snippet"]
    return {
        "video_id": video_id,
        # 제목·채널명·설명 모두 HTML 이스케이프되어 오므로 풀어준다.
        "title": html.unescape(snippet["title"]),
        "channel_name": html.unescape(snippet["channelTitle"]),
        "published_at": snippet["publishedAt"],
        "description": html.unescape(snippet.get("description", "")),
        "thumbnail_url": _pick_thumbnail(snippet["thumbnails"]),
    }
