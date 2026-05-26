# Modify Items

The optional modify section contains entries to modify existing context menu items, added by the system or by a third party.

## Sub-items

The section can have the following entry types, all of which are optional:

- One or more **item** entries. These contain the instructions on which and how to change existing menuitems.
- One or more **imports**. The content of the given file will be placed in the position of the import.

### Example

In the following example, two instructions are defined:

```nss
modify(find = 'copy' image = #00ff00)
modify(find = 'paste' image = #0000ff)
remove(find = '"format"')
```

## Item Entries

Item entries contain the instructions on how to identify existing menuitems (also referred to as **Target**), and when and what changes should be applied to them.

This is done by matching an existing menuitem's title property against the modify item's mandatory `find` property. If a match is found, the other properties of the modify item are applied to the appropriate menuitem, such as changing their properties (e.g. title, icon, visibility), or moving them to another location.

### Syntax

```nss
modify( find = value [property = value [...] ])
```

### Properties

Item entries can define three different sets of properties:

- **Validation Properties** — Determine if a given item entry should be processed when a context menu is displayed. Optional.
- **Filter Properties** — Determine if a given menuitem is a valid target for the process instructions:
  - `find` (mandatory) — Pattern used to identify targets by matching against their title property.
  - `in` — Used to identify targets by specifying the submenu in which they are located.
- **Process Instructions** — Define what to do with the target. Optional. However, if there are no process instruction specified, the entry is of no practical use.

For a complete overview and further details regarding applicable properties, please refer to the [properties page](properties.md).

## Item Target

Item targets are menuitems of an existing context menu. Their properties or location can be changed by applying the process instructions defined in a modify item.

## Process Instructions

Instructions that should be applied to the Target. Basically they consist of properties from the two property classes: **menuitem properties** and **command properties**.

Once an item is validated and a target identified, then these values are applied to the targeted menuitem.
