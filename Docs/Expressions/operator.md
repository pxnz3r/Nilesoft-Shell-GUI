# Operators

An operator is a symbol that tells Shell to perform specific mathematical or logical manipulations. Shell is rich in built-in operators and provides the following types:

- Arithmetic Operators
- Relational Operators
- Logical Operators
- Bitwise Operators
- Assignment Operators
- Conditional Operator

This chapter examines each one by one.

## Arithmetic Operators

The five arithmetical operations supported:

| Operator | Description |
|---|---|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |
| `%` | Modulo |

## Relational and Comparison Operators

Two expressions can be compared using relational and equality operators. The result of such an operation is either `true` or `false` (a Boolean value).

| Operator | Description |
|---|---|
| `==` | Equal to |
| `!=` | Not equal to |
| `<` | Less than |
| `>` | Greater than |
| `<=` | Less than or equal to |
| `>=` | Greater than or equal to |

## Logical Operators

The logical operators `&&` and `||` are used when evaluating two expressions to obtain a single relational result.

| Operator | Description |
|---|---|
| `&&` | Logical AND. If both operands are non-zero, condition becomes true. |
| `\|\|` | Logical OR. If any of the two operands is non-zero, condition becomes true. |
| `!` | Logical NOT. Reverses the logical state of its operand. |

### NOT Examples

```nss
!(5 == 5)   // evaluates to false (5 == 5 is true)
!(6 <= 4)   // evaluates to true (6 <= 4 would be false)
!true       // evaluates to false
!false      // evaluates to true
```

## Conditional Ternary Operator

The conditional operator evaluates an expression, returning one value if that expression evaluates to true, and a different one if it evaluates to false.

```nss
condition ? result1 : result2
```

If `condition` is true, the expression evaluates to `result1`, otherwise to `result2`.

### Examples

```nss
7==5 ? 4 : 3     // evaluates to 3, since 7 != 5
7==5+2 ? 4 : 3   // evaluates to 4, since 7 == 5+2
5>3 ? a : b      // evaluates to the value of a, since 5 > 3
a>b ? a : b      // evaluates to whichever is greater
```

## Bitwise Operators

Bitwise operators modify variables considering the bit patterns of the values they store.

| Operator | Description |
|---|---|
| `&` | Bitwise AND |
| `\|` | Bitwise inclusive OR |
| `^` | Bitwise exclusive OR |
| `~` | Unary complement (bit inversion) |
| `<<` | Shift bits left |
| `>>` | Shift bits right |

## Precedence of Operators

A single expression may have multiple operators. For example:

```nss
x = 5 + 7 % 2    // assigns 6 to x, because % has higher precedence than +
```

Parts of expressions can be enclosed in parentheses to override precedence order, or to make the intended effect explicit:

```nss
x = 5 + (7 % 2)    // x = 6 (same as without parenthesis)
x = (5 + 7) % 2    // x = 0
```

### Precedence Table

From greatest to smallest priority, operators are evaluated in the following order:

| Level | Group | Operator | Description | Associativity |
|---|---|---|---|---|
| 1 | Postfix (unary) | `++` `--` | Postfix increment / decrement | Left-to-right |
| | | `()` | Functional forms | |
| | | `[]` | Subscript | |
| | | `.` | Member access | |
| 2 | Prefix (unary) | `++` `--` | Prefix increment / decrement | Right-to-left |
| | | `~` `!` | Bitwise NOT / logical NOT | |
| | | `+` `-` | Unary prefix | |
| 4 | Arithmetic | `*` `/` `%` | Multiply, divide, modulo | Left-to-right |
| 5 | Arithmetic | `+` `-` | Addition, subtraction | Left-to-right |
| 6 | Bitwise shift | `<<` `>>` | Shift left, shift right | Left-to-right |
| 7 | Relational | `<` `>` `<=` `>=` | Comparison | Left-to-right |
| 8 | Equality | `==` `!=` | Equality / inequality | Left-to-right |
| 9 | Bitwise AND | `&` | Bitwise AND | Left-to-right |
| 10 | Exclusive or | `^` | Bitwise XOR | Left-to-right |
| 11 | Inclusive or | `\|` | Bitwise OR | Left-to-right |
| 12 | Logical AND | `&&` | Logical AND | Left-to-right |
| 13 | Logical OR | `\|\|` | Logical OR | Left-to-right |
| 15 | Assignment | `=` | Assignment | Right-to-left |
| | | `?:` | Conditional operator | |
| 16 | Sequencing | `,` | Comma separator | Left-to-right |

When an expression has two operators with the same precedence level, associativity determines which one is evaluated first (left-to-right or right-to-left).

> Enclosing sub-statements in parentheses (even those unnecessary because of precedence) improves code readability.
