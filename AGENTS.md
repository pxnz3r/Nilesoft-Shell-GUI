# Nilesoft Shell GUI: project context

## Overview
A **Streamlit** GUI (`theme-tweaker.py`) for editing [Nilesoft Shell](https://nilesoft.org/docs) context menu config files (`.nss`). Nilesoft Shell reads these files to customize the Windows File Explorer context menu. The GUI covers theme editing, custom items, modify rules, settings, imports, icons, find/replace, backups, and export/import.

`SKILL.md` has the NSS syntax reference for assistants. `Docs/` holds a local copy of the official reference; trust it over memory when they disagree.

## File structure
```
/
├── theme-tweaker.py         Streamlit GUI, all features in one file
├── requirements.txt         streamlit>=1.50
├── start.bat                Launcher (streamlit run theme-tweaker.py)
├── CHANGELOG.md             Release notes
├── CONTRIBUTING.md          Contributor setup and PR checklist
├── shell.nss                Main entry point: settings block + imports
├── AGENTS.md                This file
├── CLAUDE.md                Points Claude Code at this file
├── SKILL.md                 NSS syntax reference for assistants
├── README.md                Setup and feature overview
├── assets/hero-banner.svg   Animated README banner (pure SVG + CSS). README links it by commit hash
│                            to dodge GitHub's image cache: after changing it, commit, then update the hash.
├── imports/
│   ├── theme.nss            Visual theme (colors, gradient, font, border, shadow)
│   ├── modify.nss           Hide/move/reorder system menu items
│   ├── custom.nss           User items appended by the Menu Items tab
│   ├── images.nss           SVG image definitions (@name='<svg>...</svg>')
│   ├── terminal.nss         Terminal / command prompt entries
│   ├── file-manage.nss      File operations (copy path, attributes, ...)
│   ├── develop.nss          Dev tools (VS Code, dotnet)
│   ├── goto.nss             Navigation shortcuts
│   └── taskbar.nss          Taskbar menu items
├── Docs/                    Nilesoft Shell reference (Configuration, Expressions, Examples)
└── backups/                 Timestamped backups, created on first write (gitignored)
```

## GUI tabs

| Tab | What it does | Writes |
|-----|--------------|--------|
| Menu Items | Build `item(...)` from a form; template library with copyable snippets | appends to `imports/custom.nss`, adds its import to `shell.nss` if missing |
| Modify | Build `modify(...)` rules (move, hide, position) | appends to `imports/modify.nss` |
| Settings | priority, showdelay, exclude.where, tooltips, duplicate removal; shows `shell.log` | replaces the `settings { }` block in `shell.nss` |
| Imports | Add/remove import lines, inline editor per file, syntax checker | `shell.nss`, any `imports/*.nss` |
| Theme | Full theme editor, 10 presets, live menu preview | overwrites `imports/theme.nss` |
| Icons | Renders every SVG in `images.nss` with the theme's icon colors | nothing |
| Find | Search and replace across all `.nss` files | any `.nss` |
| Export | Zip of all `.nss` + AGENTS.md + SKILL.md (+ optional backups, theme state); import restores `.nss` files only | `.nss` files |
| History | Browse and restore backups | the restored file |
| Help | Usage guide | nothing |

Every write calls `backup_file()` first (`backups/<name>.<YYYYmmdd_HHMMSS>`).

## How the GUI code works
- **Theme state**: on first load `parse_theme()` reads `imports/theme.nss` into `st.session_state`, falling back to `DEFAULTS`. Widgets are bound by `key=` only (no `value=`), so state is the single source of truth.
- **Changing state**: only before the theme widgets render. Use `load_theme_state()` from an `on_click`/`on_change` callback (presets, Reload, Reset), or set `st.session_state._pending_state` and `st.rerun()` (zip import). Setting a widget key after its widget rendered raises `StreamlitAPIException`.
- **Gradient stops** live in `num_stops`, `so_<i>` (offset) and `sc_<i>` (color). `current_stops()` collects them; `generate_theme()` writes them.
- **Hidden widgets**: a loop at the top re-assigns theme keys every run so Streamlit doesn't drop values while their widgets are hidden (font off, radial vs linear).
- **File IO**: read with `read_file_safe()` (UTF-8 with BOM stripped, cp1252 fallback, missing file = ""). Write UTF-8. Catch `OSError`, not bare `except`.
- **Imports**: `import_paths()` parses `import '...'` lines; paths use forward slashes (`imports/x.nss`).
- Requires Streamlit 1.50+ (`width="stretch"`, `st.html`).

## Key NSS syntax

### Theme block
```nss
theme
{
    name="modern"              // modern, classic, white, black
    dark=default               // default, true, false
    view=view.compact          // auto, compact, small, medium, large, wide
    background
    {
        color=#hex
        opacity=100
        effect=2               // 0=disable, 1=transparent, 2=blur, 3=acrylic
        gradient { enabled=true linear=[x1, x2, y1, y2] stop=[[offset, #hex], ...] }
    }
    item { radius=0 text { normal=#hex select=#hex } back { normal=#hex select=#hex } }
    image { color=[#c1, #c2, #c3] align=2 }    // 0=check mark, 1=image, 2=both
    border { enabled=true size=2 color=#hex opacity=80 radius=6 }
    shadow { enabled=true size=8 color=#000 opacity=40 offset=2 }
    font { name="Segoe UI" size=9 weight=4 italic=0 }
}
```

### Items
```nss
item(title='My App' cmd='notepad.exe' args='"@sel.path"' image=icon.settings admin)
menu(title='Submenu' image=icon.folder) { item(...) }
```

### Modify rules
```nss
modify(where=this.id==id.copy_as_path vis=vis.remove)                    // hide
modify(find="unpin*" pos="bottom" menu="Pin/Unpin")                      // move by name
modify(type="dir.back" where=this.id==id.customize_this_folder pos=1 menu="file manage")
modify(mode=mode.multiple where=this.id(id.send_to, id.share) pos=1 menu=title.more_options)
```
`pos` accepts `auto`, `top`, `middle`, `bottom`, or an integer. `sep` accepts `none`, `top`/`before`, `bottom`/`after`, `both`.

### Settings
```nss
settings { priority=1 showdelay=200 exclude.where=!process.is_explorer modify.remove.duplicate=1 tip.enabled=true }
```

## Common system item IDs
`id.copy_as_path`, `id.properties`, `id.send_to`, `id.share`, `id.create_shortcut`, `id.pin_to_start`, `id.unpin_from_start`, `id.open_powershell_window_here`, `id.format`, `id.eject`, `id.restore_previous_versions`, `id.cast_to_device`, `id.empty_recycle_bin`, `id.rotate_left`, `id.rotate_right`, `id.give_access_to`, `id.include_in_library`, `id.print`, `id.map_network_drive`, `id.disconnect_network_drive`, `id.customize_this_folder`

## Development
1. Install [Nilesoft Shell](https://github.com/moudey/shell) on Windows.
2. `pip install -r requirements.txt`
3. `streamlit run theme-tweaker.py` (or `start.bat`)
4. Link the `.nss` files into Shell's install folder (see README).
5. Set the Shell install path in the Settings tab to see `shell.log`.

No test suite. A quick headless check: `streamlit.testing.v1.AppTest.from_file("theme-tweaker.py").run()` and assert `at.exception` is empty.

## Reloading
After editing any `.nss` file: hold **Ctrl** and right-click the desktop or taskbar, then **Shell > Update changes**. Or restart Windows Explorer. Parse errors go to `shell.log` in the Shell install folder.
