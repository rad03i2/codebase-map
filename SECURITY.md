# Security Policy

## Supported version
The latest release on the default branch receives security fixes.

## Security model
Codebase Map is designed for local, read-only inspection. It does not execute target files, import target modules, follow symbolic links, make network requests, or collect telemetry. Known generated/vendor directories are excluded. Text line counting is limited to files at most 2 MB and the total scan has a configurable file-count limit.

Do not publish generated JSON blindly when repository paths themselves are confidential.

## Reporting
Please report a suspected vulnerability privately through GitHub's available security reporting mechanism when enabled. Do not place secrets, exploit payloads containing sensitive data, or private credentials in public issues.
