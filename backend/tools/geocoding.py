import math
import requests

from backend.config import get_settings


def _get_coordinates(address: str) -> tuple[float, float] | None:
    """
    주소 → (위도, 경도) 변환.
    1차: 주소 검색 API (도로명/지번 상세 주소)
    2차: 키워드 검색 API (서울시 송파구 같은 행정구역명 fallback)
    """
    settings = get_settings()
    headers = {"Authorization": f"KakaoAK {settings.geocoding_api_key}"}

    # 1차 시도 — 주소 검색 API
    try:
        response = requests.get(
            "https://dapi.kakao.com/v2/local/search/address.json",
            headers=headers,
            params={"query": address},
            timeout=5,
        )
        response.raise_for_status()
        documents = response.json().get("documents", [])
        if documents:
            doc = documents[0]
            return float(doc["y"]), float(doc["x"])
    except Exception:
        pass

    # 2차 시도 — 키워드 검색 API (행정구역명 등 상세 주소가 아닌 경우)
    try:
        response = requests.get(
            "https://dapi.kakao.com/v2/local/search/keyword.json",
            headers=headers,
            params={"query": address},
            timeout=5,
        )
        response.raise_for_status()
        documents = response.json().get("documents", [])
        if documents:
            doc = documents[0]
            return float(doc["y"]), float(doc["x"])
    except Exception:
        pass

    return None


def _haversine_km(coord1: tuple[float, float], coord2: tuple[float, float]) -> float:
    """두 좌표 간 직선거리(km) 계산 — Haversine 공식."""
    R = 6371  # 지구 반지름 (km)
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


def _estimate_travel_time(distance_km: float) -> dict:
    """
    직선거리 기반 대략적 이동 시간 추정.
    - 실제 도로 거리는 직선거리의 약 1.3배로 보정
    - 차량: 평균 40km/h (서울 시내 기준)
    - 대중교통: 평균 25km/h (환승 대기 포함)
    """
    road_distance_km = round(distance_km * 1.3, 1)

    car_minutes = int((road_distance_km / 40) * 60)
    transit_minutes = int((road_distance_km / 25) * 60)

    def _format(minutes: int) -> str:
        if minutes < 60:
            return f"약 {minutes}분"
        return f"약 {minutes // 60}시간 {minutes % 60}분" if minutes % 60 else f"약 {minutes // 60}시간"

    return {
        "car": _format(car_minutes),
        "transit": _format(transit_minutes),
    }


def get_distance_info(candidate_address: str, company_address: str) -> dict:
    """
    지원자 주소와 회사 주소 간 거리 및 이동 시간을 반환합니다.

    Returns:
        {
            "distance_km": 12.3,
            "car_time": "약 24분",
            "transit_time": "약 38분",
            "error": None  # 실패 시 에러 메시지
        }
    """
    candidate_coord = _get_coordinates(candidate_address)
    if candidate_coord is None:
        return {"error": f"지원자 주소 좌표 변환 실패: {candidate_address}"}

    company_coord = _get_coordinates(company_address)
    if company_coord is None:
        return {"error": f"회사 주소 좌표 변환 실패: {company_address}"}

    distance_km = round(_haversine_km(candidate_coord, company_coord), 1)
    travel_time = _estimate_travel_time(distance_km)

    return {
        "distance_km": distance_km,
        "car_time": travel_time["car"],
        "transit_time": travel_time["transit"],
        "error": None,
    }
