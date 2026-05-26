# Nilesoft Shell - Project Context

## Overview
This project is a **Streamlit GUI** for editing [Nilesoft Shell](https://nilesoft.org/docs) context menu configuration files (`.nss`). It replaces manual `.nss` editing with a visual interface — theme editor, menu item builder, modify rules, live preview, and more.

The GUI edits `.nss` files that Nilesoft Shell reads to customize Windows File Explorer context menus.

## File Structure
```
/
├── theme-tweaker.py         # Streamlit GUI — all features in one file
├── start.bat                # Launcher for the GUI
├── shell.nss                # Main entry point — imports all modules
├── AGENTS.md                # This file — AI assistant context
├── SKILL.md                 # LLM skill instructions for Nilesoft Shell
├── README.md                # Project readme with setup instructions
├── LICENSE                  # MIT License
├── .gitignore               # Excludes binaries, backups, caches
│
├── assets/
│   └── hero-banner.svg      # Animated GitHub README banner
│
├── imports/
│   ├── theme.nss            # Visual theme (colors, gradient, font, shadow, border)
│   ├── modify.nss           # Reorder/hide system context menu items
│   ├── custom.nss           # Custom user-defined menu items (auto-created)
│   ├── images.nss           # ~100 SVG icon definitions
│   ├── terminal.nss         # Terminal/command prompt entries
│   ├── file-manage.nss      # File operations (copy path, attributes, etc.)
│   ├── develop.nss          # Dev tools (VS Code, dotnet commands)
│   ├── goto.nss             # Quick navigation shortcuts
│   └── taskbar.nss          # Taskbar-specific menu items
│
├── Docs/                    # Formatted Nilesoft Shell reference docs
│   ├── Get_started.md
│   ├── Introduction.md
│   ├── Configuration/       # themes, settings, items, modify, syntax
│   ├── Expressions/         # variables, operators, literals, colors
│   └── Examples/            # usage examples
│
└── backups/                 # Auto-created timestamped backups (gitignored)
```

## GUI Features

| Feature | Description |
|---------|-------------|
| Theme Editor | Colors, gradients (4-stop harmonized), effects, border, shadow, font |
| Presets | 9 hand-tuned 4-stop gradient presets (Navy Indigo, Crimson Navy, Forest, Twilight, Amber Glow, Dark Red, Bright Red, Light Blue, Dark Blue) |
| Menu Items | Build custom items with title, command, args, icon, where-conditions |
| Modify Rules | Hide, reorder, or move built-in system menu items |
| Settings | Priority, delay, tooltips, exclude condition |
| File Editor | Inline editing of any `.nss` file with syntax checker |
| Icon Browser | Preview all built-in SVG icons and color slot preview |
| Auto-backup | Timestamped backups before every write |
| Export/Import | Package config as `.zip` with optional theme state |

## Key NSS Syntax

### Theme block
```nss
theme
{
    name="modern"              // modern, classic, white, black
    dark=auto                  // auto, true, false
    background
    {
        color=#hex
        opacity=100
        effect=2               // 0=solid, 1=transparent, 2=blur, 3=acrylic
        gradient { enabled=true linear=[x1,x2,y1,y2] stop=[[offset, #hex], ...] }
    }
    item { text { normal=#hex select=#hex } back { normal=#hex select=#hex } }
    image { color=[#c1, #c2, #c3] align=2 }
    border { enabled=true size=2 color=#hex opacity=80 radius=6 }
    shadow { enabled=true size=8 color=#000 opacity=40 offset=2 }
    font { name="Segoe UI" size=9 weight=4 }
}
```

### Item block
```nss
item(title='My App' cmd='notepad.exe' args='@sel.path' image=icon.settings admin)
menu(title='Submenu' image=icon.folder) { item(...) }
```

### Modify rules
```nss
modify(where=this.id==id.copy_as_path vis=vis.remove)                    // hide
modify(find="unpin*" pos="bottom" menu="Pin/Unpin")                      // move by name
modify(type="dir.back" where=this.id==id.customize_this_folder pos=1 menu="file manage")
modify(mode=mode.multiple where=this.id(id.send_to, id.share) pos=1 menu=title.more_options)
```

### Settings block
```nss
settings { priority=1 showdelay=200 modify.remove.duplicate=1 tip.enabled=true }
```

## Common System Item IDs
`id.copy_as_path`, `id.properties`, `id.send_to`, `id.share`, `id.create_shortcut`, `id.pin_to_start`, `id.unpin_from_start`, `id.open_powershell_window_here`, `id.format`, `id.eject`, `id.restore_previous_versions`, `id.cast_to_device`, `id.empty_recycle_bin`, `id.rotate_left`, `id.rotate_right`, `id.give_access_to`, `id.include_in_library`, `id.print`, `id.map_network_drive`, `id.disconnect_network_drive`, `id.customize_this_folder`

## Setup for Development
1. Install [Nilesoft Shell](https://github.com/moudey/shell) on Windows
2. Clone this repo
3. `pip install streamlit`
4. `streamlit run theme-tweaker.py`
5. Set Shell install path in GUI Settings tab to read `shell.log`
6. Link `.nss` files to Shell's config dir (copy or symlink)

## Reloading
After editing any `.nss` file: hold **Ctrl + right-click** on desktop/taskbar → **Shell → Update changes**. Or restart Windows Explorer.
