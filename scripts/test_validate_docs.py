"""Tests for the repository documentation validator."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import validate_docs


class NormalizeTests(unittest.TestCase):
    def test_normalize_rewrites_bom_crlf_trailing_space_and_final_newlines(self) -> None:
        source = b"\xef\xbb\xbffirst  \r\nsecond\r\n\r\n"

        self.assertEqual(validate_docs.normalize(source), b"first\nsecond\n")

    def test_validate_text_rejects_noncanonical_bytes(self) -> None:
        self.assertEqual(
            validate_docs.validate_text(Path("README.md"), b"content"),
            ["README.md: text is not canonical; run make fmt"],
        )


class MarkdownTests(unittest.TestCase):
    def test_missing_local_link_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "README.md"
            path.write_text("[missing](docs/missing.md)\n", encoding="utf-8")

            errors = validate_docs.validate_markdown(path, path.read_text(encoding="utf-8"), root)

            self.assertEqual(errors, ["README.md:1: missing link target: docs/missing.md"])

    def test_external_and_existing_anchor_links_are_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "README.md"
            text = "# Section\n\n[web](https://example.com) [section](#section)\n"
            path.write_text(text, encoding="utf-8")

            self.assertEqual(validate_docs.validate_markdown(path, text, root), [])

    def test_missing_anchor_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "README.md"
            path.write_text("# Existing\n\n[missing](#not-here)\n", encoding="utf-8")

            self.assertEqual(
                validate_docs.validate_markdown(path, path.read_text(encoding="utf-8"), root),
                ["README.md:3: missing Markdown anchor: #not-here"],
            )

    def test_reference_definition_target_is_validated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "README.md"
            path.write_text("[guide][missing]\n\n[missing]: docs/missing.md\n", encoding="utf-8")

            self.assertEqual(
                validate_docs.validate_markdown(path, path.read_text(encoding="utf-8"), root),
                ["README.md:3: missing link target: docs/missing.md"],
            )

    def test_links_in_fenced_examples_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "README.md"
            text = "```markdown\n[example](missing.md)\n```\n"

            self.assertEqual(validate_docs.validate_markdown(path, text, root), [])

    def test_inline_link_title_does_not_become_part_of_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            guide = root / "guide.md"
            guide.write_text("# Guide\n", encoding="utf-8")
            path = root / "README.md"
            text = '[guide](guide.md "Developer guide")\n'

            self.assertEqual(validate_docs.validate_markdown(path, text, root), [])

    def test_long_document_requires_early_summary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "long.md"
            text = "# Long\n" + "line\n" * 79

            self.assertIn(
                "long.md: long document lacks an early ## TL;DR section",
                validate_docs.validate_markdown(path, text, root),
            )


class RoadmapTests(unittest.TestCase):
    def test_milestones_must_be_contiguous(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "docs" / "roadmap" / "milestones.md"
            path.parent.mkdir(parents=True)
            path.write_text("## M01 - One\n## M03 - Three\n", encoding="utf-8")

            self.assertEqual(
                validate_docs.validate_milestones(root),
                ["docs/roadmap/milestones.md: milestone headings must be unique and contiguous from M01; got [1, 3]"],
            )


class DecisionTests(unittest.TestCase):
    def test_index_drift_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            decisions = root / "docs" / "decisions"
            decisions.mkdir(parents=True)
            (decisions / "0001-choice.md").write_text(
                "# ADR-0001: Choice\n\n"
                "- Status: Accepted\n"
                "- Date: 2026-09-29\n"
                "- Milestone: M01 - Foundation\n"
                "- Deciders: Maintainers\n"
                "- Supersedes: None\n"
                "- Superseded by: None\n",
                encoding="utf-8",
            )
            (decisions / "README.md").write_text(
                "| ADR | Decision | Status | Date |\n"
                "|:--|:--|:--|:--|\n"
                "| [ADR-0001](0001-choice.md) | Stale title | Accepted | 2026-09-29 |\n",
                encoding="utf-8",
            )

            self.assertEqual(
                validate_docs.validate_decisions(root),
                ["docs/decisions/README.md: ADR-0001 row does not match its file title, status, date, and link"],
            )

    def test_duplicate_metadata_and_index_rows_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            decisions = root / "docs" / "decisions"
            decisions.mkdir(parents=True)
            (decisions / "0001-choice.md").write_text(
                "# ADR-0001: Choice\n\n"
                "- Status: Proposed\n"
                "- Status: Accepted\n"
                "- Date: 2026-09-29\n"
                "- Milestone: M01 - Foundation\n"
                "- Deciders: Maintainers\n"
                "- Supersedes: None\n"
                "- Superseded by: None\n",
                encoding="utf-8",
            )
            row = "| [ADR-0001](0001-choice.md) | Choice | Accepted | 2026-09-29 |\n"
            (decisions / "README.md").write_text(row + row, encoding="utf-8")

            errors = validate_docs.validate_decisions(root)

            self.assertTrue(any("duplicate ADR metadata 'Status'" in error for error in errors))
            self.assertTrue(any("duplicate ADR-0001 index row" in error for error in errors))


class TemplateTests(unittest.TestCase):
    def test_issue_template_drift_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            issue = root / ".github" / "ISSUE_TEMPLATE" / "work-item.md"
            pull_request = root / ".github" / "PULL_REQUEST_TEMPLATE.md"
            issue.parent.mkdir(parents=True)
            pull_request.parent.mkdir(parents=True, exist_ok=True)
            body = "\n\n".join(f"## {heading}\n\nText" for heading in validate_docs.ISSUE_HEADINGS)
            issue.write_text(body + "\n", encoding="utf-8")
            pull_request.write_text(
                "\n\n".join(f"## {heading}\n\nText" for heading in validate_docs.PR_HEADINGS)
                + "\n"
                + "\n".join(validate_docs.PR_PROMPTS)
                + "\n",
                encoding="utf-8",
            )
            (root / "CONTRIBUTING.md").write_text(
                "Every implementation issue uses this body:\n\n```markdown\nDifferent\n```\n",
                encoding="utf-8",
            )

            self.assertEqual(
                validate_docs.validate_templates(root),
                [".github/ISSUE_TEMPLATE/work-item.md: body differs from the canonical CONTRIBUTING.md issue body"],
            )

    def test_pull_request_heading_order_and_prompts_are_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            issue = root / ".github" / "ISSUE_TEMPLATE" / "work-item.md"
            pull_request = root / ".github" / "PULL_REQUEST_TEMPLATE.md"
            issue.parent.mkdir(parents=True)
            pull_request.parent.mkdir(parents=True, exist_ok=True)
            canonical = "\n\n".join(f"## {heading}\n\nText" for heading in validate_docs.ISSUE_HEADINGS)
            issue.write_text(canonical + "\n", encoding="utf-8")
            reordered = tuple(reversed(validate_docs.PR_HEADINGS))
            pull_request.write_text(
                "\n\n".join(f"## {heading}\n" for heading in reordered) + "\n",
                encoding="utf-8",
            )
            (root / "CONTRIBUTING.md").write_text(
                f"Every implementation issue uses this body:\n\n```markdown\n{canonical}\n```\n",
                encoding="utf-8",
            )

            errors = validate_docs.validate_templates(root)

            self.assertTrue(any("headings differ" in error for error in errors))
            self.assertTrue(any("missing required prompt" in error for error in errors))


class WorkflowTests(unittest.TestCase):
    def test_action_hash_is_rejected_but_local_action_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflow = root / ".github" / "workflows" / "validate.yml"
            workflow.parent.mkdir(parents=True)
            workflow.write_text(
                "steps:\n"
                "  - uses: ./actions/local\n"
                "  - uses: actions/checkout@0123456789abcdef\n",
                encoding="utf-8",
            )

            self.assertEqual(
                validate_docs.validate_action_references(root),
                [
                    ".github/workflows/validate.yml:3: GitHub Action must use a semantic major tag "
                    "such as @v7: actions/checkout@0123456789abcdef"
                ],
            )

    def test_quoted_actions_block_scalars_and_composite_actions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflow = root / ".github" / "workflows" / "validate.yml"
            composite = root / ".github" / "actions" / "example" / "action.yml"
            workflow.parent.mkdir(parents=True)
            composite.parent.mkdir(parents=True)
            workflow.write_text(
                "steps:\n"
                "  - uses: \"actions/checkout@v7\" # readable major\n"
                "  - run: |\n"
                "      echo 'uses: owner/not-an-action@abcdef'\n",
                encoding="utf-8",
            )
            composite.write_text(
                "runs:\n  using: composite\n  steps:\n    - uses: owner/action@abcdef\n",
                encoding="utf-8",
            )

            self.assertEqual(
                validate_docs.validate_action_references(root),
                [
                    ".github/actions/example/action.yml:4: GitHub Action must use a semantic major tag "
                    "such as @v7: owner/action@abcdef"
                ],
            )


if __name__ == "__main__":
    unittest.main()
