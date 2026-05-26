# Syntax Rules for Configuration Files

This chapter describes the syntax rules for the configuration files.

The main configuration file `shell.nss` is located in the installation directory of Shell, depending on your installation method.

## General Rules

- Syntax is case-insensitive.
- Spaces around the equal (`=`) sign are optional and are ignored.
- The properties of modify-items and new-items items are separated by blank spaces or on a separate line and must be placed in parentheses `( )`.
- Other configuration files can be imported using the `import` tag.

> **Tip:** When there is an error, it is recorded in the log file (`shell.log`, which is also located in your installation directory).

## shell.nss Structure

The global section `shell{}` may have the following subsections:

- **Section `settings{}`** — Optional.
- **Section modify-items** with instructions on how to change existing menuitems — Optional.
  - modify-items are only of 2 types: `modify` and `remove`.
- **Section modify-items** with definitions for new menuitems — Optional.
  - Dynamic menuitems may have one of three types: `menu`, `item`, or `separator` (sep).

### Example

```nss
// variable declaration
$variable-name = variable-value

// image declaration
@image-id = image-value
	
settings
{
	key-name = key-value
	key-name = [key-value, key-value, ...]
	...
}

theme
{
	key-name = key-value
	...
}

// modify items
modify ( property-name = property-value   ... )
remove ( property-name = property-value   ... )

// new items
item ( property-name = property-value   ... )

separator [( property-name = property-value   ... )]

menu ( property-name = property-value   ... )
{
	$variable-name = variable-value
	
	item ( property-name = property-value   ... )
	...
}
```

## Breaking Long Lines

For best readability, users often like to avoid lines longer than 80 characters. Single quotes also allow breaking up a line.

```nss
item(title='Command prompt'
	cmd='cmd.exe')
```

## Import Tag

To better organise the configuration file, parts of the configuration can be saved in separate files. These are then imported using the `import` tag. With this method, it is also possible to import the same file as a sort of "module" into different parts of the configuration — a convenient way to include the same sub-menu in different locations.

### Syntax

The general syntax is as follows:

```
import %path%
```

Where:

- `%section%` is the name of a section — **Optional**. If given, it must be one of:
  - `settings`
  - `themes`
  - `modify-items`
  - `new-items`
  
  The section name is written literally, without any quotes (or the percent signs).

- `%path%` is a string literal that returns the path to the config file that shall be imported. This can be a relative path to the location of the file where the `import` tag is used, or it can be an absolute path. Expressions are supported when using single quotes.

There are effectively two different ways this tag is applied, depending on whether the optional `%section%` is given.

### Import an Entire Section

```
// import an entire section
import %path%
```

In this case, the content of the file found at `%path%` will be imported into a newly created `section{}`. The result would then look like so:

```
// import an entire section
section {
	/* content of the imported file goes here! Do not include
	 *
	 * section {
	 * }
	 *
	 * in your imported file!
	 */
}
```

This syntax may be used only in the following places:

- Root section `shell{}`: `shell import %path%`
- The global sections:
  - `settings{}`: `import %path%`
- Sub-sections of the `settings{}` section:
  - `theme.background{}`: `background import %path%`
  - `theme.item{}`: `item import %path%`
  - `theme.border{}`: `border import %path%`
  - ...
  - `settings.tip{}`: `tip import %path%`
  - `settings.exclude{}`: `exclude import %path%`
  - `settings.modify{}`: `static import %path%`
  - `settings.new{}`: `dynamic import %path%`

### Import as a Partial

```
section {
	// some code might go here. Optional.

	// import of a partial section
	import %path%

	// some more content might go here. Optional.
}
```

In this case, the content of the file found at `%path%` will be imported into the already existing `section{}`. The result would then look like so:

```
section {
	// some code might go here. Optional.

	// import of a partial section
	/* content of the imported file goes here! Do not include
	 *
	 * section {
	 * }
	 *
	 * in your imported file!
	 */

	// some more content might go here. Optional.
}
```

This syntax may be used nearly anywhere:

- In any section
- In the body of menu tags
