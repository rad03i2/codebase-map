import json
import tempfile
import unittest
from pathlib import Path

from codebase_map.core import render_tree, scan, summary


class CodebaseMapTests(unittest.TestCase):
    def test_scan_counts_languages_and_lines(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "app.py").write_text("print('x')\nprint('y')\n", encoding="utf-8")
            (root / "web.ts").write_text("export const x = 1;\n", encoding="utf-8")
            result = scan(root)
            self.assertEqual(len(result.files), 2)
            self.assertEqual(result.languages, {"Python": 1, "TypeScript": 1})
            self.assertEqual(result.language_lines["Python"], 2)
            self.assertIn("Files: 2", summary(result))
            self.assertEqual(json.loads(result.to_json())["languages"]["Python"], 1)

    def test_ignored_and_hidden_content(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".secret.py").write_text("x=1\n", encoding="utf-8")
            generated = root / "node_modules"
            generated.mkdir()
            (generated / "x.js").write_text("x\n", encoding="utf-8")
            self.assertEqual(len(scan(root).files), 0)
            self.assertEqual(len(scan(root, include_hidden=True).files), 1)

    def test_tree_and_safety_limit(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "a.py").write_text("x\n", encoding="utf-8")
            (root / "b.py").write_text("y\n", encoding="utf-8")
            result = scan(root)
            self.assertIn("a.py [Python]", render_tree(result))
            with self.assertRaises(RuntimeError):
                scan(root, max_files=1)

    def test_rejects_file_as_root(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "x.txt"
            path.write_text("x", encoding="utf-8")
            with self.assertRaises(NotADirectoryError):
                scan(path)


if __name__ == "__main__":
    unittest.main()
