# Nilesoft Shell - Project Context

## Overview
This project customizes Windows File Explorer context menus using [Nilesoft Shell](https://nilesoft.org/docs) — a high-performance, open-source extension. Configuration is done via `.nss` files.

## File Structure
```
The script folder\
├── shell.nss                  # Main entry point — imports all modules
├── shell.exe / shell.dll      # Nilesoft Shell runtime
├── shell.log                  # Error log (check this if something breaks)
├── theme-tweaker.py           # Streamlit GUI for visual editing
├── AGENTS.md                  # This file — context for LLMs
├── SKILL.md                   # LLM skill instructions for Nilesoft Shell
│
└── imports/
    ├── theme.nss              # Visual theme (colors, gradient, font, shadow, border)
    ├── modify.nss             # Reorder/hide system context menu items
    ├── custom.nss             # Custom user-defined menu items
    ├── images.nss             # SVG icon definitions
    ├── terminal.nss           # Terminal/command prompt entries
    ├── file-manage.nss        # File operations (copy path, attributes, etc.)
    ├── develop.nss            # Dev tools (VS Code, dotnet commands)
    ├── goto.nss               # Quick navigation shortcuts
    └── taskbar.nss            # Taskbar-specific menu items
```

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

## Reloading
After editing any `.nss` file: hold **Ctrl + right-click** on desktop/taskbar → **Shell → Update changes**. Or restart Windows Explorer.

## GUI App
`theme-tweaker.py` is a Streamlit GUI at `http://localhost:8501`. Run with:
```
streamlit run theme-tweaker.py
```

## Common System Item IDs
`id.copy_as_path`, `id.properties`, `id.send_to`, `id.share`, `id.create_shortcut`, `id.pin_to_start`, `id.unpin_from_start`, `id.open_powershell_window_here`, `id.format`, `id.eject`, `id.restore_previous_versions`, `id.cast_to_device`, `id.empty_recycle_bin`, `id.rotate_left`, `id.rotate_right`, `id.give_access_to`, `id.include_in_library`, `id.print`, `id.map_network_drive`, `id.disconnect_network_drive`, `id.customize_this_folder`
