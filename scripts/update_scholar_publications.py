import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs


def extract_scholar_user_id(config_text: str) -> str | None:
    """
    Reads `_config.yml` and extracts the Google Scholar user id from:
      author:
        google_scholar: https://scholar.google.com/citations?user=YOUR_ID
    """
    # Example line: google_scholar: https://scholar.google.com/citations?user=Ru1f2rkAAAAJ
    m = re.search(r"google_scholar:\s*(\S+)", config_text)
    if not m:
        return None
    url = m.group(1)
    try:
        parsed = urlparse(url)
        if parsed.netloc and "scholar.google" in parsed.netloc:
            qs = parse_qs(parsed.query)
            user_ids = qs.get("user") or []
            return user_ids[0] if user_ids else None
    except Exception:
        return None

    return None


def pub_to_publication(pub: dict) -> dict | None:
    """
    Convert `scholarly`'s filled publication object into our simplified schema.

    In practice, `scholarly.fill(...)` in this environment provides most fields
    inside `pub["bib"]` (a dict) such as:
      - title
      - pub_year
      - author
      - citation
      - pages, volume, publisher ...
    """
    bib = pub.get("bib")
    if not isinstance(bib, dict):
        return None

    title = bib.get("title") or pub.get("title")
    pub_year = bib.get("pub_year")
    try:
        year = int(pub_year) if pub_year is not None else None
    except Exception:
        year = None

    authors_raw = bib.get("author")
    authors = None
    if authors_raw:
        authors = (
            str(authors_raw)
            .replace("{", "")
            .replace("}", "")
            .replace(" and ", "; ")
        )

    # `citation` is usually already "Journal/Conference, volume/pages, year" (title is not repeated).
    venue = bib.get("citation") or bib.get("journal") or bib.get("booktitle")

    url = pub.get("pub_url") or pub.get("url")  # usually a Google Scholar "Cited by"/publication URL

    if not title or year is None:
        return None

    if isinstance(venue, str):
        venue = venue.replace("{", "").replace("}", "")

    return {
        "type": pub.get("source"),
        "year": year,
        "title": str(title).replace("{", "").replace("}", ""),
        "authors": authors,
        "venue": venue,
        "url": url,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch Google Scholar publications and generate Jekyll _data JSON.")
    parser.add_argument(
        "--scholar-user-id",
        dest="scholar_user_id",
        default=None,
        help="Google Scholar user id (the value after `user=`). If omitted, it is read from _config.yml.",
    )
    parser.add_argument(
        "--max",
        type=int,
        default=200,
        help="Max number of publications to fetch (helps keep runs fast).",
    )
    parser.add_argument(
        "--order",
        choices=["ascending", "descending"],
        default="descending",
        help="Sort order by year.",
    )
    args = parser.parse_args()

    # Import here so the script can print a nicer message when the dependency is missing.
    try:
        from scholarly import scholarly
    except ImportError:
        raise SystemExit(
            "Missing dependency: scholarly. Install it with:\n"
            "  pip3 install scholarly"
        )

    root = Path(__file__).resolve().parents[1]
    config_path = root / "_config.yml"
    config_text = config_path.read_text(encoding="utf-8")

    scholar_user_id = args.scholar_user_id or extract_scholar_user_id(config_text)
    if not scholar_user_id:
        raise SystemExit("Could not determine Google Scholar user id. Provide --scholar-user-id or fix _config.yml.")

    author = scholarly.search_author_id(scholar_user_id)
    author = scholarly.fill(author)
    pubs = author.get("publications") or []

    publications = []
    for pub in pubs[: args.max]:
        try:
            filled = scholarly.fill(pub)
            parsed = pub_to_publication(filled)
            if parsed:
                publications.append(parsed)
        except Exception:
            # Skip items that can't be parsed; Scholar data can have edge cases.
            continue

    # Group by year
    year_to_items: dict[int, list] = {}
    for p in publications:
        year = p["year"]
        if year is None:
            continue
        year_to_items.setdefault(year, []).append(p)

    years_sorted = sorted(year_to_items.keys(), reverse=(args.order == "descending"))

    groups = []
    for year in years_sorted:
        # Within the year, keep a stable sort by title
        items = sorted(year_to_items[year], key=lambda x: (x.get("title") or "").lower())
        groups.append(
            {
                "year": year,
                "publications": [
                    {
                        "type": it.get("type"),
                        "title": it.get("title"),
                        "authors": it.get("authors"),
                        "venue": it.get("venue"),
                        "url": it.get("url"),
                    }
                    for it in items
                ],
            }
        )

    out_dir = root / "_data"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "scholar_publications.json"
    out_path.write_text(json.dumps(groups, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Wrote {len(groups)} year-groups to {out_path}")


if __name__ == "__main__":
    main()

