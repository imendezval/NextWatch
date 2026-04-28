from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    movie_files = list(Path("data/raw/tmdb/movie").glob("ingest_date=*/*.json"))

    print(f"Found {len(movie_files)} raw movie detail files.")

    if not movie_files:
        raise RuntimeError("No movie files found. Run `pixi run ingest-small` first.")

    sample_path = movie_files[0]

    with sample_path.open("r", encoding="utf-8") as f:
        sample = json.load(f)

    print("Sample file:", sample_path)
    print("Movie ID:", sample.get("id"))
    print("Title:", sample.get("title"))
    print("Release date:", sample.get("release_date"))
    print("Genres:", [g.get("name") for g in sample.get("genres", [])])


if __name__ == "__main__":
    main()
