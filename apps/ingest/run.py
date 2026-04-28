from __future__ import annotations

import argparse
from datetime import date

from rich.console import Console
from rich.progress import track

from apps.ingest.client import TMDBClient
from apps.ingest.writer import write_json

console = Console()


def run_ingest(pages: int, ingest_date: str) -> None:
    client = TMDBClient()

    movie_ids: list[int] = []

    console.print(f"[bold]Fetching {pages} discover pages...[/bold]")

    for page in range(1, pages + 1):
        payload = client.discover_movies(page=page)
        write_json(payload, entity="discover_movie", item_id=f"page_{page}", ingest_date=ingest_date)

        for movie in payload.get("results", []):
            movie_id = movie.get("id")
            if movie_id is not None:
                movie_ids.append(int(movie_id))

    unique_movie_ids = sorted(set(movie_ids))

    console.print(f"[bold]Fetching details for {len(unique_movie_ids)} movies...[/bold]")

    for movie_id in track(unique_movie_ids):
        details = client.movie_details(movie_id)
        write_json(details, entity="movie", item_id=movie_id, ingest_date=ingest_date)

    console.print("[green]Done.[/green]")
    console.print(f"Raw data written under data/raw/tmdb/*/ingest_date={ingest_date}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=int, default=2)
    parser.add_argument("--date", type=str, default=date.today().isoformat())
    args = parser.parse_args()

    run_ingest(pages=args.pages, ingest_date=args.date)


if __name__ == "__main__":
    main()
