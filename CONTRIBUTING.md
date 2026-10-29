# Contributing

Issues and pull requests are welcome.

## Setup
```bat
pip install -r requirements.txt
streamlit run theme-tweaker.py
```
Read `AGENTS.md` first. It explains how the GUI's state handling works and the rules that keep it from breaking (widgets bound by `key=` only, state changes only from callbacks).

## Before opening a PR
- Keep changes focused; one fix or feature per PR.
- Check NSS syntax against `Docs/` or [nilesoft.org/docs](https://nilesoft.org/docs), not memory.
- Run a quick headless check; it should print `[]`:
  ```bat
  python -c "from streamlit.testing.v1 import AppTest; print(AppTest.from_file('theme-tweaker.py', default_timeout=60).run().exception)"
  ```
- If you changed `.nss` files, reload Shell (Ctrl + right-click desktop, **Shell > Update changes**) and check `shell.log` for errors.
- Add a line to `CHANGELOG.md`.

Bugs in Nilesoft Shell itself belong upstream at [moudey/shell](https://github.com/moudey/shell/issues).
