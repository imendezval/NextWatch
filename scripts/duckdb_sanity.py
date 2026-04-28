from __future__ import annotations

import duckdb


def main() -> None:
    con = duckdb.connect()

    print("\nMovies count:")
    print(
        con.sql(
            """
            SELECT COUNT(*) AS n_movies
            FROM 'data/curated/movies.parquet'
            """
        )
    )

    print("\nTop genres:")
    print(
        con.sql(
            """
            SELECT
                genre_name,
                COUNT(*) AS n_movies
            FROM 'data/curated/movie_genres.parquet'
            GROUP BY genre_name
            ORDER BY n_movies DESC
            """
        )
    )

    print("\nMost common cast members in this sample:")
    print(
        con.sql(
            """
            SELECT
                name,
                COUNT(DISTINCT movie_id) AS n_movies
            FROM 'data/curated/movie_cast.parquet'
            GROUP BY name
            ORDER BY n_movies DESC
            LIMIT 20
            """
        )
    )

    print("\nMovies with many keywords:")
    print(
        con.sql(
            """
            SELECT
                m.movie_id,
                m.title,
                COUNT(k.keyword_id) AS n_keywords
            FROM 'data/curated/movies.parquet' AS m
            LEFT JOIN 'data/curated/movie_keywords.parquet' AS k
                ON m.movie_id = k.movie_id
            GROUP BY m.movie_id, m.title
            ORDER BY n_keywords DESC
            LIMIT 20
            """
        )
    )


if __name__ == "__main__":
    main()
