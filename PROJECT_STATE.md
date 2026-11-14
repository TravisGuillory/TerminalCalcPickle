# Project State: Terminal Calculator

_Last updated: 2026-11-14_

## Overview

A dependency-free Python calculator that runs in the terminal. It evaluates one
operation at a time, keeps a session history in memory, and exits cleanly when
the user quits or interrupts the program.

**Status at a glance**

- Required features: complete
- Tests: 66 passing
- Runtime dependencies: none (standard library only)
- Python compatibility: 3.8+
- Persistence: none; history is per-session only
- Required work outstanding: none

## File map

```
TerminalCalcPickle/
├── .gitignore          # ignores caches, local environments, and tooling files
├── calculator.py       # application code
├── test_calculator.py  # 66 unit and integration tests
├── README.md           # user-facing usage and setup
└── PROJECT_STATE.md    # architecture, decisions, and backlog (this file)
```

## Architecture

`calculator.py` is a single module organized into clearly commented sections:

1. **Configuration** - command aliases as module constants
   (`QUIT_COMMANDS`, `HISTORY_COMMANDS`, `BINARY_COMMANDS`, `POWER_COMMANDS`,
   `SQRT_COMMANDS`, `PERCENT_COMMANDS`).
2. **Arithmetic operations** - pure functions: `add`, `subtract`, `multiply`,
   `divide`, `power`, `square_root`, `percentage`. They do not read input or
   print, which makes them directly unit-testable.
3. **Dispatch table** - `OPERATIONS` maps each binary symbol to a display name
   and callable:

   ```python
   OPERATIONS = {
       "+": ("addition", add),
       "-": ("subtraction", subtract),
       "*": ("multiplication", multiply),
       "/": ("division", divide),
       "^": ("power", power),
   }
   ```

4. **Control flow** - `QuitRequested` is raised when the user types a quit
   command at any prompt.
5. **Formatting** - `format_number`, `format_calculation`,
   `format_conversion`, `format_square_root`, `format_percentage` keep all
   display formatting in one place.
6. **Input helpers** - `read_operator`, `read_number`, and `read_integer`
   validate input in retry loops and support quitting mid-entry.
7. **User interface** - `show_menu`, `show_history`, and `record_entry`.
8. **Entry point** - `main()` owns the loop and the session history list.

### Control flow

```text
main()
├── show_menu()
├── read_operator()
│   ├── "h" ─────────────► show_history(history)
│   ├── "b" ─────────────► read_integer → to_binary → format_conversion → record_entry
│   ├── "s" ─────────────► read_number → square_root → format_square_root → record_entry
│   ├── "p" ─────────────► read_number x2 → percentage → format_percentage → record_entry
│   └── + - * / ^ ───────► read_number x2 → calculate() → format_calculation
│                                                   → append history → print
└── repeat until quit
```

History is a plain `List[str]` created in `main()`. Each entry is a formatted
one-line string such as `12 + 3 = 15`, `sqrt(9) = 3`, or
`42 in binary = 101010`. Only successful operations are appended.

### Error handling model

| Signal | Source | Handling |
|---|---|---|
| `QuitRequested` | `q`, `quit`, or `exit` at any prompt | Exit the main loop cleanly |
| `EOFError` / `KeyboardInterrupt` | Ctrl+D / Ctrl+C | Print a newline and `Goodbye!` |
| `ZeroDivisionError` | Division by zero | Friendly message; nothing recorded; loop continues |
| `ValueError` | Invalid domain (negative root, non-real power, zero to negative power) | Friendly message; nothing recorded; loop continues |
| `OverflowError` | Result too large to represent | Friendly message; nothing recorded; loop continues |
| Invalid text/empty input | Input helpers | Print a specific message and re-prompt |

## Supported commands

| Command | Aliases | Inputs | Output example |
|---|---|---|---|
| `+` | - | two numbers | `12 + 3 = 15` |
| `-` | - | two numbers | `10 - 4 = 6` |
| `*` | - | two numbers | `6 * 7 = 42` |
| `/` | - | two numbers | `7 / 2 = 3.5` |
| `^` | `**`, `pow`, `power` | base, exponent | `2 ^ 10 = 1024` |
| `s` | `sqrt`, `root` | one non-negative number | `sqrt(9) = 3` |
| `p` | `percent`, `%` | percentage, amount | `20% of 150 = 30` |
| `b` | `bin`, `binary` | one whole number | `42 in binary = 101010` |
| `h` | `history` | none | Numbered session history |
| `q` | `quit`, `exit` | none | Exits |

## Key decisions and rationale

- **Single-module application.** The scope is small, so a package structure
  would add ceremony without benefit. Sections and pure functions provide
  organization.
- **Pure calculation functions.** Arithmetic functions take numbers and return
  numbers or raise errors. This keeps I/O concerns in `main()` and makes the
  logic easy to test.
- **Dispatch table for binary operations.** Adding a binary arithmetic
  operation requires a function plus one `OPERATIONS` entry, and the menu,
  prompt, and history automatically stay consistent.
- **Special commands handled explicitly in `main()`.** Unary and non-arithmetic
  actions (square root, binary conversion, percentage, history) have different
  input shapes, so they use their own branches instead of being forced into the
  two-operand model.
- **Floats for general arithmetic, integers for binary conversion.**
  `read_number()` parses finite floats and rejects `inf`/`nan`. `read_integer()`
  uses `int()` so binary conversion accepts arbitrary-size whole numbers and
  rejects decimals instead of silently truncating them.
- **`QuitRequested` exception.** A single exception lets `q` work at every
  prompt without duplicating quit checks or returning sentinel values.
- **Validation loops at the input boundary.** Bad input never reaches the
  calculation layer; users get specific, actionable messages and can retry.
- **Session history stored as formatted strings.** Display, history, and
  numbering stay identical, and no persistence or serialization is needed.
- **History is intentionally in-memory.** The requirement is "current
  session"; exiting clears it. This avoids file permissions and cleanup
  concerns.
- **`format_number()` uses 12 significant digits** and strips `.0` for whole
  values. This hides binary floating-point noise (`0.1 + 0.2` displays `0.3`)
  while keeping normal decimal output readable.
- **Sign-magnitude binary for negatives.** `-10` displays as `-1010` rather
  than a machine-width two's-complement representation, which is clearer for a
  general-purpose calculator.
- **Percent means "x% of y".** This is the most common calculator use case and
  is reflected in the output format. `%` is consequently a percentage command,
  not modulo.
- **Zero third-party dependencies.** Tests use `unittest`, `unittest.mock`, and
  `contextlib.redirect_stdout`, so the project runs anywhere Python 3.8+ is
  available.
- **ASCII-only console output** for portability across Windows, macOS, and
  Linux terminals.

## Testing

`test_calculator.py` is organized by responsibility:

- `ArithmeticTests`, `PowerTests`, `SquareRootTests`, `PercentageTests`
- `CalculateDispatchTests`
- `FormatNumberTests`, `FormattingTests`
- `BinaryConversionTests`
- `OperatorInputTests`, `NumberInputTests`, `IntegerInputTests`
- `MenuHistoryTests`
- `MainLoopTests` (full interactive sessions, history, error paths, EOF/Ctrl+C)

Every function in `calculator.py` is exercised directly or through `main()`.
Run the suite with:

```bash
python -m unittest -v
```

or:

```bash
python test_calculator.py
```

## Known limitations

- Arithmetic uses binary floats, so results beyond ~15-17 significant digits
  lose precision; binary conversion avoids this via integer parsing.
- No expression parser, parentheses, or operator precedence; each calculation
  is a single operation on one or two values.
- Previous results cannot be reused (`Ans`) or chained.
- No modulo, nth roots, logarithms, trigonometry, or statistics.
- History cannot be cleared, exported, or persisted between runs.
- Binary conversion is one-way and only handles base 2.
- The UI is English-only and not configurable.
- There is no CI pipeline, linter configuration, coverage report, or packaged
  entry point.
- The folder is not currently a Git repository; `.gitignore` is ready for when
  one is initialized, and generated `__pycache__/` files exist locally.

## Remaining tasks

**Required:** none. All requested functionality, validation, documentation, and
tests are complete.

**Optional backlog** (not committed work; useful next steps if the project
continues):

| Priority | Task | Notes |
|---|---|---|
| Medium | Add a `clear history` command | Small change to `main()` plus tests and README |
| Medium | Persist history to a JSON file | Opt-in file storage; still keep session behavior by default |
| Medium | Support result reuse (`Ans`) and chained calculations | Requires extending the input grammar beyond fixed operands |
| Medium | Add more math operations | Modulo, nth root, logarithms, trigonometry |
| Low | Add percentage modes | "What percent of", percent change/increase |
| Low | Support more number bases | Binary input, hexadecimal/octal output |
| Low | Improve numeric input ergonomics | Thousands separators, fractions, unary expressions |
| Low | Add CI and quality tooling | Run tests on push; add coverage and a linter |
| Low | Package as an installable command | `pyproject.toml` with a console-script entry point |
| Low | Initialize Git repository | `.gitignore` already covers caches and local files |

When adding a binary operation: implement a pure function, register it in
`OPERATIONS`, add aliases in `read_operator()`, update the menu/prompt, then add
tests and README docs. For a unary/special command: add a command set and
`main()` branch, a formatter, a history entry, and matching tests.
