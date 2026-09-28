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

            self.assertEqual(errors, ["README.md: missing link target: docs/missing.md"])

    def test_external_and_anchor_links_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "README.md"
            text = "[web](https://example.com) [section](#section)\n"

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


if __name__ == "__main__":
    unittest.main()
