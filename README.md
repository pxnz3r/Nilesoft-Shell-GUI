<div align="center">
  <img src="assets/hero-banner.svg" alt="Nilesoft Shell GUI" width="600">
  <br><br>
  <p>A visual editor for <a href="https://github.com/moudey/shell">Nilesoft Shell</a> context menu configuration &mdash; no manual <code>.nss</code> editing required.</p>
  <p><em>Visual editor for Windows context menu config files</em></p>
</div>

## Setup

**1. Install Nilesoft Shell**

Download the [latest release](https://github.com/moudey/shell/releases), extract, and register:
```
shell.exe /reg
```

**2. Clone and install dependencies**
```bat
git clone https://github.com/pxnz3r/Nilesoft-Shell-GUI
cd Nilesoft-Shell-GUI
pip install streamlit
```

**3. Run the GUI**
```bat
streamlit run theme-tweaker.py
```
Opens at `http://localhost:8501`.

## Linking Config to Shell

For changes to take effect, Shell needs access to the `.nss` files:

**Copy** &mdash; copy the repo files into your Shell install folder.

**Symlink** &mdash; run as admin for live editing:
```bat
mklink /J "C:\Program Files\Nilesoft Shell\imports" "C:\full\path\to\Nilesoft-Shell-GUI\imports"
mklink "C:\Program Files\Nilesoft Shell\shell.nss" "C:\full\path\to\Nilesoft-Shell-GUI\shell.nss"
```

After any change: **Ctrl + right-click** desktop &rarr; **Shell &rarr; Update changes** (or restart Explorer).

> Set the Shell install path in the **Settings &rarr; Shell Installation Path** tab to read `shell.log` for errors.

## Features

| Tab | Purpose |
|-----|---------|
| Theme | Colors, 4-stop gradients, effects, border, shadow, font &mdash; 9 presets |
| Menu Items | Build custom entries (title, command, args, icon, conditions) |
| Modify | Hide, reorder, or move built-in system menu items |
| Settings | Priority, delay, tooltips, exclude condition |
| Imports | Inline editor for any `.nss` file with syntax validation |
| Icon Browser | Preview all built-in SVG icons with live color slots |
| History | Auto-timestamped backups with one-click restore |
| Export/Import | Package your config as `.zip` with optional theme state |

## Structure

```
├── theme-tweaker.py         Streamlit GUI
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
└── SKILL.md                 LLM skill instructions
```

## Documentation

Full Nilesoft Shell reference in the `Docs/` folder or at [nilesoft.org/docs](https://nilesoft.org/docs).

## License

This GUI is MIT licensed. Nilesoft Shell is [MIT](LICENSE) by [moudey](https://github.com/moudey/shell).

---

Made with ❤️ by pxnz3r
