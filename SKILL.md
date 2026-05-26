# Nilesoft Shell - LLM Skill

You are helping with a **Nilesoft Shell** project that customizes Windows File Explorer context menus. Below is everything you need to understand the project and make changes correctly.

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
- Comments: `//` for single line.
- Strings: single or double quotes, or bare words.
- Colors: `#RRGGBB` or `#RRGGBBAA`.
- Variables: `$name = value`, referenced as `@name` or `$(name)`.
- Conditional: `@if(condition, true_val, false_val)`.
- Predefined scopes: `icon.`, `id.`, `title.`, `color.`, `sys.`, `user.`, `sel.`, `io.`, `str.`, `cmd.`, `command.`, `process.`, `window.`.

## Theme Syntax
```nss
theme
{
    name="modern"           // modern, classic, white, black
    dark=auto               // auto, true, false
    view=view.compact       // auto, compact, small, medium, large, wide
    background
    {
        color=#hex          // base color
        opacity=0-100
        effect=0-3          // 0=solid, 1=transparent, 2=blur, 3=acrylic
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
    layout { rtl=true/false popup=-20-20 }
    image.align=N           // 0=check only, 1=image only, 2=both
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

// Multiple mode (checkboxes)
menu(mode="multiple" title='Choices')
{
    item(title='A')
    item(title='B')
}

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
- `@sel.type` — selected item type (1=file, 2=dir, 4=drive)
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

## GUI App
`theme-tweaker.py` is a Streamlit app that provides visual editing for themes, items, modify rules, settings, and imports.
- Run with: `streamlit run theme-tweaker.py`
- Opens at `http://localhost:8501`

## Reloading
After any `.nss` change, user must reload: **Ctrl + right-click** desktop/taskbar → **Shell → Update changes**, or restart Windows Explorer.

## Error Checking
- Check `shell.log` for parse errors.
- Errors show file name and line number.

## Official Docs
https://nilesoft.org/docs
