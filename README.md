<div align="center">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 180" width="600" height="180">
    <defs>
      <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#1a1a3e"><animate attributeName="stop-color" values="#1a1a3e;#0f2255;#1a1a3e" dur="6s" repeatCount="indefinite"/></stop>
        <stop offset="50%" stop-color="#0f2255"><animate attributeName="stop-color" values="#0f2255;#1a1a3e;#0f2255" dur="6s" repeatCount="indefinite"/></stop>
        <stop offset="100%" stop-color="#0a0a2e"><animate attributeName="stop-color" values="#0a0a2e;#162040;#0a0a2e" dur="6s" repeatCount="indefinite"/></stop>
      </linearGradient>
      <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="#6366f1"><animate attributeName="stop-color" values="#6366f1;#818cf8;#6366f1" dur="4s" repeatCount="indefinite"/></stop>
        <stop offset="100%" stop-color="#a78bfa"><animate attributeName="stop-color" values="#a78bfa;#818cf8;#a78bfa" dur="4s" repeatCount="indefinite"/></stop>
      </linearGradient>
    </defs>
    <rect width="600" height="180" rx="12" fill="url(#bg)"/>
    <rect x="0" y="0" width="600" height="4" fill="url(#accent)"/>
    <g transform="translate(50, 50)">
      <rect x="0" y="0" width="220" height="90" rx="8" fill="#ffffff10" stroke="#ffffff20" stroke-width="1"/>
      <rect x="10" y="10" width="200" height="16" rx="4" fill="#ffffff15"><animate attributeName="opacity" values="0.3;0.6;0.3" dur="2s" repeatCount="indefinite"/></rect>
      <rect x="10" y="34" width="160" height="14" rx="4" fill="#ffffff12"/>
      <rect x="10" y="54" width="140" height="14" rx="4" fill="#ffffff12"/>
      <rect x="10" y="74" width="180" height="10" rx="4" fill="#ffffff08"/>
    </g>
    <text x="310" y="62" font-family="Segoe UI, sans-serif" font-size="22" font-weight="700" fill="#ffffff" letter-spacing="1">Nilesoft Shell GUI</text>
    <text x="310" y="86" font-family="Segoe UI, sans-serif" font-size="13" fill="#a0a0c0">Visual editor for context menu config</text>
    <g transform="translate(310, 100)">
      <rect x="0" y="0" width="90" height="26" rx="6" fill="#6366f1" opacity="0.9"><animate attributeName="width" values="90;110;90" dur="3s" repeatCount="indefinite"/></rect>
      <text x="16" y="17" font-family="monospace" font-size="11" fill="#fff">Streamlit</text>
    </g>
    <text x="310" y="135" font-family="Segoe UI, sans-serif" font-size="11" fill="#606080">Made with</text>
    <g transform="translate(370, 122)">
      <path d="M0-6 A8 8 0 0 1 16-6 A8 8 0 0 1 32-6 Q32 4 16 16 Q0 4 0-6Z" fill="none" stroke="#ef4444" stroke-width="1.5">
        <animate attributeName="d" values="M0-6 A8 8 0 0 1 16-6 A8 8 0 0 1 32-6 Q32 4 16 16 Q0 4 0-6Z;M0-4 A10 10 0 0 1 16-4 A10 10 0 0 1 32-4 Q32 6 16 18 Q0 6 0-4Z;M0-6 A8 8 0 0 1 16-6 A8 8 0 0 1 32-6 Q32 4 16 16 Q0 4 0-6Z" dur="1s" repeatCount="indefinite"/>
        <animate attributeName="fill" values="#ef4444;#f87171;#ef4444" dur="1s" repeatCount="indefinite"/>
      </path>
    </g>
    <text x="408" y="135" font-family="Segoe UI, sans-serif" font-size="11" fill="#606080">by pxnz3r</text>
  </svg>
</div>

## Prerequisites

- [Nilesoft Shell](https://github.com/moudey/shell) installed on Windows
  - Download the latest release, extract, and run `shell.exe /reg` to register the shell extension
- **Python 3.10+** with `streamlit` installed (`pip install streamlit`)

## Quick Start

```bat
git clone <your-repo-url>
cd nilesoft-shell-gui
streamlit run theme-tweaker.py
```

Opens at `http://localhost:8501`.

## Linking Config to Shell

For Nilesoft Shell to pick up your `.nss` files, they need to be in Shell's config directory. Two options:

**Option A - Copy** (simple): Copy all `.nss` files from this repo into your Shell install folder (where `shell.exe` lives).

**Option B - Symlink** (recommended for dev): Run as admin:
```bat
mklink /J "C:\Program Files\Nilesoft Shell\imports" "C:\full\path\to\repo\imports"
mklink "C:\Program Files\Nilesoft Shell\shell.nss" "C:\full\path\to\repo\shell.nss"
```

After any change: **Ctrl + right-click** desktop → **Shell → Update changes** (or restart Explorer).

> Set your Shell install path in the **Settings → Shell Installation Path** tab so the GUI can open `shell.log` for error checking.

## Features

| Tab | Purpose |
|-----|---------|
| **🎨 Theme** | Edit colors, gradient, font, border, shadow - 9 presets |
| **➕ Menu Items** | Add custom context menu entries (app, command, icon, conditions) |
| **🔄 Modify** | Hide, reorder, or move built-in system menu items |
| **⚙️ Settings** | Global Shell behavior (priority, delay, tooltips, exclude) |
| **📂 Imports** | View, toggle, and edit all `.nss` files inline |
| **🔎 Icon Browser** | Preview all built-in icons and SVG definitions |
| **🔧 Syntax Check** | Validate `.nss` files for mismatched braces/parens |
| **📜 History** | Auto-backups: restore any previous version |
| **📦 Export/Import** | Package your config as `.zip` |

## Project Structure

```
├── theme-tweaker.py         # Streamlit GUI
├── start.bat                # Launcher
├── shell.nss                # Main entry point
├── imports/
│   ├── theme.nss            # Visual theme
│   ├── modify.nss           # System item reordering
│   ├── custom.nss           # Your custom items
│   ├── images.nss           # SVG icons
│   ├── terminal.nss         # Terminal entries
│   ├── file-manage.nss      # File operations
│   ├── develop.nss          # Dev tools
│   ├── goto.nss             # Navigation shortcuts
│   └── taskbar.nss          # Taskbar items
├── AGENTS.md                # AI assistant context
└── SKILL.md                 # LLM skill instructions
```

## Docs

Detailed Nilesoft Shell reference docs in `Docs/`:
- [Getting Started](Docs/Get_started.md)
- [Syntax Rules](Docs/Configuration/Syntax_rules.md)
- [Themes](Docs/Configuration/themes.md)
- [Expressions](Docs/Expressions/expressions.md)
- [Examples](Docs/Examples/example1.md)

Or visit [nilesoft.org/docs](https://nilesoft.org/docs).

## License

This GUI project is MIT licensed. Nilesoft Shell itself is [MIT](LICENSE) by [moudey](https://github.com/moudey/shell).
