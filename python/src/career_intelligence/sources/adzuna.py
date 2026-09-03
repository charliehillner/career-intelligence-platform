import requests

from career_intelligence.config import get_adzuna_credentials


BASE_URL = "https://api.adzuna.com/v1/api/jobs"


def search_jobs(
    query: str,
    country: str = "de",
    page: int = 1,
    results_per_page: int = 10,
) -> dict:
    app_id, app_key = get_adzuna_credentials()

    url = f"{BASE_URL}/{country}/search/{page}"

    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": query,
        "results_per_page": results_per_page,
    }

    headers = {
        "Accept": "application/json",
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()