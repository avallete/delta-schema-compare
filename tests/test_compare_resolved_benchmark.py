import sys
import tempfile
import types
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
sys.modules.setdefault("openai", types.SimpleNamespace(OpenAI=object))

from compare_resolved import (  # noqa: E402
    benchmark_issue_map,
    next_benchmark_index,
    slugify,
    write_benchmark_file,
)


class CompareResolvedBenchmarkTests(unittest.TestCase):
    def test_slugify(self) -> None:
        self.assertEqual(slugify("ALTER COLUMN TYPE ... USING"), "alter-column-type-using")
        self.assertEqual(slugify("!!!"), "issue")
        self.assertEqual(slugify(""), "issue")
        self.assertTrue(slugify("A" * 200).startswith("a"))
        self.assertLessEqual(len(slugify("A" * 200)), 72)
        self.assertFalse(slugify("A" * 100 + "-" * 100).endswith("-"))
        self.assertEqual(slugify("Some::Gap ### 2026"), "some-gap-2026")

    def test_benchmark_issue_map_and_next_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "001-first.md").write_text(
                "Relates to pgschema issue #123: https://example.test/123",
                encoding="utf-8",
            )
            (root / "README.md").write_text("# Ignore", encoding="utf-8")
            mapping = benchmark_issue_map(root)
            self.assertEqual(mapping[123].name, "001-first.md")
            self.assertEqual(next_benchmark_index(root), 2)

    def test_write_benchmark_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            issue = {"number": 77, "html_url": "https://github.com/pgplex/pgschema/issues/77"}
            out = write_benchmark_file(root, issue, "Test Gap", "## Context\nx")
            self.assertTrue(out.exists())
            text = out.read_text(encoding="utf-8")
            self.assertIn("Relates to pgschema issue #77", text)
            self.assertIn("## Context", text)


if __name__ == "__main__":
    unittest.main()
