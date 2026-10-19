"""JSON CLI for locally saved job roles."""

from contextlib import closing
import json
from pathlib import Path
import sqlite3
import sys
from urllib.parse import urlsplit

from record import JsonArgumentParser


def normalized(value):
    return " ".join(value.split()).casefold()


def main():
    parser = JsonArgumentParser()
    parser.add_argument("--db", required=True, type=Path)
    commands = parser.add_subparsers(dest="command", required=True, parser_class=JsonArgumentParser)
    save = commands.add_parser("save")
    save.add_argument("--company", required=True)
    save.add_argument("--title", required=True)
    save.add_argument("--url")
    save.add_argument("--file", type=Path)
    save.add_argument("--new-posting", action="store_true")
    show = commands.add_parser("show")
    show.add_argument("--id", required=True, type=int)
    find = commands.add_parser("find")
    find.add_argument("--url")
    find.add_argument("--company")
    find.add_argument("--title")
    args = parser.parse_args()

    try:
        if not args.db.is_absolute():
            raise ValueError("database path must be absolute")

        if args.command == "save":
            company, title = args.company.strip(), args.title.strip()
            if not company or not title:
                raise ValueError("company and title must not be empty")
            url = args.url.strip() if args.url is not None else None
            if url is not None:
                parts = urlsplit(url)
                if (parts.scheme != "https" or not parts.hostname or parts.username is not None
                        or any(c.isspace() or c == "\\" for c in url)):
                    raise ValueError("URL must be HTTPS with a hostname")
                _ = parts.port
            source_text = ""
            if args.file is not None:
                if not args.file.is_absolute():
                    raise ValueError("source file path must be absolute")
                with args.file.open("r", encoding="utf-8", newline="") as source:
                    source_text = source.read()

            company_key, title_key = normalized(company), normalized(title)
            with closing(sqlite3.connect(args.db)) as connection:
                connection.row_factory = sqlite3.Row
                with connection:
                    connection.execute("BEGIN IMMEDIATE")
                    connection.execute(
                        "CREATE TABLE IF NOT EXISTS jobs ("
                        "id INTEGER PRIMARY KEY, company TEXT NOT NULL, title TEXT NOT NULL, "
                        "url TEXT UNIQUE, source_text TEXT NOT NULL, "
                        "company_key TEXT NOT NULL, title_key TEXT NOT NULL)"
                    )
                    url_match = connection.execute(
                        "SELECT * FROM jobs WHERE url = ?", (url,)
                    ).fetchone() if url is not None else None
                    matches = connection.execute(
                        "SELECT * FROM jobs WHERE company_key = ? AND title_key = ? ORDER BY id",
                        (company_key, title_key),
                    ).fetchall()

                    if url_match is not None:
                        if (url_match["company_key"] == company_key
                                and url_match["title_key"] == title_key
                                and url_match["source_text"] == source_text):
                            result = {"outcome": "existing", "id": url_match["id"]}
                        else:
                            result = {"outcome": "candidates", "candidates": [
                                {key: url_match[key] for key in ("id", "company", "title", "url")}
                            ]}
                    elif (not args.new_posting and url is None and len(matches) == 1
                          and matches[0]["url"] is None
                          and matches[0]["source_text"] == source_text):
                        result = {"outcome": "existing", "id": matches[0]["id"]}
                    elif matches and not args.new_posting:
                        result = {"outcome": "candidates", "candidates": [
                            {key: row[key] for key in ("id", "company", "title", "url")}
                            for row in matches
                        ]}
                    else:
                        cursor = connection.execute(
                            "INSERT INTO jobs (company, title, url, source_text, company_key, title_key) "
                            "VALUES (?, ?, ?, ?, ?, ?)",
                            (company, title, url, source_text, company_key, title_key),
                        )
                        result = {"outcome": "created", "id": cursor.lastrowid}
        elif args.command == "show":
            with closing(sqlite3.connect(args.db.as_uri() + "?mode=ro", uri=True)) as connection:
                connection.row_factory = sqlite3.Row
                row = connection.execute(
                    "SELECT id, company, title, url, source_text FROM jobs WHERE id = ?",
                    (args.id,),
                ).fetchone()
            if row is None:
                raise ValueError("role not found")
            result = dict(row)
        else:
            if (args.url is None and (args.company is None or args.title is None)) or (
                    args.url is not None and (args.company is not None or args.title is not None)):
                raise ValueError("find requires either --url or both --company and --title")
            if args.url is not None:
                url = args.url.strip()
                parts = urlsplit(url)
                if (parts.scheme != "https" or not parts.hostname or parts.username is not None
                        or any(c.isspace() or c == "\\" for c in url)):
                    raise ValueError("URL must be HTTPS with a hostname")
                _ = parts.port
                query, values = "url = ?", (url,)
            else:
                if not args.company.strip() or not args.title.strip():
                    raise ValueError("company and title must not be empty")
                query, values = "company_key = ? AND title_key = ?", (
                    normalized(args.company), normalized(args.title))
            with closing(sqlite3.connect(args.db.as_uri() + "?mode=ro", uri=True)) as connection:
                connection.row_factory = sqlite3.Row
                rows = connection.execute(
                    "SELECT id, company, title, url, source_text FROM jobs WHERE " + query + " ORDER BY id",
                    values,
                ).fetchall()
            result = {"candidates": [dict(row) for row in rows]}

        print(json.dumps(result))
    except (OSError, UnicodeError, sqlite3.Error, ValueError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
