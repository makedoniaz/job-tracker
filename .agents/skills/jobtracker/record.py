"""Small JSON CLI for the JobTracker access prototype."""

import argparse
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import sys


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(json.dumps({"error": message}), file=sys.stderr)
        raise SystemExit(2)


def main():
    parser = JsonArgumentParser()
    parser.add_argument("--db", required=True, type=Path)
    commands = parser.add_subparsers(dest="command", required=True, parser_class=JsonArgumentParser)
    save = commands.add_parser("save")
    save.add_argument("--key", required=True)
    save.add_argument("--file", required=True, type=Path)
    show = commands.add_parser("show")
    show.add_argument("--key", required=True)
    args = parser.parse_args()

    try:
        if not args.db.is_absolute():
            raise ValueError("database path must be absolute")
        if not args.key.strip():
            raise ValueError("key must not be empty")

        if args.command == "save":
            with args.file.open("r", encoding="utf-8", newline="") as source:
                content = source.read()
            with closing(sqlite3.connect(args.db)) as connection:
                with connection:
                    connection.execute("BEGIN IMMEDIATE")
                    connection.execute(
                        "CREATE TABLE IF NOT EXISTS records (key TEXT PRIMARY KEY, content TEXT NOT NULL)"
                    )
                    row = connection.execute(
                        "SELECT content FROM records WHERE key = ?", (args.key,)
                    ).fetchone()
                    if row and row[0] != content:
                        raise ValueError("key already has different content")
                    if row is None:
                        connection.execute(
                            "INSERT INTO records (key, content) VALUES (?, ?)",
                            (args.key, content),
                        )
            result = {"key": args.key, "existing": row is not None}
        else:
            with closing(sqlite3.connect(args.db.as_uri() + "?mode=ro", uri=True)) as connection:
                row = connection.execute(
                    "SELECT content FROM records WHERE key = ?", (args.key,)
                ).fetchone()
            if row is None:
                raise ValueError("key not found")
            result = {"key": args.key, "content": row[0]}

        print(json.dumps(result))
    except (OSError, UnicodeError, sqlite3.Error, ValueError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
