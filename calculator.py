"""A simple terminal calculator.

Supports addition, subtraction, multiplication, division, powers, square
roots, percentages, and decimal-to-binary conversion for whole numbers.
Type 'h' at the operation prompt to view this session's history.
Type 'q' (or 'quit' / 'exit') at any prompt to stop the program.
"""

import math
from typing import List

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

QUIT_COMMANDS = {"q", "quit", "exit"}
HISTORY_COMMANDS = {"h", "history"}
BINARY_COMMANDS = {"b", "bin", "binary"}
POWER_COMMANDS = {"^", "**", "pow", "power"}
SQRT_COMMANDS = {"s", "sqrt", "root"}
PERCENT_COMMANDS = {"p", "percent", "%"}


# ---------------------------------------------------------------------------
# Arithmetic operations
# ---------------------------------------------------------------------------

def add(left: float, right: float) -> float:
    """Return left + right."""
    return left + right


def subtract(left: float, right: float) -> float:
    """Return left - right."""
    return left - right


def multiply(left: float, right: float) -> float:
    """Return left * right."""
    return left * right


def divide(left: float, right: float) -> float:
    """Return left / right.

    Raises:
        ZeroDivisionError: if right is zero.
    """
    if right == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return left / right


def power(base: float, exponent: float) -> float:
    """Return base raised to exponent.

    Raises:
        ValueError: if zero is raised to a negative power, or if the
            result is not a real number.
        OverflowError: if the result is too large to represent.
    """
    if base == 0 and exponent < 0:
        raise ValueError("Zero cannot be raised to a negative power.")

    try:
        result = base ** exponent
    except OverflowError:
        raise OverflowError("The result is too large to display.")

    # A negative base with a fractional exponent produces a complex number.
    if isinstance(result, complex):
        raise ValueError("The result is not a real number.")

    return result


def square_root(value: float) -> float:
    """Return the square root of a non-negative number.

    Raises:
        ValueError: if value is negative.
    """
    if value < 0:
        raise ValueError("Cannot take the square root of a negative number.")
    return math.sqrt(value)


def percentage(percent: float, amount: float) -> float:
    """Return `percent` percent of `amount`."""
    return amount * percent / 100


# Maps each supported symbol to a human-readable name and its function.
OPERATIONS = {
    "+": ("addition", add),
    "-": ("subtraction", subtract),
    "*": ("multiplication", multiply),
    "/": ("division", divide),
    "^": ("power", power),
}


# ---------------------------------------------------------------------------
# Control flow helpers
# ---------------------------------------------------------------------------

class QuitRequested(Exception):
    """Raised when the user asks to leave the calculator."""


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def format_number(value: float) -> str:
    """Format a number for display without ugly floating-point artifacts."""
    if math.isfinite(value) and value.is_integer() and abs(value) < 1e16:
        return str(int(value))
    return f"{value:.12g}"


def format_calculation(left: float, operator: str,
                       right: float, result: float) -> str:
    """Return a one-line expression such as '12 + 3 = 15'."""
    return (f"{format_number(left)} {operator} "
            f"{format_number(right)} = {format_number(result)}")


def format_conversion(value: int, binary: str) -> str:
    """Return a one-line conversion record such as '42 in binary = 101010'."""
    return f"{value} in binary = {binary}"


def format_square_root(value: float, result: float) -> str:
    """Return a one-line square-root record such as 'sqrt(9) = 3'."""
    return f"sqrt({format_number(value)}) = {format_number(result)}"


def format_percentage(percent: float, amount: float, result: float) -> str:
    """Return a one-line percentage record such as '20% of 150 = 30'."""
    return (f"{format_number(percent)}% of {format_number(amount)} "
            f"= {format_number(result)}")


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------

def read_operator() -> str:
    """Prompt for an operation until a supported symbol is entered.

    Returns a symbol from OPERATIONS, 's' for square root, 'p' for
    percentage, 'b' for binary conversion, or 'h' to show history.
    """
    while True:
        choice = input(
            "Operation (+, -, *, /, ^, s, p, b, h) or q to quit: "
        ).strip().lower()

        if choice in QUIT_COMMANDS:
            raise QuitRequested
        if choice in HISTORY_COMMANDS:
            return "h"
        if choice in BINARY_COMMANDS:
            return "b"
        if choice in SQRT_COMMANDS:
            return "s"
        if choice in PERCENT_COMMANDS:
            return "p"
        if choice in POWER_COMMANDS:
            return "^"
        if choice in OPERATIONS:
            return choice

        print(f"  Error: '{choice}' is not a valid choice. "
              "Please choose +, -, *, /, ^, s, p, b, h, or q.")


def read_number(label: str) -> float:
    """Prompt for a finite number, re-prompting until the input is valid."""
    while True:
        raw = input(f"Enter the {label}: ").strip()

        if raw.lower() in QUIT_COMMANDS:
            raise QuitRequested

        if not raw:
            print("  Error: input cannot be empty. Please enter a number.")
            continue

        try:
            value = float(raw)
        except ValueError:
            print(f"  Error: '{raw}' is not a valid number. "
                  "Try something like 12, -3.5, or 1e6.")
            continue

        if not math.isfinite(value):
            print("  Error: enter a finite number "
                  "(infinity and NaN are not supported).")
            continue

        return value


def read_integer(label: str) -> int:
    """Prompt for a whole number, re-prompting until the input is valid."""
    while True:
        raw = input(f"Enter the {label}: ").strip()

        if raw.lower() in QUIT_COMMANDS:
            raise QuitRequested

        if not raw:
            print("  Error: input cannot be empty. "
                  "Please enter a whole number.")
            continue

        try:
            return int(raw)
        except ValueError:
            print(f"  Error: '{raw}' is not a whole number. "
                  "Try something like 42 or -7.")


def calculate(left: float, operator: str, right: float) -> float:
    """Apply the selected operation to two numbers."""
    _, operation = OPERATIONS[operator]
    return operation(left, right)


def to_binary(value: int) -> str:
    """Return the binary representation of a whole number.

    Negative numbers use a leading minus sign, for example -10 -> '-1010'.
    """
    return format(value, "b")


# ---------------------------------------------------------------------------
# User interface
# ---------------------------------------------------------------------------

def show_menu() -> None:
    """Print the list of available operations."""
    print("Available operations:")
    print("  +  addition")
    print("  -  subtraction")
    print("  *  multiplication")
    print("  /  division")
    print("  ^  power")
    print("  s  square root")
    print("  p  percentage (x% of y)")
    print("  b  convert a number to binary")
    print("  h  show calculation history")
    print("  q  quit")
    print()


def show_history(history: List[str]) -> None:
    """Print every successful calculation recorded this session."""
    if not history:
        print("  No calculations yet.")
        print()
        return

    print("  Calculation history:")
    for index, entry in enumerate(history, start=1):
        print(f"  {index}. {entry}")
    print()


def record_entry(history: List[str], entry: str) -> None:
    """Add a formatted result to the session history and print it."""
    history.append(entry)
    print(f"  {entry}")
    print()


def main() -> None:
    """Run the calculator until the user quits."""
    print("=" * 40)
    print(" Terminal Calculator")
    print("=" * 40)
    show_menu()

    # History lives only in memory, so it is cleared when the program exits.
    history: List[str] = []

    try:
        while True:
            operator = read_operator()

            if operator == "h":
                show_history(history)
                continue

            if operator == "b":
                number = read_integer("whole number to convert")
                entry = format_conversion(number, to_binary(number))
                record_entry(history, entry)
                continue

            if operator == "s":
                number = read_number("number")
                try:
                    result = square_root(number)
                except ValueError as error:
                    print(f"  Error: {error}")
                    print()
                    continue
                record_entry(history, format_square_root(number, result))
                continue

            if operator == "p":
                percent = read_number("percentage")
                amount = read_number("amount")
                result = percentage(percent, amount)
                record_entry(
                    history,
                    format_percentage(percent, amount, result),
                )
                continue

            if operator == "^":
                first_label, second_label = "base", "exponent"
            else:
                first_label, second_label = "first number", "second number"

            first = read_number(first_label)
            second = read_number(second_label)

            try:
                result = calculate(first, operator, second)
            except ZeroDivisionError:
                print("  Error: division by zero is not allowed. "
                      "Try a different divisor.")
                print()
                continue
            except (OverflowError, ValueError) as error:
                print(f"  Error: {error}")
                print()
                continue

            entry = format_calculation(first, operator, second, result)
            history.append(entry)

            description = OPERATIONS[operator][0]
            print(f"  Result ({description}): {entry}")
            print()
    except QuitRequested:
        pass
    except (EOFError, KeyboardInterrupt):
        # Leave the prompt on a clean line when the user presses Ctrl+C / Ctrl+D.
        print()

    print("Goodbye!")


if __name__ == "__main__":
    main()
