"""Import a JSONL corpus file into the segments table.

Usage:
    python -m scripts.import_corpus data/arbres-kenstur.jsonl
    python -m scripts.import_corpus data/arbres-kenstur.jsonl --source "arbres-kenstur"
    python -m scripts.import_corpus data/arbres-kenstur.jsonl --source "arbres-kenstur" --replace

Expected JSONL format (one object per line):
    {"translation": {"br": "Demat", "fr": "Bonjour"}}
"""

import argparse
import json
import sys
from pathlib import Path

from sqlalchemy import delete, select

from backend.app.database import SessionLocal, init_db
from backend.app.models import Segment

BATCH_SIZE = 500


def import_corpus(filepath: Path, source: str, *, replace: bool = False) -> None:
    """Read *filepath* and insert each line as a Segment."""
    init_db()
    db = SessionLocal()

    # --- purge existing segments for this source if --replace -----------
    if replace:
        deleted = db.execute(
            delete(Segment).where(Segment.source == source)
        ).rowcount
        db.commit()
        print(f"🗑  {deleted} segments supprimés (source={source!r})")

    inserted = 0
    skipped = 0
    errors = 0

    try:
        with filepath.open(encoding="utf-8") as fh:
            for lineno, raw_line in enumerate(fh, start=1):
                raw_line = raw_line.strip()
                if not raw_line:
                    continue

                # --- parse ------------------------------------------------
                try:
                    obj = json.loads(raw_line)
                    translation = obj["translation"]
                    breton = translation["br"]
                    francais = translation["fr"]
                except (json.JSONDecodeError, KeyError, TypeError) as exc:
                    print(f"  ⚠  ligne {lineno} ignorée ({exc})")
                    errors += 1
                    continue

                # --- duplicate check -------------------------------------
                exists = db.execute(
                    select(Segment.id).where(
                        Segment.breton == breton,
                        Segment.francais == francais,
                        Segment.source == source,
                    )
                ).first()

                if exists:
                    skipped += 1
                    continue

                # --- insert -----------------------------------------------
                db.add(Segment(breton=breton, francais=francais, source=source))
                inserted += 1

                if inserted % BATCH_SIZE == 0:
                    db.commit()
                    print(f"  … {inserted} segments insérés", end="\r")

        db.commit()
    finally:
        db.close()

    print(f"✅  Terminé — {filepath.name} (source={source!r})")
    print(f"   {inserted:>6} insérés")
    print(f"   {skipped:>6} doublons ignorés")
    if errors:
        print(f"   {errors:>6} lignes en erreur")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Importer un fichier JSONL dans la table segments.",
    )
    parser.add_argument(
        "file",
        type=Path,
        help="Chemin vers le fichier .jsonl",
    )
    parser.add_argument(
        "--source",
        default=None,
        help="Nom du corpus source (défaut : nom du fichier sans extension)",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Supprimer les segments existants de cette source avant import",
    )
    args = parser.parse_args()

    if not args.file.is_file():
        print(f"❌  Fichier introuvable : {args.file}", file=sys.stderr)
        sys.exit(1)

    source = args.source if args.source else args.file.stem
    import_corpus(args.file, source, replace=args.replace)


if __name__ == "__main__":
    main()
