"""Validate and optionally normalize the repository documentation foundation."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIRECTORIES = {".git", ".idea", ".venv", "__pycache__", "node_modules"}
TEXT_NAMES = {
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
    ".python-version",
    "LICENSE",
    "Makefile",
}
TEXT_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml", ".txt"}
REQUIRED_FILES = {
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
    ".github/CODEOWNERS",
    ".github/ISSUE_TEMPLATE/work-item.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/validate.yml",
    "AGENTS.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "Makefile",
    "README.md",
    "SECURITY.md",
    "docs/architecture/overview.md",
    "docs/decisions/README.md",
    "docs/development/dependency-policy.md",
    "docs/development/developer-quickstart.md",
    "docs/development/engineering-standards.md",
    "docs/development/sql-migrations.md",
    "docs/product/product-definition.md",
    "docs/roadmap/milestones.md",
}
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
ADR_PATTERN = re.compile(r"^\d{4}-[a-z0-9-]+\.md$")
MILESTONE_PATTERN = re.compile(r"^## (M\d{2} - .+)$", re.MULTILINE)


def repository_files(root: Path) -> list[Path]:
    """Return supported repository text files in deterministic order."""
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or any(part in IGNORED_DIRECTORIES for part in path.parts):
            continue
        if path.name in TEXT_NAMES or path.suffix.lower() in TEXT_SUFFIXES:
            files.append(path)
    return sorted(files, key=lambda item: item.as_posix())


def normalize(data: bytes) -> bytes:
    """Return UTF-8 bytes with LF endings, no trailing spaces, and one final newline."""
    text = data.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip(" \t") for line in text.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return ("\n".join(lines) + "\n").encode("utf-8")


def validate_text(path: Path, data: bytes) -> list[str]:
    """Return encoding and canonical-text errors for one file."""
    errors: list[str] = []
    try:
        canonical = normalize(data)
    except UnicodeDecodeError as error:
        return [f"{path}: is not valid UTF-8: {error}"]
    if data != canonical:
        errors.append(f"{path}: text is not canonical; run make fmt")
    return errors


def resolve_link(markdown: Path, target: str, root: Path) -> Path | None:
    """Resolve a repository-local Markdown link or return None for external links."""
    target = target.strip().strip("<>")
    if not target or target.startswith("#"):
        return None
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
        return None
    path_text = unquote(target.split("#", 1)[0])
    if not path_text:
        return None
    candidate = (root / path_text.lstrip("/")) if path_text.startswith("/") else (markdown.parent / path_text)
    return candidate.resolve()


def validate_markdown(path: Path, text: str, root: Path) -> list[str]:
    """Return TL;DR and repository-local link errors for one Markdown file."""
    errors: list[str] = []
    relative = path.relative_to(root).as_posix()
    if len(text.splitlines()) >= 80 and "## TL;DR" not in text.splitlines()[:25]:
        errors.append(f"{relative}: long document lacks an early ## TL;DR section")
    for target in LINK_PATTERN.findall(text):
        resolved = resolve_link(path, target, root)
        if resolved is None:
            continue
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            errors.append(f"{relative}: link escapes repository: {target}")
            continue
        if not resolved.exists():
            errors.append(f"{relative}: missing link target: {target}")
    return errors


def validate_decisions(root: Path) -> list[str]:
    """Ensure every numbered ADR is present in the decision index."""
    decisions = root / "docs" / "decisions"
    index = decisions / "README.md"
    if not index.exists():
        return []
    index_text = index.read_text(encoding="utf-8")
    errors: list[str] = []
    for path in sorted(decisions.glob("*.md")):
        if ADR_PATTERN.match(path.name) and f"({path.name})" not in index_text:
            errors.append(f"docs/decisions/{path.name}: missing from ADR index")
    return errors


def validate_milestones(root: Path) -> list[str]:
    """Validate unique, contiguous milestone headings beginning with M01."""
    path = root / "docs" / "roadmap" / "milestones.md"
    if not path.exists():
        return []
    headings = MILESTONE_PATTERN.findall(path.read_text(encoding="utf-8"))
    numbers = [int(heading[1:3]) for heading in headings]
    expected = list(range(1, len(numbers) + 1))
    if numbers != expected:
        return [f"docs/roadmap/milestones.md: milestone headings must be unique and contiguous from M01; got {numbers}"]
    return []


def validate_repository(root: Path) -> list[str]:
    """Return every repository-foundation validation error."""
    errors = [f"missing required file: {name}" for name in sorted(REQUIRED_FILES) if not (root / name).is_file()]
    forbidden_vendor = "i" + "lert"
    for path in repository_files(root):
        relative = path.relative_to(root).as_posix()
        data = path.read_bytes()
        errors.extend(validate_text(Path(relative), data))
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError:
            continue
        if forbidden_vendor in text.casefold():
            errors.append(f"{relative}: vendor-specific market research must remain outside this repository")
        if path.suffix.lower() == ".md":
            errors.extend(validate_markdown(path, text, root))
    errors.extend(validate_decisions(root))
    errors.extend(validate_milestones(root))
    return errors


def format_repository(root: Path) -> None:
    """Normalize every supported text file in place."""
    for path in repository_files(root):
        original = path.read_bytes()
        canonical = normalize(original)
        if original != canonical:
            path.write_bytes(canonical)


def main() -> int:
    """Run repository validation and return a process exit code."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fix", action="store_true", help="normalize supported text before validating")
    args = parser.parse_args()
    if args.fix:
        format_repository(ROOT)
    errors = validate_repository(ROOT)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("documentation foundation is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
