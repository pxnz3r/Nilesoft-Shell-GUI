# String Literal

A string is zero or more characters written inside single or double quotes.

You can use quotes inside a string, as long as they don't match the quotes surrounding the string:

```nss
$var1 = "It's alright"
$var2 = "He is called 'Johnny'"
$var3 = 'He is called "Johnny"'
```

## Single Quotes

Single quotes allow you to use the syntax of expressions within them. The `@` sign must be placed before the expressions.

```nss
item(title = 'windows dir path: @sys.dir')
```

## Double Quotes

Double quotes allow you to use the Escape Character inside them only. The backslash (`\`) escape character turns special characters into other characters.

The sequence `\"` inserts a double quote in a string:

```nss
$var1 = "hello\"world"
// result: hello"world
```

### Escape Sequences

| Sequence | Description |
|---|---|
| `\'` | Single quote |
| `\"` | Double quote |
| `\\` | Backslash |
| `\0` | Null |
| `\a` | Alert |
| `\b` | Backspace |
| `\f` | Form Feed |
| `\n` | New Line |
| `\r` | Carriage Return |
| `\t` | Horizontal Tab |
| `\v` | Vertical Tab |
| `\uHHHH` | Unicode escape sequence (UTF-16) — range: `0000` – `FFFF` |
| `\xnnnn` | Unicode escape for character with hex value `nnnn` (variable length version of `\u`) |
| `\U00HHHHHH` | Unicode escape sequence (UTF-32) — range: `000000` – `10FFFF` |
