#!/usr/bin/env python3
"""Pack a clean Git/Cloudflare-ready archive (Astro source, no node_modules/dist)."""

import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_DIR = ROOT / "archive"
OUT_DIR = ARCHIVE_DIR / "git-repo"
OUT_ZIP = ARCHIVE_DIR / "onlinecasinoexperte-astro-git.zip"

INCLUDE_DIRS = ("src", "public", "scripts", "mirror", "reports")
INCLUDE_FILES = (
    ".gitignore",
    "astro.config.mjs",
    "cloudflare-pages.md",
    "package.json",
    "package-lock.json",
    "tsconfig.json",
    "wrangler.toml",
)

EXCLUDE_DIR_NAMES = {"node_modules", "dist", ".astro", ".git", "__pycache__"}
EXCLUDE_FILE_SUFFIXES = {".zip", ".log"}


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIR_NAMES:
        return True
    if path.suffix.lower() in EXCLUDE_FILE_SUFFIXES:
        return True
    return False


def copy_tree(src: Path, dst: Path) -> int:
    count = 0
    if src.is_file():
        if should_skip(src):
            return 0
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        return 1
    for item in src.rglob("*"):
        if not item.is_file() or should_skip(item):
            continue
        rel = item.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)
        count += 1
    return count


def write_notes() -> None:
    notes = ARCHIVE_DIR / "ARCHIVE-NOTES.txt"
    notes.write_text(
        """onlinecasinoexperte.org — archive notes
=========================================

onlinecasinoexperte-astro-git.zip / git-repo/
  Ready to push to GitHub -> Cloudflare Pages.
  Contains: src/, public/, scripts/, mirror/, reports/, configs.
  Does NOT contain: node_modules, dist, .tools (Cloudflare runs npm ci && npm run build).

wayback-versiya-vp.zip
  Full Wayback mirror backup (~31 MB). Keep locally, do not push to Git.

onlinecasinoexperte-wp-files.zip
  Old partial WP folders from root cleanup. Checked: mostly empty dirs +
  Wayback error stubs (145 KB placeholders), NOT needed. Real assets are in
  public/wp-content/ and mirror/wp-content/.

Cloudflare build:
  Command: npm ci && npm run build
  Output:  dist
  Node:    22
""",
        encoding="utf-8",
    )


def main() -> None:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir()

    total = 0
    for name in INCLUDE_DIRS:
        src = ROOT / name
        if src.is_dir():
            total += copy_tree(src, OUT_DIR / name)

    for name in INCLUDE_FILES:
        src = ROOT / name
        if src.is_file():
            shutil.copy2(src, OUT_DIR / name)
            total += 1

    if OUT_ZIP.exists():
        OUT_ZIP.unlink()
    with zipfile.ZipFile(OUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in OUT_DIR.rglob("*"):
            if path.is_file():
                zf.write(path, path.relative_to(OUT_DIR).as_posix())

    # Move loose WP zip into archive if still at root
    wp_root = ROOT / "onlinecasinoexperte wp files.zip"
    wp_archive = ARCHIVE_DIR / "onlinecasinoexperte-wp-files.zip"
    if wp_root.exists() and not wp_archive.exists():
        shutil.move(str(wp_root), str(wp_archive))

    write_notes()
    size_mb = OUT_ZIP.stat().st_size / 1024 / 1024
    print(f"Packed {total} files")
    print(f"Folder: {OUT_DIR}")
    print(f"Zip:    {OUT_ZIP} ({size_mb:.1f} MB)")
    print(f"Notes:  {ARCHIVE_DIR / 'ARCHIVE-NOTES.txt'}")


if __name__ == "__main__":
    main()
