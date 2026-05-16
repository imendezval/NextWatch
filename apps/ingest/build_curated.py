from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
from rich.console import Console

from apps.ingest.normalize import (
    normalize_movie,
    normalize_movie_cast,
    normalize_movie_crew,
    normalize_movie_genres,
    normalize_movie_keywords,
)

from apps.ingest.schemas import validate_dataframe

console = Console()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_parquet(rows: list[dict[str, Any]], output_path: Path, table_name: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(rows)

    if df.empty:
        console.print(f"[yellow]Skipping empty table: {output_path}[/yellow]")
        return
    
    df = validate_dataframe(df, table_name=table_name)

    df.to_parquet(output_path, index=False)


def main() -> None:
    movie_files = sorted(Path("data/raw/tmdb/movie").glob("ingest_date=*/*.json"))

    if not movie_files:
        raise RuntimeError("No raw movie JSON files found. Run `pixi run ingest-small` first.")

    movies: list[dict[str, Any]] = []
    movie_genres: list[dict[str, Any]] = []
    movie_keywords: list[dict[str, Any]] = []
    movie_cast: list[dict[str, Any]] = []
    movie_crew: list[dict[str, Any]] = []

    for path in movie_files:
        movie = read_json(path)

        movies.append(normalize_movie(movie))
        movie_genres.extend(normalize_movie_genres(movie))
        movie_keywords.extend(normalize_movie_keywords(movie))
        movie_cast.extend(normalize_movie_cast(movie))
        movie_crew.extend(normalize_movie_crew(movie))

    write_parquet(movies, Path("data/curated/movies.parquet"), "movies")
    write_parquet(movie_genres, Path("data/curated/movie_genres.parquet"), "movie_genres")
    write_parquet(movie_keywords, Path("data/curated/movie_keywords.parquet"), "movie_keywords")
    write_parquet(movie_cast, Path("data/curated/movie_cast.parquet"), "movie_cast")
    write_parquet(movie_crew, Path("data/curated/movie_crew.parquet"), "movie_crew")

    console.print("[green]Curated Parquet tables written to data/curated[/green]")
    console.print(f"movies: {len(movies)}")
    console.print(f"movie_genres: {len(movie_genres)}")
    console.print(f"movie_keywords: {len(movie_keywords)}")
    console.print(f"movie_cast: {len(movie_cast)}")
    console.print(f"movie_crew: {len(movie_crew)}")


if __name__ == "__main__":
    main()
