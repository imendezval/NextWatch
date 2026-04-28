from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


def write_json(
    obj: dict[str, Any],
    entity: str,
    item_id: int | str,
    ingest_date: str | None = None,
) -> Path:
    current_date = ingest_date or date.today().isoformat()

    out_dir = Path("data/raw/tmdb") / entity / f"ingest_date={current_date}"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / f"{item_id}.json"

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

    return out_path
