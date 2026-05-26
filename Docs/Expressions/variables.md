# Variables

Variables are containers for storing data values.

Global and local variables are optional. To declare more than one variable, use a space.

## Naming Rules

The general rules for constructing names for variables (unique identifiers) are:

- Names can contain letters, digits, and underscores (`_`).
- Names must begin with a letter.
- Names cannot contain whitespaces or special characters like `!`, `#`, `%`, etc.
- Reserved words (like keywords, such as `null`, `true`, `false`, etc.) cannot be used as names.
- Variables can be placed in global variables, or in the dynamic body section of a menu, or in both.
- All variables must be identified with unique names.
- These unique names are called **identifiers**. Identifiers can be short names (like `x` and `y`) or more descriptive names (`age`, `sum`, `totalVolume`).

> **Note:** It is recommended to use descriptive names in order to create understandable and maintainable code.

## Example

```nss
$hello_world = 'Hello World!'
$test_add1 = 5 + 6

item(title = hello_world cmd = msg(hello_world))

menu(title = test_add1)
{
	$test_sub1 = 11 - 5
	item(title = test_sub1)
}
```
