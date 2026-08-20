#!/usr/bin/env python3
"""Create a deterministic ZIP and SHA-256 manifest without executing case files."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path, PurePosixPath
import stat
import sys
import zipfile


MANIFEST_NAME = "PACKAGE_SHA256SUMS.txt"
CHUNK_SIZE = 1024 * 1024


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Package a reviewed evidence directory as bytes without executing content."
    )
    parser.add_argument("case_dir", type=Path, help="Reviewed case directory to package")
    parser.add_argument("output_zip", type=Path, help="New .zip file to create")
    return parser.parse_args()


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def collect_files(root: Path) -> list[tuple[Path, str]]:
    files: list[tuple[Path, str]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        mode = os.lstat(path).st_mode
        if stat.S_ISLNK(mode):
            raise ValueError(f"Refusing symlink: {path}")
        if stat.S_ISDIR(mode):
            continue
        if not stat.S_ISREG(mode):
            raise ValueError(f"Refusing non-regular file: {path}")
        relative = PurePosixPath(path.relative_to(root).as_posix()).as_posix()
        if relative == MANIFEST_NAME:
            continue
        files.append((path, relative))
    return files


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(CHUNK_SIZE):
            digest.update(chunk)
    return digest.hexdigest()


def zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    info.create_system = 3
    return info


def write_file(archive: zipfile.ZipFile, source: Path, name: str) -> None:
    with source.open("rb") as source_handle, archive.open(zip_info(name), "w") as dest:
        while chunk := source_handle.read(CHUNK_SIZE):
            dest.write(chunk)


def main() -> int:
    args = parse_args()
    root = args.case_dir.expanduser().resolve(strict=True)
    output = args.output_zip.expanduser().resolve(strict=False)

    if not root.is_dir():
        raise ValueError(f"Case path is not a directory: {root}")
    if output.suffix.lower() != ".zip":
        raise ValueError("Output filename must end in .zip")
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite existing file: {output}")
    if is_within(output, root):
        raise ValueError("Output ZIP must be outside the case directory")

    output.parent.mkdir(parents=True, exist_ok=True)
    files = collect_files(root)
    if not files:
        raise ValueError("Case directory contains no regular files")

    manifest_lines = [f"{sha256_file(path)}  {name}" for path, name in files]
    manifest = ("\n".join(manifest_lines) + "\n").encode("utf-8")

    try:
        with zipfile.ZipFile(output, "x", allowZip64=True) as archive:
            for path, name in files:
                write_file(archive, path, name)
            archive.writestr(zip_info(MANIFEST_NAME), manifest)
    except Exception:
        if output.exists():
            output.unlink()
        raise

    print(f"Created: {output}")
    print(f"Files: {len(files)} plus {MANIFEST_NAME}")
    print(f"SHA-256: {sha256_file(output)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
