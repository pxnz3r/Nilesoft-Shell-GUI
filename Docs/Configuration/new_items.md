# New Items

Add new items to the context menu.

## Sub-items

The section can have the following entry types, all of which are optional:

- **Menuitems**, i.e. one or more of the following:
  - One or more `item` entries. These appear as top-level items in a context menu.
  - One or more `menu` entries. These appear as top-level sub-menus in a context menu.
  - One or more `separator` entries. These create a horizontal line between the given entries.
- One or more **imports**. The content of the given file will be placed in the position of the import.

### Example

In the following example, one top-level item is created, that is separated with a horizontal line from an adjacent sub-menu, which in turn has one sub-item on its own:

```nss
item(title = 'Hello, World!')
separator
menu(title = 'sub menu' image = #0000ff)
{
	item(title = 'test sub-item')
}
```

## Menuitems

Menuitem is an umbrella term for those entry types that may appear in a menu. These include the following:

- `item`
- `menu`
- `separator`

## Items

Items create a single menu entry.

### Properties

Either a `title` or an `image` property is mandatory (set to a non-null value). For further details, please refer to the [properties page](properties.md).

### Syntax

```nss
item( title = value [property = value [...] ])
```

## Menus

Menu entries create a new sub-menu. They have properties and sub-entries.

### Properties

Either a `title` or an `image` property is mandatory (set to a non-null value). For further details, please refer to the [properties page](properties.md).

### Sub-items

Menus can have the following entry types, all of which are optional:

- **Menuitems**, i.e. one or more of the following:
  - One or more `item` entries.
  - One or more sub-`menu` entries.
  - One or more `separator` entries. These create a horizontal line between the given entries.
- One or more **imports**. The content of the given file will be placed in the position of the import.

### Syntax

```nss
menu( title = value [property = value [...] ])
{
	[ item() [...] ]
	[ menu(){} [...] ]
	[ separator [...] ]
	[ import 'path/to/import.nss' [...] ]
}
```

## Separators

Separators create a horizontal line.

### Properties

Separators do not have any mandatory properties. Please refer to the [properties page](properties.md) for further details.

### Syntax

```nss
separator
separator( property = value [property = value [...] ])
```
