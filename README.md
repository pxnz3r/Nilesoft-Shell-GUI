<div align="center">
  <img src="https://raw.githubusercontent.com/pxnz3r/Nilesoft-Shell-GUI/bd79960/assets/hero-banner.svg" alt="Nilesoft Shell GUI" width="800">
  <br><br>
  <p>A visual editor for <a href="https://github.com/moudey/shell">Nilesoft Shell</a> context menu configuration - no manual <code>.nss</code> editing required.</p>
  <p>
    <a href="https://github.com/pxnz3r/Nilesoft-Shell-GUI/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="MIT"></a>
    <a href="https://streamlit.io"><img src="https://img.shields.io/badge/built%20with-Streamlit-FF4B4B?style=flat-square&logo=streamlit" alt="Streamlit"></a>
    <a href="https://github.com/moudey/shell/releases"><img src="https://img.shields.io/badge/Nilesoft%20Shell-1.9%2B-181717?style=flat-square" alt="Nilesoft Shell"></a>
    <a href="https://www.python.org"><img src="https://img.shields.io/badge/python-3.10%2B-3776AB?style=flat-square&logo=python" alt="Python"></a>
  </p>
</div>

## Setup

**1. Install Nilesoft Shell**

Use the installer from the [latest release](https://github.com/moudey/shell/releases), or `winget install nilesoft.shell`. For the portable zip, register it from an admin terminal:
```bat
shell.exe -register -restart
```

**2. Clone and install dependencies**
```bat
git clone https://github.com/pxnz3r/Nilesoft-Shell-GUI
cd Nilesoft-Shell-GUI
pip install -r requirements.txt
```

**3. Run the GUI**
```bat
streamlit run theme-tweaker.py
```
Or double-click `start.bat`. Opens at `http://localhost:8501`. The Theme tab starts from your current `imports/theme.nss`.

## Linking Config to Shell

For changes to take effect, Shell needs access to the `.nss` files:

**Copy** - copy the repo files into your Shell install folder.

**Symlink** - run as admin for live editing:
```bat
mklink /J "C:\Program Files\Nilesoft Shell\imports" "C:\full\path\to\Nilesoft-Shell-GUI\imports"
mklink "C:\Program Files\Nilesoft Shell\shell.nss" "C:\full\path\to\Nilesoft-Shell-GUI\shell.nss"
```

After any change: **Ctrl + right-click** desktop &rarr; **Shell &rarr; Update changes** (or restart Explorer).

> Set the Shell install path in the **Settings &rarr; Shell Installation Path** tab to read `shell.log` for errors.

## Features

| Tab | Purpose |
|-----|---------|
| Menu Items | Build custom entries (title, command, args, icon, conditions) plus a snippet library |
| Modify | Hide, reorder, or move built-in system menu items |
| Settings | Priority, delay, tooltips, exclude condition, `shell.log` viewer |
| Imports | Toggle imports, inline editor for any `.nss` file, syntax checker |
| Theme | Colors, gradients (up to 6 stops), effects, border, shadow, font, 10 presets, live preview |
| Icons | Preview every SVG in `images.nss` in your theme's icon colors |
| Find | Search and replace across all `.nss` files |
| Export | Package your config as `.zip` with optional theme state, and restore it |
| History | Auto-timestamped backups with one-click restore |

## Structure

```
├── theme-tweaker.py         Streamlit GUI
├── requirements.txt         Python dependencies
├── start.bat                Launcher
├── shell.nss                Main entry point (imports all modules)
├── imports/
│   ├── theme.nss            Colors, gradients, fonts, borders, shadows
│   ├── modify.nss           System item reordering rules
│   ├── custom.nss           Your custom menu items (auto-created)
│   ├── images.nss           ~100 SVG icon definitions
│   ├── terminal.nss         Terminal / command prompt entries
│   ├── file-manage.nss      File operations (copy path, attributes, etc.)
│   ├── develop.nss          Dev tools (VS Code, dotnet, etc.)
│   ├── goto.nss             Navigation shortcuts
│   └── taskbar.nss          Taskbar-specific items
├── Docs/                    Nilesoft Shell reference documentation
├── AGENTS.md                AI assistant context
├── CLAUDE.md                Claude Code entry (imports AGENTS.md)
└── SKILL.md                 NSS syntax reference for assistants
```

## Documentation

Full Nilesoft Shell reference in the `Docs/` folder or at [nilesoft.org/docs](https://nilesoft.org/docs).

## License

This GUI is [MIT](LICENSE) licensed. Nilesoft Shell and the default `.nss` configs it ships are MIT by [moudey](https://github.com/moudey/shell).

Contributions welcome, see [CONTRIBUTING.md](CONTRIBUTING.md). Release notes are in [CHANGELOG.md](CHANGELOG.md).

---

Made with ❤️ by pxnz3r
