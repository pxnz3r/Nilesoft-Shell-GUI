# Nilesoft Shell - LLM Skill

You are helping with a **Nilesoft Shell** GUI project that lets users visually customize Windows File Explorer context menus. The GUI is a **Streamlit** app (`theme-tweaker.py`) that edits `.nss` configuration files.

## Project Location
The script folder — all `.nss` files live here and in `imports/`.

## Entry Points
- **`shell.nss`** — main config, imports all modules. Edit settings block here.
- **`imports/theme.nss`** — visual appearance (colors, gradients, fonts, borders, shadows).
- **`imports/modify.nss`** — rules to move/hide/organize system context menu items.
- **`imports/custom.nss`** — user-defined custom menu items.
- **`imports/images.nss`** — SVG icon definitions for menu icons.
- **`imports/terminal.nss`**, **`file-manage.nss`**, **`develop.nss`**, **`goto.nss`**, **`taskbar.nss`** — feature modules.

## NSS Language Basics
- Files use `.nss` extension, plain text.
- Blocks use `{ }` braces.
- Comments: `//` single line, `/* ... */` block.
- Strings: single or double quotes. Inside quotes, `@expr` interpolates (e.g. `args='"@sel.path"'`).
- Colors: `#RGB`, `#RRGGBB` or `#RRGGBBAA`.
- Variables: `$name = value`, referenced as `@name`.
- Conditional: `@if(condition, true_val, false_val)`.
- Predefined scopes: `icon.`, `id.`, `title.`, `color.`, `sys.`, `user.`, `sel.`, `io.`, `str.`, `cmd.`, `command.`, `process.`, `window.`.

## Theme Syntax
```nss
theme
{
    name="modern"           // modern, classic, white, black
    dark=default            // default, true, false
    view=view.compact       // auto, compact, small, medium, large, wide
    background
    {
        color=#hex          // base color
        opacity=0-100
        effect=0-3          // 0=disable, 1=transparent, 2=blur, 3=acrylic
        gradient
        {
            enabled=true
            linear=[x1, x2, y1, y2]     // or radial=[cx,cy,r,fx,fy]
            stop=[[offset, #hex], ...]
        }
    }
    item
    {
        opacity=0-100
        radius=0-3
        text { normal=#hex normal.disabled=#hex select=#hex select.disabled=#hex }
        back { normal=#hex normal.disabled=#hex select=#hex select.disabled=#hex }
        border { normal=#hex select=#hex }
        padding { left=N top=N right=N bottom=N }
        margin { left=N top=N right=N bottom=N }
    }
    border { enabled=true/false size=0-10 color=#hex opacity=0-100 radius=0-20 padding { ... } }
    shadow { enabled=true/false size=0-30 color=#hex opacity=0-100 offset=0-30 }
    font { size=6-24 name="fontname" weight=1-9 italic=0/1 }
    separator { size=0-40 color=#hex opacity=0-100 margin { ... } }
    image { enabled=true/false color=[#c1,#c2,#c3] gap=N glyph="font" scale=true/false align=0-2 }
                            // align: 0=check mark only, 1=image only, 2=both
    layout { rtl=true/false popup=-20..20 }
}
```

## Menu Item Syntax
```nss
// Basic item
item(title='Label' cmd='executable' args='arguments')

// With icon and admin
item(title='Notepad' cmd='notepad.exe' image=icon.notepad admin)

// With conditions
item(type='file' where=sel.count>0 title='Open' cmd='app.exe' args='@sel.path')

// Submenu
menu(title='Submenu' image=icon.folder)
{
    item(title='Option 1' cmd='cmd1')
    item(title='Option 2' cmd='cmd2')
}

// mode controls which selections show the menu: "single", "multi_unique", "multi_single", "multiple"
menu(mode="multiple" title='Tools')
{
    item(title='A' cmd='a.exe')
    item(title='B' cmd='b.exe')
}

// Separators: sep=sep.top / sep="bottom" / sep="both" on an item, or a bare `sep` line

// Available icons: icon.pin, icon.settings, icon.copy_path, icon.properties,
// icon.run_with_powershell, icon.task_manager, icon.folder_options, icon.new_folder,
// icon.new_file, icon.select_all, icon.share, icon.delete, etc.
```

## Modify Rules
```nss
// Hide an item
modify(where=this.id==id.restore_previous_versions vis=vis.remove)

// Move item to a custom menu
modify(where=this.id==id.copy_as_path menu="file manage")

// Move by name pattern
modify(find="unpin*" pos="bottom" menu="Pin/Unpin")

// Set position with separator
modify(type="dir.back|drive.back" where=this.id==id.customize_this_folder pos=1 sep="top" menu="file manage")

// Move multiple items at once
modify(mode=mode.multiple where=this.id(id.send_to, id.share, id.create_shortcut) pos=1 menu=title.more_options)
```
`pos`: `auto`, `top`, `middle`, `bottom`, or an integer. Target menus are matched by title (`menu="file manage"`).

## Settings Syntax
```nss
settings
{
    priority=1                      // Load order (higher = later)
    exclude.where = !process.is_explorer  // Only show in Explorer
    showdelay = 200                 // Milliseconds before menu appears
    modify.remove.duplicate=1       // Auto-remove duplicate items
    tip.enabled=true                // Show tooltips
}
```

## Useful Predefined Variables
- `@sel.path` — selected item path
- `@sel.dir` — selected item's directory
- `@sel.file.name` — selected file name
- `@sel.file.ext` — selected file extension
- `@sel.count` — number of selected items
- `@sys.dir` — Windows directory
- `@sys.bin` — System32 directory
- `@user.desktop` — Desktop path
- `@user.downloads` — Downloads path
- `@user.documents` — Documents path
- `@app.name` — Shell app name
- `@app.ver` — Shell version
- `@app.dir` — Shell directory
- `@app.cfg` — config file path
- `@theme.islight` — whether light theme is active

## GUI App (theme-tweaker.py)

`theme-tweaker.py` is a Streamlit app (1.50+) with tabs:
- **Menu Items** — build custom items with form inputs, append to custom.nss
- **Modify** — add hide/reorder rules for built-in items
- **Settings** — edit global shell.nss settings, view shell.log
- **Imports** — toggle imports, inline editor for any .nss file, syntax checker
- **Theme** — visual editor loaded from theme.nss, 10 presets, live menu preview
- **Icons** — preview all SVGs from images.nss in the theme's icon colors
- **Find** — search/replace across .nss files
- **Export** — package/restore config as zip
- **History** — restore previous backups

Key constants:
```python
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
THEME_PATH = os.path.join(_SCRIPT_DIR, "imports", "theme.nss")
CUSTOM_PATH = os.path.join(_SCRIPT_DIR, "imports", "custom.nss")
MODIFY_PATH = os.path.join(_SCRIPT_DIR, "imports", "modify.nss")
SHELL_PATH = os.path.join(_SCRIPT_DIR, "shell.nss")
IMPORTS_DIR = os.path.join(_SCRIPT_DIR, "imports")
BACKUP_DIR = os.path.join(_SCRIPT_DIR, "backups")
```

Key functions:
- `parse_theme()` — reads theme.nss into GUI state keys (runs on first load and on Reload)
- `load_theme_state()` — pushes values into widget state; call only from callbacks or before widgets render
- `current_stops()` — collects gradient stops from `num_stops` / `so_<i>` / `sc_<i>`
- `generate_theme()` — builds NSS theme code from session state values
- `backup_file()` — saves timestamped backup before overwrites
- `list_backups()` — returns sorted backup list for restore
- `parse_shell_settings()` — reads current settings from shell.nss
- `read_file_safe()` — reads files with UTF-8/CP1252 fallback

Theme widgets are bound by `key=` only; `st.session_state` is the source of truth.

## Reloading
After any `.nss` change, user must reload: **Ctrl + right-click** desktop/taskbar → **Shell → Update changes**, or restart Windows Explorer.

## Error Checking
- Check `shell.log` for parse errors (point GUI Settings tab to Shell install dir).
- Errors show file name and line number.

## Official Docs
https://nilesoft.org/docs
