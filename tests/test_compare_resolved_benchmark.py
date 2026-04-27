import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
sys.modules.setdefault("openai", types.SimpleNamespace(OpenAI=object))

import compare_resolved  # noqa: E402
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

    def test_write_benchmark_file_overwrites_existing_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            existing = root / "001-existing-gap.md"
            existing.write_text("old", encoding="utf-8")
            issue = {"number": 88, "html_url": "https://github.com/pgplex/pgschema/issues/88"}

            out = write_benchmark_file(
                root,
                issue,
                "Updated Gap",
                "## Context\nnew",
                path=existing,
            )

            self.assertEqual(out, existing)
            text = out.read_text(encoding="utf-8")
            self.assertIn("# Updated Gap", text)
            self.assertIn("Relates to pgschema issue #88", text)
            self.assertIn("## Context\nnew", text)

    def test_main_keeps_historical_benchmark_when_issue_is_still_covered(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            benchmark_dir = root / "benchmark"
            benchmark_dir.mkdir()
            (root / "repos" / "pg-toolbelt" / "packages" / "pg-delta").mkdir(
                parents=True
            )
            (root / "repos" / "pgschema").mkdir(parents=True)
            benchmark_file = benchmark_dir / "001-existing-gap.md"
            benchmark_file.write_text(
                "# Existing Gap\n\nRelates to pgschema issue #268: https://github.com/pgplex/pgschema/issues/268\n",
                encoding="utf-8",
            )
            review_memory_path = benchmark_dir / "review-memory.json"

            issue = {
                "number": 268,
                "title": "materialized view cascade dependencies",
                "html_url": "https://github.com/pgplex/pgschema/issues/268",
                "updated_at": "2026-02-09T03:57:30Z",
            }

            with (
                mock.patch.object(compare_resolved, "GITHUB_TOKEN", "test-token"),
                mock.patch.object(compare_resolved, "DRY_RUN", False),
                mock.patch.object(
                    compare_resolved,
                    "OUTPUT_MODE",
                    compare_resolved.OUTPUT_MODE_BENCHMARK,
                ),
                mock.patch.object(compare_resolved, "BENCHMARK_DIR", benchmark_dir),
                mock.patch.object(compare_resolved, "REVIEW_MEMORY_PATH", review_memory_path),
                mock.patch.object(
                    compare_resolved,
                    "PGDELTA_LOCAL_PATH",
                    root / "repos" / "pg-toolbelt" / "packages" / "pg-delta",
                ),
                mock.patch.object(
                    compare_resolved,
                    "PGSCHEMA_LOCAL_PATH",
                    root / "repos" / "pgschema",
                ),
                mock.patch.object(compare_resolved, "get_resolved_pgschema_issues", return_value=[issue]),
                mock.patch.object(compare_resolved, "load_review_memory", return_value={"open": {}, "resolved": {}}),
                mock.patch.object(compare_resolved, "get_git_head", side_effect=["pgdelta-sha", "pgschema-sha"]),
                mock.patch.object(compare_resolved, "has_local_coverage", return_value=True),
                mock.patch.object(compare_resolved, "collect_pgdelta_snippets", return_value="snippets"),
                mock.patch.object(compare_resolved, "llm_has_coverage", return_value=True),
                mock.patch.object(compare_resolved, "save_review_memory") as save_review_memory,
            ):
                compare_resolved.main()

            self.assertTrue(benchmark_file.exists(), "covered benchmark files should be retained as historical context")
            saved_memory = save_review_memory.call_args.args[1]
            self.assertEqual(saved_memory["resolved"]["268"]["verdict"], "covered")


if __name__ == "__main__":
    unittest.main()
