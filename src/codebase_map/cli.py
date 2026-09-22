from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .core import render_tree, scan, summary


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="codebase-map", description="Map a local codebase without executing project code.")
    p.add_argument("path", nargs="?", default=".", help="Repository/directory to inspect")
    p.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    p.add_argument("--tree", action="store_true", help="Render a compact source tree")
    p.add_argument("--depth", type=int, default=4, help="Maximum tree depth (default: 4)")
    p.add_argument("--include-hidden", action="store_true", help="Include hidden files except known generated directories")
    p.add_argument("--max-files", type=int, default=50_000, help="Safety limit for scanned files")
    p.add_argument("--output", type=Path, help="Write output to a UTF-8 file")
    p.add_argument("--version", action="version", version="codebase-map 1.0.0")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        result = scan(args.path, include_hidden=args.include_hidden, max_files=args.max_files)
        if args.json:
            text = result.to_json()
        elif args.tree:
            text = render_tree(result, max_depth=args.depth)
        else:
            text = summary(result)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text + "\n", encoding="utf-8")
        else:
            print(text)
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
