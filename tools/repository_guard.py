#!/usr/bin/env python3
"""Scan this repository for local paths, secrets, and forbidden terms."""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

SKIPPED_DIRECTORIES = {
    ".git",
    ".kiro",
    ".local",
    ".mypy_cache",
    ".nox",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "ENV",
    "__pycache__",
    "env",
    "htmlcov",
    "node_modules",
    "venv",
}

BINARY_SUFFIXES = {
    ".7z",
    ".bmp",
    ".class",
    ".dll",
    ".dylib",
    ".exe",
    ".gif",
    ".ico",
    ".jar",
    ".jpeg",
    ".jpg",
    ".o",
    ".obj",
    ".pdf",
    ".png",
    ".pyc",
    ".so",
    ".webp",
}

ARCHIVE_SUFFIXES = (
    ".tar",
    ".tar.bz2",
    ".tar.gz",
    ".tar.xz",
    ".tgz",
    ".zip",
)

LOCAL_PATH_PATTERNS = (
    re.compile(r"(?<![\w])/(?:Users|home)/[^/\s\"'`<>]+(?:/[^\s\"'`<>)]*)?"),
    re.compile(r"(?i)\b[A-Z]:[\\/]+Users[\\/]+[^\\/\s\"'`<>]+"),
)

PRIVATE_KEY_PATTERN = re.compile(
    r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"
)

CREDENTIAL_ASSIGNMENT_PATTERN = re.compile(
    r"(?i)(?P<name>(?:api[_-]?key|api[_-]?token|access[_-]?key|access[_-]?token|"
    r"auth[_-]?token|client[_-]?secret|secret(?:[_-]?key)?|password|passwd|"
    r"aws[_-]?secret[_-]?access[_-]?key))\s*[=:]\s*(?P<value>[^\s,;#]+)"
)

PROVIDER_TOKEN_PATTERNS = (
    re.compile(r"^gh[pousr]_[A-Za-z0-9_]{20,}$"),
    re.compile(r"^github_pat_[A-Za-z0-9_]{20,}$"),
    re.compile(r"^sk-(?:live|proj)-[A-Za-z0-9_-]{16,}$"),
    re.compile(r"^AKIA[0-9A-Z]{16}$"),
    re.compile(r"^xox[baprs]-[A-Za-z0-9-]{16,}$"),
)

PLACEHOLDER_MARKERS = (
    "<redacted>",
    "<secret>",
    "<token>",
    "changeme",
    "example",
    "placeholder",
    "redacted",
    "your-",
    "your_",
)


@dataclass(frozen=True)
class Finding:
    category: str
    path: str
    line: int | None
    message: str


@dataclass
class ScanResult:
    scanned_files: int = 0
    excluded_files: int = 0
    excluded_directories: int = 0
    findings: list[Finding] | None = None

    def __post_init__(self) -> None:
        if self.findings is None:
            self.findings = []


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Scan repository paths and UTF-8 text for local user paths, private keys, "
            "likely credentials, and configurable forbidden terms."
        )
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=REPOSITORY_ROOT,
        help="Repository root to scan. Defaults to the repository containing this tool.",
    )
    parser.add_argument(
        "--forbidden-term",
        action="append",
        default=[],
        help="Term to reject in paths and UTF-8 text. Repeat for multiple terms.",
    )
    parser.add_argument(
        "--denylist",
        type=Path,
        help="Optional UTF-8 file containing one forbidden term per line.",
    )
    return parser.parse_args(argv)


def read_denylist(path: Path) -> list[str]:
    terms: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        term = raw_line.strip()
        if term and not term.startswith("#"):
            terms.append(term)
    return terms


def collect_forbidden_terms(
    root: Path, command_line_terms: Iterable[str], denylist: Path | None
) -> tuple[list[str], set[Path]]:
    terms = [term.strip() for term in command_line_terms if term.strip()]
    excluded_files: set[Path] = set()

    auto_denylist = root / ".local" / "forbidden-terms.txt"
    denylist_paths = [auto_denylist] if auto_denylist.exists() else []
    if denylist is not None:
        explicit = denylist.expanduser().resolve()
        if not explicit.is_file():
            raise ValueError("the configured denylist does not exist or is not a file")
        denylist_paths.append(explicit)

    for path in denylist_paths:
        resolved = path.resolve()
        try:
            terms.extend(read_denylist(resolved))
        except (OSError, UnicodeError) as exc:
            raise ValueError(f"cannot read a configured denylist: {exc.__class__.__name__}") from exc
        excluded_files.add(resolved)

    unique: dict[str, str] = {}
    for term in terms:
        if "\n" in term or "\r" in term:
            raise ValueError("forbidden terms must be single-line values")
        unique.setdefault(term.casefold(), term)
    return list(unique.values()), excluded_files


def is_generated_archive(path: Path) -> bool:
    return path.name.casefold().endswith(ARCHIVE_SUFFIXES)


def is_known_binary(path: Path) -> bool:
    return path.suffix.casefold() in BINARY_SUFFIXES


def matching_forbidden_term(value: str, terms: Sequence[str]) -> str | None:
    folded = value.casefold()
    for term in terms:
        if term.casefold() in folded:
            return term
    return None


def redact_path(path: str, terms: Sequence[str]) -> str:
    redacted = path
    for term in sorted(terms, key=len, reverse=True):
        redacted = re.sub(re.escape(term), "<redacted>", redacted, flags=re.IGNORECASE)
    return redacted


def normalize_assigned_value(raw_value: str) -> str:
    value = raw_value.strip().strip("\"'").rstrip(",;")
    return value


def is_likely_secret(value: str) -> bool:
    if not value:
        return False
    folded = value.casefold()
    if (
        folded in {"none", "null", "true", "false", "...", "xxx"}
        or folded.startswith("${")
        or folded.startswith("$(")
        or value.startswith("$")
        or (value.startswith("<") and value.endswith(">"))
        or any(marker in folded for marker in PLACEHOLDER_MARKERS)
    ):
        return False
    if any(pattern.fullmatch(value) for pattern in PROVIDER_TOKEN_PATTERNS):
        return True
    if len(value) < 20 or re.search(r"\s", value):
        return False
    if not re.fullmatch(r"[A-Za-z0-9_./+=:@-]+", value):
        return False
    has_letter = bool(re.search(r"[A-Za-z]", value))
    has_digit = bool(re.search(r"\d", value))
    diversity = len(set(value)) / len(value)
    return has_letter and has_digit and diversity >= 0.30


def inspect_text(path: str, text: str, terms: Sequence[str]) -> list[Finding]:
    findings: list[Finding] = []
    forbidden_reported = False
    local_path_reported = False
    private_key_reported = False
    credential_reported = False

    for line_number, line in enumerate(text.splitlines(), start=1):
        if not forbidden_reported and matching_forbidden_term(line, terms):
            findings.append(Finding("forbidden-term", path, line_number, "forbidden term in text"))
            forbidden_reported = True

        if not local_path_reported and any(pattern.search(line) for pattern in LOCAL_PATH_PATTERNS):
            findings.append(Finding("local-path", path, line_number, "absolute local user path"))
            local_path_reported = True

        if not private_key_reported and PRIVATE_KEY_PATTERN.search(line):
            findings.append(Finding("private-key", path, line_number, "private-key material"))
            private_key_reported = True

        if not credential_reported:
            for match in CREDENTIAL_ASSIGNMENT_PATTERN.finditer(line):
                if is_likely_secret(normalize_assigned_value(match.group("value"))):
                    findings.append(
                        Finding("credential", path, line_number, "likely credential assignment")
                    )
                    credential_reported = True
                    break

    return findings


def scan_repository(root: Path, terms: Sequence[str], denylist_files: set[Path]) -> ScanResult:
    result = ScanResult()
    root = root.resolve()

    for current, directory_names, file_names in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        kept_directories: list[str] = []
        for name in sorted(directory_names):
            child = current_path / name
            if name in SKIPPED_DIRECTORIES or child.is_symlink():
                result.excluded_directories += 1
                continue
            relative = child.relative_to(root).as_posix()
            if matching_forbidden_term(relative, terms):
                result.findings.append(
                    Finding("forbidden-term", redact_path(relative, terms), None, "forbidden term in path")
                )
            kept_directories.append(name)
        directory_names[:] = kept_directories

        for name in sorted(file_names):
            path = current_path / name
            relative = path.relative_to(root).as_posix()

            if (
                path.is_symlink()
                or path.resolve() in denylist_files
                or is_generated_archive(path)
                or is_known_binary(path)
            ):
                result.excluded_files += 1
                continue

            if matching_forbidden_term(relative, terms):
                result.findings.append(
                    Finding("forbidden-term", redact_path(relative, terms), None, "forbidden term in path")
                )

            try:
                data = path.read_bytes()
            except OSError:
                result.findings.append(Finding("read-error", relative, None, "file could not be read"))
                continue

            if b"\x00" in data:
                result.excluded_files += 1
                continue
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                result.excluded_files += 1
                continue

            result.scanned_files += 1
            result.findings.extend(inspect_text(relative, text, terms))

    return result


def print_result(result: ScanResult) -> None:
    for finding in result.findings:
        location = finding.path
        if finding.line is not None:
            location = f"{location}:{finding.line}"
        print(f"ERROR [{finding.category}] {location}: {finding.message}")

    print(f"Files scanned: {result.scanned_files}")
    print(f"Files excluded: {result.excluded_files}")
    print(f"Directories excluded: {result.excluded_directories}")
    print(f"Errors: {len(result.findings)}")
    if result.findings:
        print("Repository guard: FAILED")
    else:
        print("Repository guard: OK")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        print("Repository guard configuration error: scan root is not a directory", file=sys.stderr)
        return 2

    try:
        terms, denylist_files = collect_forbidden_terms(root, args.forbidden_term, args.denylist)
    except ValueError as exc:
        print(f"Repository guard configuration error: {exc}", file=sys.stderr)
        return 2

    result = scan_repository(root, terms, denylist_files)
    print_result(result)
    return 1 if result.findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
