# Comments

Comments can be used to explain Shell code, and to make it more readable. They can also be used to prevent execution of Shell code. Comments can be single-lined or multi-lined.

## Single-line Comments

Single-line comments start with two forward slashes (`//`). Any text between `//` and the end of the line is ignored (will not be executed).

### Before a line of code:

```nss
dynamic 
{
	// This is a comment
	item(title='Hello World!')
	
	//item(title='Hello World!')
}
```

### At the end of a line of code:

```nss
dynamic 
{
    item(title='Hello World!') // This is a comment
}
```

## Multi-line Comments

Multi-line comments start with `/*` and end with `*/`. Any text between `/*` and `*/` will be ignored.

```nss
dynamic
{
	item(title='Hello, /* multiple-lines comment inside */ world')
	
	/*
	item(title='test item 1')
	item(title='test item 2')
	*/
}
```

## Single or Multi-line Comments?

It is up to you which to use. Normally, use `//` for short comments, and `/* */` for longer ones.
