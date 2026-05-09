#!/usr/bin/env python3
"""
Replaces commas with semicolons in the 'quellen:' frontmatter field
in all .md files found recursively under a given folder.

The quellen field looks like:
    quellen: Source A|https://..., Source B|https://..., Source C|https://...

And will be converted to:
    quellen: Source A|https://...; Source B|https://...; Source C|https://...

Usage:
    python fix_quellen.py <folder>
    python fix_quellen.py <folder> --dry-run   # preview changes without writing
"""

import re
import sys
import argparse
from pathlib import Path


# Matches the quellen line inside YAML frontmatter.
QUELLEN_RE = re.compile(r'^(quellen:\s*)(.+)$', re.MULTILINE | re.IGNORECASE)


def fix_quellen(text: str) -> tuple[str, int]:
    """Replace commas with semicolons on the quellen: line. Returns (new_text, n_replaced)."""
    n_replaced = 0

    def replacer(match):
        nonlocal n_replaced
        prefix, value = match.group(1), match.group(2)
        new_value = value.replace(',', ';')
        n_replaced += value.count(',')
        return prefix + new_value

    new_text = QUELLEN_RE.sub(replacer, text)
    return new_text, n_replaced


def process_folder(folder: Path, dry_run: bool = False):
    md_files = list(folder.rglob('*.md'))

    if not md_files:
        print(f"No .md files found under: {folder}")
        return

    total_files_changed = 0
    total_commas_replaced = 0

    for path in sorted(md_files):
        original = path.read_text(encoding='utf-8')
        updated, n_changes = fix_quellen(original)

        if updated == original:
            print(f"  [skip]    {path.relative_to(folder)}  (no quellen field with commas)")
            continue

        total_files_changed += 1
        total_commas_replaced += n_changes

        if dry_run:
            print(f"  [dry-run] {path.relative_to(folder)}  ({n_changes} comma(s) would be replaced)")
        else:
            path.write_text(updated, encoding='utf-8')
            print(f"  [updated] {path.relative_to(folder)}  ({n_changes} comma(s) replaced)")

    print()
    if dry_run:
        print(f"Dry run complete. {total_files_changed} file(s) would be updated, "
              f"{total_commas_replaced} comma(s) would be replaced.")
    else:
        print(f"Done. {total_files_changed} file(s) updated, "
              f"{total_commas_replaced} comma(s) replaced.")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('folder', help='Root folder to search for .md files')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without writing files')
    args = parser.parse_args()

    folder = Path(args.folder).resolve()
    if not folder.is_dir():
        print(f"Error: '{folder}' is not a directory.")
        sys.exit(1)

    print(f"{'[DRY RUN] ' if args.dry_run else ''}Scanning: {folder}\n")
    process_folder(folder, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
