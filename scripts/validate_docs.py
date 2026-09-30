"""Validate and optionally normalize the repository documentation foundation."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
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
    "docs/README.md",
    "docs/architecture/overview.md",
    "docs/decisions/README.md",
    "docs/development/dependency-policy.md",
    "docs/development/developer-quickstart.md",
    "docs/development/engineering-standards.md",
    "docs/development/harness.md",
    "docs/development/sql-migrations.md",
    "docs/product/product-definition.md",
    "docs/roadmap/milestones.md",
}
INLINE_LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
REFERENCE_LINK_PATTERN = re.compile(r"^[ \t]{0,3}\[[^\]]+\]:[ \t]*(?:<([^>]+)>|(\S+))", re.MULTILINE)
HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
ADR_PATTERN = re.compile(r"^(\d{4})-([a-z0-9-]+)\.md$")
ADR_HEADER_PATTERN = re.compile(r"^# ADR-(\d{4}): (.+)$")
MILESTONE_PATTERN = re.compile(r"^## (M\d{2} - .+)$", re.MULTILINE)
ADR_STATUSES = {"Proposed", "Accepted", "Rejected", "Deprecated", "Superseded"}
ADR_METADATA = ("Status", "Date", "Milestone", "Deciders", "Supersedes", "Superseded by")
ISSUE_HEADINGS = ("Goal", "Scope", "Design decisions", "Acceptance criteria", "Out of scope")
PR_HEADINGS = (
    "Linked work",
    "Outcome and scope",
    "Design, compatibility, and operations",
    "Verification",
    "Limitations and review",
)
PR_PROMPTS = (
    "Issue:",
    "Milestone:",
    "Problem and resulting behavior:",
    "Boundaries and deliberate exclusions:",
    "Assumptions and unresolved questions:",
    "ADRs:",
    "Contract/API/schema effects:",
    "Security/privacy effects:",
    "Rollout and recovery:",
    "Commands and evidence:",
    "Checks not run, blocking conditions, and residual risk:",
    "Known limitations and follow-up:",
)
ACTION_USE_PATTERN = re.compile(r"^\s*(?:-\s*)?uses:\s*(.*?)\s*$")
YAML_BLOCK_SCALAR_PATTERN = re.compile(r"^\s*(?:-\s*)?[^:#]+:\s*[|>][+-]?\d*\s*(?:#.*)?$")
SEMANTIC_MAJOR_ACTION_PATTERN = re.compile(r"^[^@\s]+@v[1-9]\d*$")


@dataclass(frozen=True)
class MarkdownLink:
    """A repository-local link candidate and its source line."""

    target: str
    line: int


@dataclass(frozen=True)
class AdrRecord:
    """The index-relevant metadata parsed from one ADR."""

    number: str
    title: str
    status: str
    date: str
    filename: str


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
    try:
        canonical = normalize(data)
    except UnicodeDecodeError as error:
        return [f"{path}: is not valid UTF-8: {error}"]
    return [] if data == canonical else [f"{path}: text is not canonical; run make fmt"]


def markdown_without_fences(text: str) -> str:
    """Blank fenced-code content while preserving line numbers."""
    visible: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        stripped = line.lstrip()
        marker = stripped[:3]
        if fence is None and marker in {"```", "~~~"}:
            fence = marker
            visible.append("")
        elif fence is not None:
            if stripped.startswith(fence):
                fence = None
            visible.append("")
        else:
            visible.append(line)
    return "\n".join(visible)


def markdown_links(text: str) -> list[MarkdownLink]:
    """Return inline and reference-definition links outside fenced code."""
    visible = markdown_without_fences(text)
    links: list[MarkdownLink] = []
    for match in INLINE_LINK_PATTERN.finditer(visible):
        links.append(MarkdownLink(match.group(1), visible.count("\n", 0, match.start()) + 1))
    for match in REFERENCE_LINK_PATTERN.finditer(visible):
        links.append(MarkdownLink(match.group(1) or match.group(2), visible.count("\n", 0, match.start()) + 1))
    return links


def split_link_target(target: str) -> tuple[str, str]:
    """Return the decoded path and fragment portions of a Markdown link."""
    cleaned = target.strip()
    if cleaned.startswith("<") and ">" in cleaned:
        cleaned = cleaned[1 : cleaned.index(">")]
    else:
        cleaned = cleaned.split(maxsplit=1)[0] if cleaned else ""
    path_text, separator, fragment = cleaned.partition("#")
    return unquote(path_text), unquote(fragment) if separator else ""


def resolve_link(markdown: Path, target: str, root: Path) -> tuple[Path, str] | None:
    """Resolve a repository-local Markdown link and its optional anchor."""
    path_text, fragment = split_link_target(target)
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", path_text):
        return None
    if not path_text:
        return markdown.resolve(), fragment
    candidate = (root / path_text.lstrip("/")) if path_text.startswith("/") else (markdown.parent / path_text)
    return candidate.resolve(), fragment


def has_exact_path_case(path: Path, root: Path) -> bool:
    """Return whether every repository-relative path segment uses on-disk case."""
    try:
        relative = path.relative_to(root.resolve())
    except ValueError:
        return False
    current = root.resolve()
    for part in relative.parts:
        try:
            names = {child.name for child in current.iterdir()}
        except (FileNotFoundError, NotADirectoryError, PermissionError):
            return False
        if part not in names:
            return False
        current /= part
    return True


def github_anchor(text: str) -> str:
    """Return the GitHub-style base anchor for a Markdown heading."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[^\w\- ]", "", text.casefold(), flags=re.UNICODE)
    return text.replace(" ", "-")


def markdown_anchors(path: Path) -> set[str]:
    """Return anchors generated by headings in a Markdown document."""
    anchors: set[str] = set()
    occurrences: dict[str, int] = {}
    for line in markdown_without_fences(path.read_text(encoding="utf-8-sig")).splitlines():
        match = HEADING_PATTERN.match(line)
        if not match:
            continue
        base = github_anchor(match.group(1))
        count = occurrences.get(base, 0)
        anchors.add(base if count == 0 else f"{base}-{count}")
        occurrences[base] = count + 1
    return anchors


def validate_markdown(path: Path, text: str, root: Path) -> list[str]:
    """Return summary, local-link, case, and anchor errors for one Markdown file."""
    errors: list[str] = []
    relative = path.relative_to(root).as_posix()
    if len(text.splitlines()) >= 80 and "## TL;DR" not in text.splitlines()[:25]:
        errors.append(f"{relative}: long document lacks an early ## TL;DR section")
    for link in markdown_links(text):
        resolved_link = resolve_link(path, link.target, root)
        if resolved_link is None:
            continue
        resolved, fragment = resolved_link
        location = f"{relative}:{link.line}"
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            errors.append(f"{location}: link escapes repository: {link.target}")
            continue
        if not resolved.exists():
            errors.append(f"{location}: missing link target: {link.target}")
            continue
        if not has_exact_path_case(resolved, root):
            errors.append(f"{location}: link path has incorrect case: {link.target}")
            continue
        if fragment and resolved.suffix.casefold() == ".md" and fragment.casefold() not in markdown_anchors(resolved):
            errors.append(f"{location}: missing Markdown anchor: {link.target}")
    return errors


def parse_adr(path: Path, root: Path) -> tuple[AdrRecord | None, list[str]]:
    """Parse and validate identity and required metadata for one ADR."""
    relative = path.relative_to(root).as_posix()
    filename_match = ADR_PATTERN.match(path.name)
    if filename_match is None:
        return None, []
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    errors: list[str] = []
    header_match = ADR_HEADER_PATTERN.match(lines[0]) if lines else None
    if header_match is None:
        errors.append(f"{relative}: first line must be '# ADR-{filename_match.group(1)}: Decision title'")
        return None, errors
    if header_match.group(1) != filename_match.group(1):
        errors.append(f"{relative}: filename and ADR header numbers differ")
    metadata: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:12], start=2):
        match = re.match(r"^- ([^:]+):\s*(.*)$", line)
        if match:
            if match.group(1) in metadata:
                errors.append(f"{relative}:{line_number}: duplicate ADR metadata '{match.group(1)}'")
            metadata[match.group(1)] = match.group(2)
    for field in ADR_METADATA:
        if not metadata.get(field):
            errors.append(f"{relative}: missing ADR metadata '{field}'")
    status = metadata.get("Status", "")
    if status and status not in ADR_STATUSES:
        errors.append(f"{relative}: unsupported ADR status '{status}'")
    date = metadata.get("Date", "")
    if date and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        errors.append(f"{relative}: ADR date must use YYYY-MM-DD")
    return AdrRecord(filename_match.group(1), header_match.group(2), status, date, path.name), errors


def parse_adr_index(text: str) -> tuple[dict[str, AdrRecord], list[str]]:
    """Return indexed ADR rows and duplicate-row errors."""
    rows: dict[str, AdrRecord] = {}
    errors: list[str] = []
    pattern = re.compile(
        r"^\| \[ADR-(\d{4})\]\(([^)]+)\) \| ([^|]+?) \| ([^|]+?) \| ([^|]+?) \|$",
        re.MULTILINE,
    )
    for match in pattern.finditer(text):
        number, filename, title, status, date = (part.strip() for part in match.groups())
        if number in rows:
            line = text.count("\n", 0, match.start()) + 1
            errors.append(f"docs/decisions/README.md:{line}: duplicate ADR-{number} index row")
        rows[number] = AdrRecord(number, title, status, date, filename)
    return rows, errors


def validate_decisions(root: Path) -> list[str]:
    """Validate the ADR sequence, metadata, and exact index projection."""
    decisions = root / "docs" / "decisions"
    index = decisions / "README.md"
    if not index.exists():
        return []
    errors: list[str] = []
    records: list[AdrRecord] = []
    for path in sorted(decisions.glob("*.md")):
        record, record_errors = parse_adr(path, root)
        errors.extend(record_errors)
        if record is not None:
            records.append(record)
    numbers = [int(record.number) for record in records]
    expected = list(range(1, len(numbers) + 1))
    if numbers != expected:
        errors.append(f"docs/decisions: ADR numbers must be unique and contiguous from 0001; got {numbers}")
    indexed, index_errors = parse_adr_index(index.read_text(encoding="utf-8-sig"))
    errors.extend(index_errors)
    for record in records:
        row = indexed.get(record.number)
        if row is None:
            errors.append(f"docs/decisions/{record.filename}: missing from ADR index")
        elif row != record:
            errors.append(f"docs/decisions/README.md: ADR-{record.number} row does not match its file title, status, date, and link")
    for number in sorted(indexed.keys() - {record.number for record in records}):
        errors.append(f"docs/decisions/README.md: ADR-{number} has no numbered ADR file")
    return errors


def validate_milestones(root: Path) -> list[str]:
    """Validate unique, contiguous milestone headings beginning with M01."""
    path = root / "docs" / "roadmap" / "milestones.md"
    if not path.exists():
        return []
    headings = MILESTONE_PATTERN.findall(path.read_text(encoding="utf-8-sig"))
    numbers = [int(heading[1:3]) for heading in headings]
    expected = list(range(1, len(numbers) + 1))
    if numbers != expected:
        return [f"docs/roadmap/milestones.md: milestone headings must be unique and contiguous from M01; got {numbers}"]
    return []


def markdown_headings(text: str) -> tuple[str, ...]:
    """Return ordered level-two heading text outside fenced code."""
    return tuple(line[3:].strip() for line in markdown_without_fences(text).splitlines() if line.startswith("## "))


def issue_body(text: str) -> str:
    """Remove optional YAML front matter from an issue template."""
    if not text.startswith("---\n"):
        return text.strip()
    end = text.find("\n---\n", 4)
    return text[end + 5 :].strip() if end >= 0 else text.strip()


def canonical_issue_body(contributing: str) -> str | None:
    """Extract the canonical fenced issue body from CONTRIBUTING.md."""
    marker = "Every implementation issue uses this body:"
    start = contributing.find(marker)
    if start < 0:
        return None
    match = re.search(r"```markdown\n(.*?)\n```", contributing[start:], re.DOTALL)
    return match.group(1).strip() if match else None


def validate_templates(root: Path) -> list[str]:
    """Keep issue and pull-request templates aligned with contributor policy."""
    issue_path = root / ".github" / "ISSUE_TEMPLATE" / "work-item.md"
    pull_request_path = root / ".github" / "PULL_REQUEST_TEMPLATE.md"
    contributing_path = root / "CONTRIBUTING.md"
    if not issue_path.exists() or not pull_request_path.exists() or not contributing_path.exists():
        return []
    errors: list[str] = []
    issue_text = issue_path.read_text(encoding="utf-8-sig")
    issue_headings = markdown_headings(issue_text)
    if issue_headings != ISSUE_HEADINGS:
        errors.append(".github/ISSUE_TEMPLATE/work-item.md: level-two headings differ from canonical order")
    canonical = canonical_issue_body(contributing_path.read_text(encoding="utf-8-sig"))
    if canonical is None:
        errors.append("CONTRIBUTING.md: canonical implementation-issue body is missing")
    elif issue_body(issue_text) != canonical:
        errors.append(".github/ISSUE_TEMPLATE/work-item.md: body differs from the canonical CONTRIBUTING.md issue body")
    pull_request_text = pull_request_path.read_text(encoding="utf-8-sig")
    pull_request_headings = markdown_headings(pull_request_text)
    if pull_request_headings != PR_HEADINGS:
        errors.append(".github/PULL_REQUEST_TEMPLATE.md: level-two headings differ from canonical order")
    for prompt in PR_PROMPTS:
        if prompt not in pull_request_text:
            errors.append(f".github/PULL_REQUEST_TEMPLATE.md: missing required prompt '{prompt}'")
    return errors


def yaml_action_references(text: str) -> list[tuple[str, int]]:
    """Return actual YAML uses values while ignoring block-scalar content."""
    references: list[tuple[str, int]] = []
    block_indent: int | None = None
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip(" ")
        indent = len(line) - len(stripped)
        if block_indent is not None:
            if not stripped or indent > block_indent:
                continue
            block_indent = None
        if YAML_BLOCK_SCALAR_PATTERN.match(line):
            block_indent = indent
            continue
        match = ACTION_USE_PATTERN.match(line)
        if not match:
            continue
        raw = match.group(1).strip()
        if raw.startswith(('"', "'")):
            quote = raw[0]
            closing = raw.find(quote, 1)
            reference = raw[1:closing] if closing >= 0 else raw
        else:
            reference = raw.split("#", 1)[0].strip()
        references.append((reference, line_number))
    return references


def validate_action_references(root: Path) -> list[str]:
    """Require third-party GitHub Actions to use readable semantic major tags."""
    workflows = root / ".github" / "workflows"
    actions = root / ".github" / "actions"
    paths: set[Path] = set()
    if workflows.exists():
        paths.update((*workflows.glob("*.yml"), *workflows.glob("*.yaml")))
    if actions.exists():
        paths.update((*actions.rglob("action.yml"), *actions.rglob("action.yaml")))
    errors: list[str] = []
    for path in sorted(paths):
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8-sig")
        for reference, line in yaml_action_references(text):
            if reference.startswith(("./", "docker://")) or SEMANTIC_MAJOR_ACTION_PATTERN.fullmatch(reference):
                continue
            errors.append(
                f"{relative}:{line}: GitHub Action must use a semantic major tag such as @v7: {reference}"
            )
    return errors


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
    errors.extend(validate_templates(root))
    errors.extend(validate_action_references(root))
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
