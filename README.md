# Terminal Calculator

A small command-line calculator written in Python. It supports the four basic
arithmetic operations, powers, square roots, percentages, and binary
conversion, and keeps running until you tell it to quit.

## Features

- Addition (`+`), subtraction (`-`), multiplication (`*`), and division (`/`)
- Powers (`^`), including fractional and negative exponents
- Square roots (`s`)
- Percentages (`p`), calculated as x% of y
- Decimal-to-binary conversion for whole numbers (`b`)
- Continuous prompt loop: calculate as many times as you like
- Session history: view earlier calculations and conversions with `h`
- Input validation with friendly error messages
- Protection against division by zero, invalid roots, and non-real powers
- Clean result formatting (no `5.0` or `0.30000000000000004`)
- Quit at any prompt with `q`, `quit`, or `exit`
- Graceful exit on `Ctrl+C` / `Ctrl+D`

## Requirements

- Python 3.8 or newer (no third-party packages)

Check your version with:

```bash
python --version
```

On Windows you can usually use `py` instead of `python`.

## Project structure

```
TerminalCalcPickle/
├── .gitignore          # ignored caches, local files, and tooling artifacts
├── calculator.py       # the application
├── test_calculator.py  # unit tests
├── README.md           # this file
└── PROJECT_STATE.md    # architecture, decisions, and backlog
```

## How to run

1. Open a terminal in the project folder:

   ```bash
   cd TerminalCalcPickle
   ```

2. Start the calculator:

   ```bash
   python calculator.py
   ```

   Windows alternative:

   ```powershell
   py calculator.py
   ```

## Usage

```text
========================================
 Terminal Calculator
========================================
Available operations:
  +  addition
  -  subtraction
  *  multiplication
  /  division
  ^  power
  s  square root
  p  percentage (x% of y)
  b  convert a number to binary
  h  show calculation history
  q  quit

Operation (+, -, *, /, ^, s, p, b, h) or q to quit: +
Enter the first number: 12
Enter the second number: 3
  Result (addition): 12 + 3 = 15

Operation (+, -, *, /, ^, s, p, b, h) or q to quit: /
Enter the first number: 7
Enter the second number: 2
  Result (division): 7 / 2 = 3.5

Operation (+, -, *, /, ^, s, p, b, h) or q to quit: ^
Enter the base: 2
Enter the exponent: 10
  Result (power): 2 ^ 10 = 1024

Operation (+, -, *, /, ^, s, p, b, h) or q to quit: s
Enter the number: 9
  sqrt(9) = 3

Operation (+, -, *, /, ^, s, p, b, h) or q to quit: p
Enter the percentage: 20
Enter the amount: 150
  20% of 150 = 30

Operation (+, -, *, /, ^, s, p, b, h) or q to quit: b
Enter the whole number to convert: 42
  42 in binary = 101010

Operation (+, -, *, /, ^, s, p, b, h) or q to quit: h
  Calculation history:
  1. 12 + 3 = 15
  2. 7 / 2 = 3.5
  3. 2 ^ 10 = 1024
  4. sqrt(9) = 3
  5. 20% of 150 = 30
  6. 42 in binary = 101010

Operation (+, -, *, /, ^, s, p, b, h) or q to quit: q
Goodbye!
```

### Input rules

- Numbers may be whole numbers, decimals, or scientific notation
  (for example `42`, `-3.5`, `1e6`).
- Type `^` (or `**`) at the operation prompt for a power.
- Type `s` (or `sqrt`) at the operation prompt for a square root.
- Type `p` (or `percent` / `%`) at the operation prompt for a percentage.
- Type `b` (or `binary`) at the operation prompt to convert a number to binary.
- Type `h` (or `history`) at the operation prompt to view the session history.
- Type `q`, `quit`, or `exit` at any prompt to leave.
- Press `Ctrl+C` to exit immediately.

### Powers

Choose `^` (or type `**`), then enter a base and an exponent:

```text
Operation (+, -, *, /, ^, s, p, b, h) or q to quit: ^
Enter the base: 2
Enter the exponent: 10
  Result (power): 2 ^ 10 = 1024
```

- Fractional exponents are supported (`9 ^ 0.5` gives `3`).
- A negative base with a fractional exponent has no real result and is rejected.
- Zero cannot be raised to a negative power.
- Results that are too large to represent are reported as an error.

### Square roots

Choose `s` (or type `sqrt`), then enter a non-negative number:

```text
Operation (+, -, *, /, ^, s, p, b, h) or q to quit: s
Enter the number: 9
  sqrt(9) = 3
```

Square roots of negative numbers are rejected because the calculator only
handles real numbers.

### Percentages

Choose `p` (or type `percent` / `%`), then enter the percentage and the amount:

```text
Operation (+, -, *, /, ^, s, p, b, h) or q to quit: p
Enter the percentage: 20
Enter the amount: 150
  20% of 150 = 30
```

Fractional and negative percentages are allowed.

### Binary conversion

Choose `b` at the operation prompt, then enter a whole number. The result is
printed in base 2:

```text
Operation (+, -, *, /, ^, s, p, b, h) or q to quit: b
Enter the whole number to convert: 42
  42 in binary = 101010
```

- Only whole numbers are supported; decimals such as `3.5` are rejected with a
  helpful error message.
- Negative numbers use a leading minus sign (`-10` becomes `-1010`).
- Zero converts to `0`.

### Calculation history

Every successful operation is added to an in-memory list for the current
session, including arithmetic results, powers, square roots, percentages, and
binary conversions. Type `h` at the operation prompt to see the numbered
history.

History is not saved to disk, so it is cleared when the program exits. Failed
operations, such as division by zero or invalid input, are not recorded.

### Error handling

Invalid input never crashes the calculator. For example:

```text
Operation (+, -, *, /, ^, s, p, b, h) or q to quit: x
  Error: 'x' is not a valid choice. Please choose +, -, *, /, ^, s, p, b, h, or q.

Operation (+, -, *, /, ^, s, p, b, h) or q to quit: ^
Enter the base: -8
Enter the exponent: 0.5
  Error: The result is not a real number.

Operation (+, -, *, /, ^, s, p, b, h) or q to quit: s
Enter the number: -4
  Error: Cannot take the square root of a negative number.

Operation (+, -, *, /, ^, s, p, b, h) or q to quit: /
Enter the first number: 1
Enter the second number: 0
  Error: division by zero is not allowed. Try a different divisor.

Operation (+, -, *, /, ^, s, p, b, h) or q to quit: b
Enter the whole number to convert: 3.5
  Error: '3.5' is not a whole number. Try something like 42 or -7.
```

## Running the tests

The suite covers every function in `calculator.py`, including validation errors
and complete interactive sessions.

From the project folder:

```bash
python -m unittest -v
```

Or run the test file directly:

```bash
python test_calculator.py
```
