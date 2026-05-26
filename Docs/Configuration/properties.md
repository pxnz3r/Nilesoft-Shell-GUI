# Properties

Shell supports the following properties classes:

- **Validation Properties**
- **Filter Properties**
- **Menuitem Properties**
- **Command Properties**

Please also see the full [index](#index) of available properties below.

## Index

| Category | Properties |
|---|---|
| Command | `Admin`, `arg`, `args`, `Arguments` |
| Menuitem | `Checked`, `cmd`, `col`, `Column`, `Command` |
| Filter | `Default`, `dir`, `Directory` |
| Menuitem | `Expanded` |
| Filter | `Find` |
| Menuitem | `Icon`, `Image`, `Invoke`, `In` |
| Menuitem | `Keys` |
| Validation | `Mode`, `Menu` |
| Menuitem | `Parent`, `pos`, `Position` |
| Menuitem | `sep`, `Separator` |
| Menuitem | `Tip`, `Title`, `Type` |
| Menuitem | `Verb`, `vis`, `Visibility` |
| Validation | `Wait`, `Where`, `Window` |

## Entry Types

In the following tables, the **Types** column shows to which entry types the property applies to.

The following abbreviations are used (if set in **bold**, then the property is mandatory for the given type):

| Abbr | Meaning |
|---|---|
| **mi** | Modify item, i.e. the item entry itself. Is basically required to evaluate if the process instructions are applied to any given target. |
| mt | Modify target, i.e. the menuitem of the existing menu to which the process instructions are applied. |
| **nm** | New menu type. |
| **ni** | New item type. |
| ns | New separator type. |

## Validation Properties

Determine if a given Modify items or New items entry should be processed when a context menu is displayed.

### Properties

| Property | Types (*) | Summary |
|---|---|---|
| `Where` | mi, nm, ni, ns | Process given menuitem if `true` is returned. Allows the evaluation of arbitrary expressions, e.g. `if()`. Default = `true` |
| `Mode` | mi, nm, ni, ns | Display menuitem by **type of selection**. The value has one of the following parameters (of type string): |
| | | `none` — Display menuitem when there is no selection. |
| | | `single` — Display menuitem when there is a single object selected. |
| | | `multi_unique` — Display menuitem when multiple objects of the same type are selected. |
| | | `multi_single` — Display menuitem when multiple files with a single file extension are selected. |
| | | `multiple` — Display any type of selection, unless there is none. Default = `single` |
| `Type` | mi, nm, ni, ns | Specifies the **types of objects** for which the menuitem will be displayed. Separate multiple types with the pipe character (`\|`), in which case the menuitem is displayed if any of the given types is matched. To exclude a given type, prefix its value with the tilde character (`~`). Expressions are not supported with this property. |

#### Type Values

| Value | Description |
|---|---|
| `*` | Display menuitem when any type is selected. |
| `File` | Display menuitem when files are selected. |
| `Directory` (Dir) | Display menuitem when directories are selected. |
| `Drive` | Display menuitem when drives are selected. |
| `USB` | Display menuitem when USB flash-drives are selected. |
| `DVD` | Display menuitem when DVD-ROM drives are selected. |
| `Fixed` | Display menuitem when fixed drives are selected (e.g. hard disk drive or flash drive). |
| `VHD` | Display menuitem when Virtual Hard Disks are selected. |
| `Removable` | Display menuitem when the selected drives have removable media (e.g. floppy drive, thumb drive, or flash card reader). |
| `Remote` | Display menuitem when the selected remote (network) drives are selected. |
| `Back` | Display menuitem when the background of all types is selected (`back`). Or specify one of the following more granular types: |
| | `back.directory` |
| | `back.drive`, including `back.fixed`, `back.usb`, `back.dvd`, `back.vhd`, `back.Removable` |
| | `back.namespace`, including `back.computer`, `back.recyclebin` |
| `Desktop` | Display menuitem when the Desktop is selected. |
| `Namespace` | Display menuitem when Namespaces are selected (virtual objects such as My Network Places and Recycle Bin). |
| `Computer` | Display menuitem when My Computer is selected. |
| `Recyclebin` | Display menuitem when the Recycle bin is selected. |
| `Taskbar` | Display menuitem when the Taskbar is selected. |

Default = Accepts all types, except for the Taskbar.

## Filter Properties

For Modify items entries only, filter properties determine if a given menuitem is a valid target for the process instructions.

### Properties

| Property | Types (*) | Summary |
|---|---|---|
| `Find` | nm, ni, ns | **For modify items (required):** Apply the current item's process instructions to any existing menuitem if their title property matches the pattern of the current item's `find` property. **For dynamic items (optional):** Display the current menuitem if the pattern of its `find` property matches the path name or path extension of the selected files. Default = `null`, which means any string is "matched". |
| `In` | mi | Specifies the existing submenu where the modify target is located. Syntax: `in = "New"` / `in = "Sort By"` |

#### Find Syntax

```nss
find = '%pattern%'
find = '%pattern%|%pattern%[...]'
```

Where `%pattern%` can be one or more matching instructions. The following characters do have special meaning:

| Character | Meaning |
|---|---|
| `\|` | Use to separate patterns. If any one pattern matches, the property yields true. |
| `*` | Matches any number of characters. Used as a wildcard to match only the beginning or the end of the entire string (or word, if used in combination with `!`). |
| `!` | Negates the match of the current pattern, or limits the wildcard (`*`) to one word only. |
| `""` | The enclosed string is treated as a word. A word is a sequence of alphanumerical characters confined to the left and right by either a space, a non-word character (e.g. `/` or `-`), or the beginning/end of the entire string. |

##### Pattern Examples

| Pattern | Matches any string that… | Would match | Would not match |
|---|---|---|---|
| `'foo'` | contains the literal string `foo` anywhere | `foo`, `foobar`, `afoobar` | `fo`, `f oo`, `bar` |
| `'"foo"'` | contains `foo` as a whole word only | `foo`, `foo/bar`, `some foo bar` | `foobar`, `foofoo`, `bar` |
| `'*foo'` | ends with `foo` | `foo`, `barfoo`, `bar/foo` | `foobar`, `fooo`, `foo` |
| `'foo*'` | starts with `foo` | `foo`, `foobar`, `foo/bar` | `foobar`, `fo`, `yeti` |
| `'!foo'` | does NOT contain `foo` anywhere | `fobar`, `fo`, `kung-fu` | `foo`, `foobar`, `barfoo/bar` |
| `'!"foo"'` | does NOT contain the word `foo` | `fobar`, `kung fu bar`, `foobar` | `foo`, `kung foo bar`, `bar/foo/bar` |
| `'!*foo'` | does NOT contain a word ending with `foo` | `foobar`, `fooo-fo` | `foo`, `foo bar`, `bar/foo` |
| `'foo*!'` | does NOT contain a word starting with `foo` | `myFooBar`, `barFoo` | `foo`, `foobar`, `fo-fooo` |

##### File Extension Patterns

| Pattern | Matches | Would match | Would not match |
|---|---|---|---|
| `'.exe'` | equal to `.exe` | `setup.exe`, `notepad.exe` | `install.bat`, `shell.nss`, `shell.ex_`, files without extension |
| `'!.exe'` | not equal to `.exe` | `setup.exe.zip`, `video.mp4`, `shell.ex_`, files without extension | `setup.exe`, `shell.exe` |
| `'.exe\|.dll'` | equal to `.exe` or `.dll` | `shell.exe`, `shell.dll` | `shell.zip`, `shell.nss`, files without extension |

## Menuitem Properties

This set of properties describe the appearance and location of a given menuitem. For modify-items, this is the target menuitem. For dynamic entries, this is the newly created menuitem.

### Appearance

- `Checked`
- `Default`
- `Image`
- `Separator`
- `Tip`
- `Title`
- `Visibility`

### Location

- `Column`
- `Expanded`
- `Keys`
- `Menu`
- `Parent`
- `Position`

### Syntax

| Property | Types (*) | Summary |
|---|---|---|
| `Title` | st, nm, **ni** | Sets the caption of the menuitem. **For modify-items (optional):** Default = `null` (title is not changed). **For dynamic items (required):** Mandatory for menu and item entries, unless an `image` property is defined. |
| `Visibility` (vis) | st, nm, ni, ns | Sets the visibility of a menuitem. Can have one of the following parameters: `Hidden` — Hide the menuitem; `Normal` — Enable the menuitem; `Disable` — Disable the menuitem; `Static` — Display as label with/without image; `Label` — Display as label without image. Note: `Static` and `Label` are not available for modify-items. Default = `Normal` |
| `Separator` (sep) | st, nm, ni | Add a separator to the menuitem: `None` — No separator; `Before`, `Top` — Separator before; `After`, `Bottom` — Separator after; `Both` — Separator before and after. Default = `none` |
| `Position` (pos) | st, nm, ni, ns | The position at which a menuitem should be inserted: `Auto` — Current position; `Middle` — Middle of the menu; `Top` — Top of the menu; `Bottom` — Bottom of the menu; `Integer` — A specified position. Default = `auto` |
| `Image`, `Icon` | st, nm, **ni** | The icon that appears in a menuitem. Can be assigned as image files, resource icons, glyph, or color. Parameters: `null` — No icon; `Inherit` — Inherits from parent; `Cmd` — Assign from command property; `Glyph` — Assign as Glyph; `Color` — Assign as color; `Path` — Assign from location path or resource icon. Note: `Cmd` is not available for modify-items targets. Default = `null` |
| `Parent`, `Menu` | st, nm, ni, ns | Move current menuitem to another menu. Default = `null` |
| `Checked` | st, **ni** | Type of select option: `0` — Not checked; `1` — Display as check mark; `2` — Display as radio bullet. Default = `0` |
| `Default` | st, **ni** | Specifies that the item is the default (displayed in bold). A menu can contain only one default. Default = `false` |
| `Expanded` | **nm** | Move all immediate menuitems to the parent menu. Default = `false` |
| `Column` (col) | **nm**, **ni** | Create a new column. Default = `true` |
| `Keys` | st, nm, **ni** | Show keyboard shortcuts. Default = `null` |
| `Tip` | st, nm, **ni** | Show a tooltip for the current menu or item. Default = `null` |

#### Tip Syntax

```nss
tip = "Lorem Ipsum is simply dummy text."
tip = ["Lorem Ipsum is simply dummy text.", tip.info]
tip = ["Lorem Ipsum is simply dummy text.", tip.info, 1.2]
```

## Command Properties

This set of properties describe how a command is executed. Only available for dynamic items.

| Property | Types (*) | Summary |
|---|---|---|
| `Command` (cmd) | **ni** | The command associated with the menuitem. Occurs when the menuitem is clicked or selected. Default = `null` |
| `Arguments` (arg, args) | **ni** | The command line parameters to pass to the command property. Default = `null` |
| `Invoke` | **ni** | Set execution type: `0`, `single` — Execute only once; `1`, `multiple` — Execute once per item. Default = `0` |
| `Window` | **ni** | Controls how the window is shown: `Hidden`, `Show`, `Visible`, `Minimized`, `Maximized`. Default = `show` |
| `Directory` (dir) | **ni** | Specifies the working directory to execute the command in. Default = `null` |
| `Admin` | **ni** | Execute the command with administrative permissions. Default = `false` |
| `Verb` | **ni** | Specifies the default operation for the selected file. Values: `null` (default), `Open`, `OpenAs`, `RunAs`, `Edit`, `Explore`, `Properties`, `Print`, `Find`. Default = `open` |
| `Wait` | **ni** | Wait for the command to complete. Default = `false` |
