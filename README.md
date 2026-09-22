# Codebase Map

A fast, local, dependency-free CLI and Python library for understanding the shape of an unfamiliar codebase without executing its code.

**Author:** Radwan Abdulhadi Ahmed · رضوان عبدالهادي أحمد · [@rad03i2](https://github.com/rad03i2)

## Why it exists
Large repositories are difficult to orient around quickly. Codebase Map produces a deterministic inventory, language/file statistics, approximate source line counts, and a compact tree that can be saved or consumed as JSON.

## Features
- Recursive repository inventory with relative paths and byte sizes.
- Language recognition for common Python, web, systems, JVM, .NET, scripting and data files.
- Per-language file and text-line counts.
- Compact tree view with configurable depth.
- Machine-readable JSON output and reusable Python API.
- Optional output-to-file and hidden-file inclusion.
- Ignores common generated/vendor directories by default.
- Never executes or imports target-project code; no network access or telemetry.
- Skips symbolic links and caps scans at 50,000 files by default.

## Requirements & installation
Python 3.10 or newer. Runtime has no third-party dependencies.

```bash
git clone https://github.com/rad03i2/codebase-map.git
cd codebase-map
python -m pip install -e .
```

## Usage
```bash
codebase-map .
codebase-map /path/to/project --tree --depth 5
codebase-map . --json
codebase-map . --json --output reports/map.json
codebase-map . --include-hidden --max-files 100000
```

Default output is a concise statistical summary. `--tree` is intended for human orientation; `--json` includes every discovered file and is intended for tooling.

### Python API
```python
from codebase_map import scan, render_tree

result = scan(".")
print(result.languages)
print(render_tree(result, max_depth=3))
```

## Configuration
There is intentionally no configuration file. CLI options make each run explicit. Generated/vendor directories such as `.git`, `.venv`, `node_modules`, `dist`, and `build` are always excluded. Hidden paths are excluded unless `--include-hidden` is supplied.

## Project structure
```text
src/codebase_map/core.py   scanning, statistics, rendering
src/codebase_map/cli.py    command-line interface
src/codebase_map/__init__.py public API
tests/test_core.py         functional tests
.github/workflows/ci.yml   cross-platform CI
```

## Testing
```bash
python -m unittest discover -s tests -v
python -m compileall -q src tests
codebase-map . --json
```
CI runs these checks on Ubuntu, Windows and macOS using Python 3.10, 3.12 and 3.13.

## Preview guidance
For a portfolio screenshot, run `codebase-map . --tree --depth 4` in a clean terminal at the repository root. No screenshot is committed because output depends on the inspected project.

## Security & privacy
Codebase Map operates locally, performs read-only inspection of the target, does not follow symlinks, does not execute project code, and makes no network requests. JSON output contains file paths, so review it before sharing if repository names or paths are sensitive.

## Limitations
Language identification is extension-based. Line counts are physical text lines, not semantic LOC, and are skipped for files over 2 MB. Binary content is not analyzed. The tree is a file-oriented compact view rather than a call graph, dependency graph, AST analyzer, or architecture inference engine. Files that change during a scan can yield a point-in-time approximation.

## Optional roadmap
Possible future additions include opt-in `.gitignore` rule interpretation, export to Mermaid, and language-specific symbol indexing. These are not claimed as current features.

## Contributing
Contributions are welcome. Keep behavior cross-platform and dependency-light, add tests for behavior changes, and avoid features that execute untrusted target code. See `CONTRIBUTING.md`.

## License
MIT — see `LICENSE`.

## Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **[@rad03i2](https://github.com/rad03i2)**

---

# العربية

## خريطة قاعدة الشفرة — Codebase Map
أداة محلية سريعة تعمل من سطر الأوامر، إضافة إلى واجهة Python، لفهم بنية مشروع برمجي غير مألوف دون تشغيل شفرته.

## لماذا هذا المشروع؟
قد يصعب استيعاب المستودعات الكبيرة بسرعة. تنشئ الأداة جردًا منظمًا للملفات، وإحصاءات للغات والأحجام والأسطر، وشجرة مختصرة، مع إمكانية إخراج JSON لاستخدام النتائج في الأدوات والأتمتة.

## المزايا
- مسح المجلدات والملفات بصورة متكررة مع مسارات نسبية وأحجام.
- التعرف على مجموعة واسعة من لغات البرمجة الشائعة اعتمادًا على الامتداد.
- إحصاء عدد الملفات والأسطر لكل لغة.
- عرض شجرة مختصرة بعمق قابل للتحديد.
- إخراج JSON وواجهة Python قابلة لإعادة الاستخدام.
- حفظ النتيجة في ملف ودعم اختياري للملفات المخفية.
- تجاهل مجلدات البناء والاعتماديات الشائعة تلقائيًا.
- لا تشغّل شفرة المشروع ولا تستخدم الشبكة أو القياس عن بعد.
- تتجاوز الروابط الرمزية وتضع حدًا افتراضيًا قدره 50,000 ملف.

## المتطلبات والتثبيت
تحتاج Python 3.10 أو أحدث، ولا توجد اعتماديات خارجية وقت التشغيل.

```bash
git clone https://github.com/rad03i2/codebase-map.git
cd codebase-map
python -m pip install -e .
```

## الاستخدام
```bash
codebase-map .
codebase-map . --tree --depth 5
codebase-map . --json --output reports/map.json
```

ويمكن استخدامها برمجيًا:
```python
from codebase_map import scan
result = scan(".")
print(result.languages)
```

## الإعداد والبنية
لا يوجد ملف إعداد متعمدًا؛ الخيارات واضحة في كل تشغيل. توجد نواة المسح في `src/codebase_map/core.py` وواجهة الأوامر في `cli.py` والاختبارات في `tests/` وCI في `.github/workflows/ci.yml`.

## الاختبارات
```bash
python -m unittest discover -s tests -v
python -m compileall -q src tests
```
ويفحص CI المشروع على Linux وWindows وmacOS عبر عدة إصدارات Python.

## المعاينة
لصورة مناسبة للمعرض شغّل `codebase-map . --tree --depth 4` في طرفية نظيفة. لم نضع صورة ثابتة لأن النتيجة تتغير حسب المشروع المفحوص.

## الخصوصية والأمان
الفحص محلي وللقراءة فقط، ولا يتبع الروابط الرمزية ولا يشغّل ملفات المشروع ولا يرسل بيانات إلى الشبكة. قد يحتوي JSON على أسماء ومسارات ملفات، لذلك راجعه قبل مشاركته.

## القيود
التعرف على اللغة يعتمد على امتداد الملف. عدد الأسطر هو عدد الأسطر النصية الفعلية وليس LOC دلاليًا، وتتجاوز الأداة حساب أسطر الملفات الأكبر من 2MB. ليست الأداة محلل AST أو call graph أو dependency graph ولا تدّعي استنتاج معمارية المشروع آليًا.

## التطوير المستقبلي الاختياري
يمكن مستقبلًا إضافة دعم اختياري لقواعد `.gitignore`، وتصدير Mermaid، وفهرسة الرموز حسب اللغة. هذه ليست ميزات حالية.

## المساهمة والترخيص
المساهمات مرحب بها مع الحفاظ على التوافق بين الأنظمة وإضافة اختبارات للتغييرات. المشروع مرخص برخصة MIT؛ راجع `LICENSE` و`CONTRIBUTING.md`.

## المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **[@rad03i2](https://github.com/rad03i2)**
