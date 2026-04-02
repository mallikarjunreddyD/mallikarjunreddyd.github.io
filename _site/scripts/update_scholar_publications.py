import argparse
import json
import os
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


def bibtex_get_field(bibtex: str, field_name: str) -> str | None:
    """
    Very small BibTeX field extractor for the specific format we get from `scholarly.bibtex(...)`.
    Handles: field = { ... }  and field = " ... "
    """
    # Try braces first
    pattern_braces = rf"{re.escape(field_name)}\s*=\s*\{{\s*([^}}]+?)\s*\}}"
    m = re.search(pattern_braces, bibtex, flags=re.IGNORECASE)
    if m:
        return m.group(1).strip()

    # Then double-quotes
    pattern_quotes = rf'{re.escape(field_name)}\s*=\s*"\s*([^"]+?)\s*"'
    m = re.search(pattern_quotes, bibtex, flags=re.IGNORECASE)
    if m:
        return m.group(1).strip()

    return None


def bibtex_to_publication(bibtex: str) -> dict:
    entry_type_match = re.match(r"@(\w+)\s*\{", bibtex.strip())
    entry_type = entry_type_match.group(1).lower() if entry_type_match else None

    title = bibtex_get_field(bibtex, "title")
    year_raw = bibtex_get_field(bibtex, "year")
    try:
        year = int(year_raw) if year_raw else None
    except Exception:
        year = None

    author_raw = bibtex_get_field(bibtex, "author")
    # "Last, First and Last, First" -> "Last, First; Last, First"
    authors = None
    if author_raw:
        authors = author_raw.replace(" and ", "; ").replace("{", "").replace("}", "")

    journal = bibtex_get_field(bibtex, "journal")
    booktitle = bibtex_get_field(bibtex, "booktitle")
    venue = journal or booktitle
    if venue:
        venue = venue.replace("{", "").replace("}", "")
    if title:
        title = title.replace("{", "").replace("}", "")

    url = bibtex_get_field(bibtex, "url")
    doi = bibtex_get_field(bibtex, "doi")
    if not url and doi:
        url = f"https://doi.org/{doi}"

    return {
        "type": entry_type,
        "year": year,
        "title": title,
        "authors": authors,
        "venue": venue,
        "url": url,
        "bibtex": bibtex,  # keep for debugging/extension; not rendered
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
            pub = scholarly.fill(pub)
            # `scholarly` provides BibTeX for each publication.
            bibtex = scholarly.bibtex(pub)
            parsed = bibtex_to_publication(bibtex)
            if parsed.get("year") is not None and parsed.get("title"):
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

