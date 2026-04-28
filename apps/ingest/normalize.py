from __future__ import annotations

from typing import Any


def normalize_movie(movie: dict[str, Any]) -> dict[str, Any]:
    return {
        "movie_id": movie.get("id"),
        "title": movie.get("title"),
        "original_title": movie.get("original_title"),
        "overview": movie.get("overview"),
        "release_date": movie.get("release_date") or None,
        "runtime": movie.get("runtime"),
        "budget": movie.get("budget"),
        "revenue": movie.get("revenue"),
        "popularity": movie.get("popularity"),
        "vote_average": movie.get("vote_average"),
        "vote_count": movie.get("vote_count"),
        "adult": movie.get("adult"),
        "original_language": movie.get("original_language"),
        "status": movie.get("status"),
        "tagline": movie.get("tagline"),
        "homepage": movie.get("homepage"),
        "imdb_id": movie.get("imdb_id"),
    }


def normalize_movie_genres(movie: dict[str, Any]) -> list[dict[str, Any]]:
    movie_id = movie.get("id")
    rows = []

    for genre in movie.get("genres", []):
        rows.append(
            {
                "movie_id": movie_id,
                "genre_id": genre.get("id"),
                "genre_name": genre.get("name"),
            }
        )

    return rows


def normalize_movie_keywords(movie: dict[str, Any]) -> list[dict[str, Any]]:
    movie_id = movie.get("id")
    rows = []

    keywords_payload = movie.get("keywords", {})
    keywords = keywords_payload.get("keywords", [])

    for keyword in keywords:
        rows.append(
            {
                "movie_id": movie_id,
                "keyword_id": keyword.get("id"),
                "keyword_name": keyword.get("name"),
            }
        )

    return rows


def normalize_movie_cast(movie: dict[str, Any]) -> list[dict[str, Any]]:
    movie_id = movie.get("id")
    rows = []

    credits = movie.get("credits", {})
    cast = credits.get("cast", [])

    for person in cast:
        rows.append(
            {
                "movie_id": movie_id,
                "person_id": person.get("id"),
                "name": person.get("name"),
                "character": person.get("character"),
                "cast_order": person.get("order"),
                "known_for_department": person.get("known_for_department"),
                "gender": person.get("gender"),
                "popularity": person.get("popularity"),
            }
        )

    return rows


def normalize_movie_crew(movie: dict[str, Any]) -> list[dict[str, Any]]:
    movie_id = movie.get("id")
    rows = []

    credits = movie.get("credits", {})
    crew = credits.get("crew", [])

    for person in crew:
        rows.append(
            {
                "movie_id": movie_id,
                "person_id": person.get("id"),
                "name": person.get("name"),
                "job": person.get("job"),
                "department": person.get("department"),
                "known_for_department": person.get("known_for_department"),
                "gender": person.get("gender"),
                "popularity": person.get("popularity"),
            }
        )

    return rows
