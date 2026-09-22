# Contributing

Thank you for improving Codebase Map.

1. Use Python 3.10+ and keep runtime dependencies at zero unless a strong case exists.
2. Preserve read-only behavior: never execute or import code from the inspected target.
3. Add or update tests for behavioral changes.
4. Run `python -m unittest discover -s tests -v` and `python -m compileall -q src tests`.
5. Keep documentation accurate and avoid claiming unimplemented features.
6. Use focused commits and describe observable behavior changes clearly.

By contributing, you agree that your contribution is provided under the MIT License.
