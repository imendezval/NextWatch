from __future__ import annotations

import os
import time
from typing import Any

import requests
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential


class TMDBClient:
    def __init__(self) -> None:
        load_dotenv()

        self.api_key = os.getenv("TMDB_API_KEY")
        if not self.api_key:
            raise RuntimeError("TMDB_API_KEY is missing. Add it to your .env file.")

        self.base_url = "https://api.themoviedb.org/3"
        self.rate_per_sec = float(os.getenv("TMDB_READ_RATE_PER_SEC", "3"))
        self.sleep_seconds = 1.0 / self.rate_per_sec

    @retry(
        wait=wait_exponential(multiplier=1, min=1, max=30),
        stop=stop_after_attempt(5),
        reraise=True,
    )
    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        time.sleep(self.sleep_seconds)

        query_params = params.copy() if params else {}
        query_params["api_key"] = self.api_key

        response = requests.get(
            f"{self.base_url}{path}",
            params=query_params,
            timeout=30,
        )

        if response.status_code == 429:
            raise RuntimeError("TMDB rate limit hit. Retrying...")

        response.raise_for_status()
        return response.json()

    def discover_movies(self, page: int = 1) -> dict[str, Any]:
        return self.get(
            "/discover/movie",
            params={
                "page": page,
                "sort_by": "popularity.desc",
                "include_adult": "false",
                "language": "en-US",
            },
        )

    def movie_details(self, movie_id: int) -> dict[str, Any]:
        return self.get(
            f"/movie/{movie_id}",
            params={
                "language": "en-US",
                "append_to_response": "credits,keywords",
            },
        )
