from __future__ import annotations

import pandas as pd
from pandera import Check, Column, DataFrameSchema


movies_schema = DataFrameSchema(
    {
        "movie_id": Column(int, nullable=False, unique=True),
        "title": Column(str, nullable=True),
        "original_title": Column(str, nullable=True),
        "overview": Column(str, nullable=True),
        "release_date": Column(str, nullable=True),
        "runtime": Column(float, nullable=True, checks=Check.ge(0)),
        "budget": Column(float, nullable=True, checks=Check.ge(0)),
        "revenue": Column(float, nullable=True, checks=Check.ge(0)),
        "popularity": Column(float, nullable=True, checks=Check.ge(0)),
        "vote_average": Column(float, nullable=True, checks=Check.in_range(0, 10)),
        "vote_count": Column(float, nullable=True, checks=Check.ge(0)),
        "adult": Column(bool, nullable=True),
        "original_language": Column(str, nullable=True),
        "status": Column(str, nullable=True),
        "tagline": Column(str, nullable=True),
        "homepage": Column(str, nullable=True),
        "imdb_id": Column(str, nullable=True),
    },
    coerce=True,
)


movie_genres_schema = DataFrameSchema(
    {
        "movie_id": Column(int, nullable=False),
        "genre_id": Column(int, nullable=False),
        "genre_name": Column(str, nullable=False),
    },
    coerce=True,
)


movie_keywords_schema = DataFrameSchema(
    {
        "movie_id": Column(int, nullable=False),
        "keyword_id": Column(int, nullable=False),
        "keyword_name": Column(str, nullable=False),
    },
    coerce=True,
)


movie_cast_schema = DataFrameSchema(
    {
        "movie_id": Column(int, nullable=False),
        "person_id": Column(int, nullable=False),
        "name": Column(str, nullable=False),
        "character": Column(str, nullable=True),
        "cast_order": Column(float, nullable=True),
        "known_for_department": Column(str, nullable=True),
        "gender": Column(float, nullable=True),
        "popularity": Column(float, nullable=True),
    },
    coerce=True,
)


movie_crew_schema = DataFrameSchema(
    {
        "movie_id": Column(int, nullable=False),
        "person_id": Column(int, nullable=False),
        "name": Column(str, nullable=False),
        "job": Column(str, nullable=True),
        "department": Column(str, nullable=True),
        "known_for_department": Column(str, nullable=True),
        "gender": Column(float, nullable=True),
        "popularity": Column(float, nullable=True),
    },
    coerce=True,
)


def validate_dataframe(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    schemas = {
        "movies": movies_schema,
        "movie_genres": movie_genres_schema,
        "movie_keywords": movie_keywords_schema,
        "movie_cast": movie_cast_schema,
        "movie_crew": movie_crew_schema,
    }

    schema = schemas[table_name]
    return schema.validate(df, lazy=True)
