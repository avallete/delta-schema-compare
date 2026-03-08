import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from review_memory import (  # noqa: E402
    build_fingerprint,
    is_covered_cache_hit,
    load_review_memory,
    record_review_result,
    save_review_memory,
)


class ReviewMemoryTests(unittest.TestCase):
    def test_load_missing_file_returns_default_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "review-memory.json"
            self.assertEqual(load_review_memory(path), {"open": {}, "resolved": {}})

    def test_record_and_cache_hit_for_covered_verdict(self) -> None:
        memory = {"open": {}, "resolved": {}}
        issue = {
            "number": 42,
            "title": "sample",
            "html_url": "https://example.test/42",
            "updated_at": "2026-01-01T00:00:00Z",
        }
        fingerprint = build_fingerprint(issue, "pgdelta-sha", "pgschema-sha")
        record_review_result(memory, "open", issue, fingerprint, "covered")

        self.assertTrue(is_covered_cache_hit(memory, "open", 42, fingerprint))
        self.assertFalse(is_covered_cache_hit(memory, "open", 42, "different"))

    def test_save_and_load_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "review-memory.json"
            memory = {"open": {"1": {"verdict": "covered"}}, "resolved": {}}
            save_review_memory(path, memory)
            loaded = load_review_memory(path)
            self.assertEqual(loaded["open"]["1"]["verdict"], "covered")
            # confirm JSON file remains valid and human-readable
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertIn("open", data)


if __name__ == "__main__":
    unittest.main()
