# Changelog

## 2026-10-29

### Fixed
- Theme editor saves the gradient stops you edit (it used to write the preset's stops).
- Theme editor loads `imports/theme.nss` on start; added **Reload theme.nss**.
- Presets apply cleanly without Streamlit session-state warnings.
- Radial gradient values are saved.
- Live preview renders gradients (valid CSS, correct angle).
- Imports tab detects imported files on Windows; add/remove back up `shell.nss` first.
- Zip import only restores `.nss` files inside the project (no path traversal) and no longer crashes when restoring theme state.
- Consistent UTF-8 file handling; Find & Replace keeps backslashes literal.
- Template and icon "copy" buttons replaced with real copyable snippets.
- Modify: hide honors the type filter, invalid `pos="last"` removed, append disabled until a target is set.
- Item builder quotes values safely; syntax checker skips `//` and `/* */` comments.
- Settings parser handles `key = value` with spaces.
- Icon browser renders icons that use shared SVG templates.
- `shell.nss` imports `imports/custom.nss`; `theme.nss` uses the documented `dark=default`.

### Changed
- Animated README banner rebuilt as a 16s motion loop.
- AGENTS.md, SKILL.md, README rewritten against the local `Docs/`; added CLAUDE.md.
- Requires Streamlit 1.50+ (`requirements.txt`).
