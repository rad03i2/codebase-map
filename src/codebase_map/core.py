from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

IGNORED = {".git", ".hg", ".svn", ".venv", "venv", "node_modules", "__pycache__", ".idea", ".vscode", "dist", "build", ".pytest_cache", ".mypy_cache"}
LANGUAGES = {
    ".py": "Python", ".js": "JavaScript", ".jsx": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript",
    ".java": "Java", ".cs": "C#", ".cpp": "C++", ".cc": "C++", ".c": "C", ".h": "C/C++ Header",
    ".go": "Go", ".rs": "Rust", ".rb": "Ruby", ".php": "PHP", ".swift": "Swift", ".kt": "Kotlin",
    ".html": "HTML", ".css": "CSS", ".scss": "SCSS", ".sql": "SQL", ".sh": "Shell", ".ps1": "PowerShell",
}
TEXT_EXTENSIONS = set(LANGUAGES) | {".md", ".txt", ".json", ".toml", ".yaml", ".yml", ".xml", ".ini", ".cfg"}
MAX_FILE_BYTES = 2_000_000

@dataclass(frozen=True)
class FileInfo:
    path: str
    size: int
    language: str | None
    lines: int | None

@dataclass(frozen=True)
class MapResult:
    root: str
    files: tuple[FileInfo, ...]
    directories: int
    total_bytes: int
    languages: dict[str, int]
    language_lines: dict[str, int]
    skipped: int

    def to_dict(self) -> dict:
        value = asdict(self)
        value["files"] = [asdict(item) for item in self.files]
        return value

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


def _line_count(path: Path) -> int | None:
    try:
        if path.stat().st_size > MAX_FILE_BYTES or path.suffix.lower() not in TEXT_EXTENSIONS:
            return None
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            return sum(1 for _ in handle)
    except OSError:
        return None


def scan(root: str | Path, *, include_hidden: bool = False, max_files: int = 50_000) -> MapResult:
    base = Path(root).expanduser().resolve()
    if not base.exists():
        raise FileNotFoundError(f"Path does not exist: {base}")
    if not base.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {base}")
    if max_files < 1:
        raise ValueError("max_files must be at least 1")

    files: list[FileInfo] = []
    dirs: set[Path] = set()
    skipped = 0
    for path in base.rglob("*"):
        rel = path.relative_to(base)
        if any(part in IGNORED or (not include_hidden and part.startswith(".")) for part in rel.parts):
            continue
        if path.is_symlink():
            skipped += 1
            continue
        if path.is_dir():
            dirs.add(path)
            continue
        if not path.is_file():
            skipped += 1
            continue
        if len(files) >= max_files:
            raise RuntimeError(f"File limit exceeded ({max_files}); narrow the target or raise --max-files")
        try:
            size = path.stat().st_size
        except OSError:
            skipped += 1
            continue
        language = LANGUAGES.get(path.suffix.lower())
        files.append(FileInfo(rel.as_posix(), size, language, _line_count(path)))

    language_files = Counter(f.language for f in files if f.language)
    language_lines = Counter()
    for item in files:
        if item.language and item.lines is not None:
            language_lines[item.language] += item.lines
    return MapResult(str(base), tuple(sorted(files, key=lambda f: f.path.lower())), len(dirs), sum(f.size for f in files), dict(language_files.most_common()), dict(language_lines.most_common()), skipped)


def render_tree(result: MapResult, *, max_depth: int = 4) -> str:
    if max_depth < 1:
        raise ValueError("max_depth must be at least 1")
    root = Path(result.root).name or result.root
    lines = [root + "/"]
    paths = [Path(f.path) for f in result.files if len(Path(f.path).parts) <= max_depth]
    for path in paths:
        indent = "  " * (len(path.parts) - 1)
        info = next(f for f in result.files if f.path == path.as_posix())
        suffix = f" [{info.language}]" if info.language else ""
        lines.append(f"{indent}├─ {path.name}{suffix}")
    return "\n".join(lines)


def summary(result: MapResult) -> str:
    lines = [
        f"Root: {result.root}", f"Files: {len(result.files)}", f"Directories: {result.directories}",
        f"Size: {result.total_bytes} bytes", f"Skipped: {result.skipped}", "Languages:",
    ]
    if not result.languages:
        lines.append("  (no recognized source files)")
    for lang, count in result.languages.items():
        loc = result.language_lines.get(lang, 0)
        lines.append(f"  {lang}: {count} file(s), {loc} line(s)")
    return "\n".join(lines)
