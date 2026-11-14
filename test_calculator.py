"""Unit tests for every function in calculator.py."""

import io
import unittest
from contextlib import redirect_stdout
from unittest import mock

import calculator


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run_main(*inputs):
    """Run calculator.main() with scripted answers and return its output."""
    with mock.patch("builtins.input", side_effect=list(inputs)):
        with redirect_stdout(io.StringIO()) as output:
            calculator.main()
    return output.getvalue()


# ---------------------------------------------------------------------------
# Arithmetic functions
# ---------------------------------------------------------------------------

class ArithmeticTests(unittest.TestCase):
    """Tests for add, subtract, multiply, and divide."""

    def test_add(self):
        self.assertEqual(calculator.add(2, 3), 5)
        self.assertEqual(calculator.add(-2.5, 1), -1.5)

    def test_subtract(self):
        self.assertEqual(calculator.subtract(10, 4), 6)
        self.assertEqual(calculator.subtract(1, 3.5), -2.5)

    def test_multiply(self):
        self.assertEqual(calculator.multiply(6, 7), 42)
        self.assertEqual(calculator.multiply(-3, 2.5), -7.5)

    def test_divide(self):
        self.assertAlmostEqual(calculator.divide(7, 2), 3.5)

    def test_divide_negative_numbers(self):
        self.assertEqual(calculator.divide(-9, 3), -3)

    def test_divide_by_zero_raises(self):
        with self.assertRaises(ZeroDivisionError):
            calculator.divide(1, 0)


class PowerTests(unittest.TestCase):
    """Tests for power()."""

    def test_positive_exponent(self):
        self.assertEqual(calculator.power(2, 10), 1024)

    def test_power_fractional_exponent(self):
        self.assertAlmostEqual(calculator.power(9, 0.5), 3.0)

    def test_power_negative_exponent(self):
        self.assertEqual(calculator.power(2, -2), 0.25)

    def test_power_negative_base_with_integer_exponent(self):
        self.assertEqual(calculator.power(-2, 3), -8)

    def test_power_zero_exponent(self):
        self.assertEqual(calculator.power(7, 0), 1)

    def test_power_negative_base_fractional_exponent_is_not_real(self):
        with self.assertRaises(ValueError):
            calculator.power(-8, 0.5)

    def test_power_zero_to_negative_power_is_rejected(self):
        with self.assertRaises(ValueError):
            calculator.power(0, -1)

    def test_overflow_is_reported(self):
        with self.assertRaises(OverflowError):
            calculator.power(10.0, 1000.0)


class SquareRootTests(unittest.TestCase):
    """Tests for square_root()."""

    def test_perfect_square(self):
        self.assertEqual(calculator.square_root(9), 3)

    def test_zero(self):
        self.assertEqual(calculator.square_root(0), 0)

    def test_irrational_result(self):
        self.assertAlmostEqual(
            calculator.square_root(2), 1.41421356, places=6
        )

    def test_negative_number_is_rejected(self):
        with self.assertRaises(ValueError):
            calculator.square_root(-4)


class PercentageTests(unittest.TestCase):
    """Tests for percentage()."""

    def test_percentage_of_amount(self):
        self.assertEqual(calculator.percentage(20, 150), 30)

    def test_fractional_percentage(self):
        self.assertEqual(calculator.percentage(12.5, 200), 25)

    def test_negative_percentage(self):
        self.assertEqual(calculator.percentage(-10, 50), -5)


class CalculateDispatchTests(unittest.TestCase):
    """Tests for calculate(), which dispatches to an operation."""

    def test_dispatches_every_binary_operation(self):
        cases = {
            "+": (8, 3, 11),
            "-": (8, 3, 5),
            "*": (8, 3, 24),
            "/": (8, 2, 4),
            "^": (2, 3, 8),
        }
        for operator, (left, right, expected) in cases.items():
            with self.subTest(operator=operator):
                self.assertEqual(
                    calculator.calculate(left, operator, right),
                    expected,
                )

    def test_division_by_zero_propagates(self):
        with self.assertRaises(ZeroDivisionError):
            calculator.calculate(1, "/", 0)

    def test_power_error_propagates(self):
        with self.assertRaises(ValueError):
            calculator.calculate(-8, "^", 0.5)


# ---------------------------------------------------------------------------
# Formatting functions
# ---------------------------------------------------------------------------

class FormatNumberTests(unittest.TestCase):
    """Tests for format_number()."""

    def test_whole_numbers_lose_decimal_point(self):
        self.assertEqual(calculator.format_number(5.0), "5")
        self.assertEqual(calculator.format_number(-12.0), "-12")

    def test_floating_point_noise_is_hidden(self):
        self.assertEqual(calculator.format_number(0.1 + 0.2), "0.3")

    def test_fractional_values_keep_decimals(self):
        self.assertEqual(calculator.format_number(3.5), "3.5")

    def test_very_large_values_use_scientific_notation(self):
        self.assertEqual(calculator.format_number(1e20), "1e+20")


class FormattingTests(unittest.TestCase):
    """Tests for the calculation, conversion, root, and percentage formatters."""

    def test_format_calculation(self):
        self.assertEqual(
            calculator.format_calculation(12, "+", 3, 15),
            "12 + 3 = 15",
        )

    def test_format_calculation_uses_caret_for_power(self):
        self.assertEqual(
            calculator.format_calculation(2, "^", 10, 1024),
            "2 ^ 10 = 1024",
        )

    def test_format_conversion(self):
        self.assertEqual(
            calculator.format_conversion(42, "101010"),
            "42 in binary = 101010",
        )

    def test_format_negative_conversion(self):
        self.assertEqual(
            calculator.format_conversion(-10, "-1010"),
            "-10 in binary = -1010",
        )

    def test_format_square_root(self):
        self.assertEqual(
            calculator.format_square_root(9, 3),
            "sqrt(9) = 3",
        )

    def test_format_percentage(self):
        self.assertEqual(
            calculator.format_percentage(20, 150, 30),
            "20% of 150 = 30",
        )


# ---------------------------------------------------------------------------
# Binary conversion
# ---------------------------------------------------------------------------

class BinaryConversionTests(unittest.TestCase):
    """Tests for to_binary()."""

    def test_positive_number(self):
        self.assertEqual(calculator.to_binary(42), "101010")

    def test_zero(self):
        self.assertEqual(calculator.to_binary(0), "0")

    def test_negative_number(self):
        self.assertEqual(calculator.to_binary(-10), "-1010")


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------

class OperatorInputTests(unittest.TestCase):
    """Tests for read_operator()."""

    def test_accepts_every_operation_symbol(self):
        for symbol in ["+", "-", "*", "/", "^"]:
            with self.subTest(symbol=symbol):
                with mock.patch("builtins.input", return_value=symbol):
                    self.assertEqual(calculator.read_operator(), symbol)

    def test_accepts_command_aliases(self):
        cases = {
            "**": "^",
            "pow": "^",
            "power": "^",
            "s": "s",
            "sqrt": "s",
            "root": "s",
            "p": "p",
            "percent": "p",
            "%": "p",
            "b": "b",
            "bin": "b",
            "binary": "b",
            "h": "h",
            "history": "h",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                with mock.patch("builtins.input", return_value=text):
                    self.assertEqual(calculator.read_operator(), expected)

    def test_reprompts_after_invalid_choice(self):
        with mock.patch("builtins.input", side_effect=["x", "/"]):
            with redirect_stdout(io.StringIO()) as output:
                operator = calculator.read_operator()

        self.assertEqual(operator, "/")
        self.assertIn("not a valid choice", output.getvalue())

    def test_quits_with_each_quit_command(self):
        for command in ["q", "quit", "exit"]:
            with self.subTest(command=command):
                with mock.patch("builtins.input", return_value=command):
                    with self.assertRaises(calculator.QuitRequested):
                        calculator.read_operator()


class NumberInputTests(unittest.TestCase):
    """Tests for read_number()."""

    def test_accepts_whitespace_and_float(self):
        with mock.patch("builtins.input", return_value=" 3.5 "):
            self.assertEqual(calculator.read_number("first number"), 3.5)

    def test_accepts_negative_and_scientific_notation(self):
        for text, expected in [("-7", -7.0), ("1e3", 1000.0)]:
            with self.subTest(text=text):
                with mock.patch("builtins.input", return_value=text):
                    self.assertEqual(
                        calculator.read_number("number"), expected
                    )

    def test_reprompts_after_invalid_input(self):
        with mock.patch("builtins.input", side_effect=["abc", "2"]):
            with redirect_stdout(io.StringIO()) as output:
                value = calculator.read_number("first number")

        self.assertEqual(value, 2.0)
        self.assertIn("not a valid number", output.getvalue())

    def test_rejects_empty_input(self):
        with mock.patch("builtins.input", side_effect=["", "8"]):
            with redirect_stdout(io.StringIO()) as output:
                value = calculator.read_number("second number")

        self.assertEqual(value, 8.0)
        self.assertIn("cannot be empty", output.getvalue())

    def test_rejects_infinity_and_nan(self):
        with mock.patch("builtins.input", side_effect=["inf", "nan", "5"]):
            with redirect_stdout(io.StringIO()) as output:
                value = calculator.read_number("number")

        self.assertEqual(value, 5.0)
        self.assertEqual(output.getvalue().count("finite number"), 2)

    def test_quits(self):
        with mock.patch("builtins.input", return_value="q"):
            with self.assertRaises(calculator.QuitRequested):
                calculator.read_number("first number")


class IntegerInputTests(unittest.TestCase):
    """Tests for read_integer()."""

    def test_accepts_whitespace(self):
        with mock.patch("builtins.input", return_value=" 42 "):
            self.assertEqual(
                calculator.read_integer("whole number to convert"), 42
            )

    def test_accepts_negative_number(self):
        with mock.patch("builtins.input", return_value="-10"):
            self.assertEqual(
                calculator.read_integer("whole number to convert"), -10
            )

    def test_rejects_decimal(self):
        with mock.patch("builtins.input", side_effect=["3.5", "7"]):
            with redirect_stdout(io.StringIO()) as output:
                value = calculator.read_integer("number")

        self.assertEqual(value, 7)
        self.assertIn("not a whole number", output.getvalue())

    def test_rejects_empty_input(self):
        with mock.patch("builtins.input", side_effect=["", "7"]):
            with redirect_stdout(io.StringIO()) as output:
                value = calculator.read_integer("number")

        self.assertEqual(value, 7)
        self.assertIn("cannot be empty", output.getvalue())

    def test_quits(self):
        with mock.patch("builtins.input", return_value="q"):
            with self.assertRaises(calculator.QuitRequested):
                calculator.read_integer("number")


# ---------------------------------------------------------------------------
# Menu and history
# ---------------------------------------------------------------------------

class MenuHistoryTests(unittest.TestCase):
    """Tests for show_menu(), show_history(), and record_entry()."""

    def test_show_menu_lists_every_option(self):
        with redirect_stdout(io.StringIO()) as output:
            calculator.show_menu()

        text = output.getvalue()
        for line in [
            "Available operations:",
            "  +  addition",
            "  -  subtraction",
            "  *  multiplication",
            "  /  division",
            "  ^  power",
            "  s  square root",
            "  p  percentage (x% of y)",
            "  b  convert a number to binary",
            "  h  show calculation history",
            "  q  quit",
        ]:
            with self.subTest(line=line):
                self.assertIn(line, text)

    def test_show_history_when_empty(self):
        with redirect_stdout(io.StringIO()) as output:
            calculator.show_history([])

        self.assertIn("No calculations yet", output.getvalue())

    def test_show_history_numbers_entries_in_order(self):
        history = ["2 + 3 = 5", "7 / 2 = 3.5"]
        with redirect_stdout(io.StringIO()) as output:
            calculator.show_history(history)

        text = output.getvalue()
        self.assertIn("Calculation history", text)
        self.assertIn("1. 2 + 3 = 5", text)
        self.assertIn("2. 7 / 2 = 3.5", text)
        self.assertLess(text.index("1. 2 + 3 = 5"), text.index("2. 7 / 2 = 3.5"))

    def test_record_entry_appends_and_prints(self):
        history = []
        with redirect_stdout(io.StringIO()) as output:
            calculator.record_entry(history, "2 + 3 = 5")

        self.assertEqual(history, ["2 + 3 = 5"])
        self.assertIn("  2 + 3 = 5", output.getvalue())

    def test_record_entry_preserves_existing_entries(self):
        history = ["1 + 1 = 2"]
        with redirect_stdout(io.StringIO()):
            calculator.record_entry(history, "2 + 2 = 4")

        self.assertEqual(history, ["1 + 1 = 2", "2 + 2 = 4"])


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

class MainLoopTests(unittest.TestCase):
    """End-to-end tests for main()."""

    def test_arithmetic_session(self):
        text = run_main("+", "12", "3", "q")

        self.assertIn("Result (addition): 12 + 3 = 15", text)
        self.assertIn("Goodbye!", text)

    def test_can_quit_at_a_number_prompt(self):
        text = run_main("+", "q")

        self.assertIn("Goodbye!", text)
        self.assertNotIn("Result", text)

    def test_history_records_arithmetic(self):
        text = run_main("+", "2", "3", "/", "7", "2", "h", "q")

        self.assertIn("1. 2 + 3 = 5", text)
        self.assertIn("2. 7 / 2 = 3.5", text)
        self.assertIn("Goodbye!", text)

    def test_division_by_zero_is_not_recorded(self):
        text = run_main("/", "1", "0", "h", "q")

        self.assertIn("division by zero", text)
        self.assertIn("No calculations yet.", text)
        self.assertIn("Goodbye!", text)

    def test_binary_conversion_is_recorded(self):
        text = run_main("b", "42", "h", "q")

        self.assertIn("42 in binary = 101010", text)
        self.assertIn("1. 42 in binary = 101010", text)
        self.assertIn("Goodbye!", text)

    def test_advanced_operations_are_recorded(self):
        text = run_main("^", "2", "10", "s", "9", "p", "20", "150", "h", "q")

        self.assertIn("1. 2 ^ 10 = 1024", text)
        self.assertIn("2. sqrt(9) = 3", text)
        self.assertIn("3. 20% of 150 = 30", text)
        self.assertIn("Goodbye!", text)

    def test_invalid_advanced_operations_are_not_recorded(self):
        text = run_main("s", "-4", "^", "-8", "0.5", "h", "q")

        self.assertIn("Cannot take the square root of a negative number.", text)
        self.assertIn("The result is not a real number.", text)
        self.assertIn("No calculations yet.", text)
        self.assertIn("Goodbye!", text)

    def test_eof_exits_cleanly(self):
        with mock.patch("builtins.input", side_effect=EOFError):
            with redirect_stdout(io.StringIO()) as output:
                calculator.main()

        self.assertIn("Goodbye!", output.getvalue())

    def test_keyboard_interrupt_exits_cleanly(self):
        with mock.patch("builtins.input", side_effect=KeyboardInterrupt):
            with redirect_stdout(io.StringIO()) as output:
                calculator.main()

        self.assertIn("Goodbye!", output.getvalue())


if __name__ == "__main__":
    unittest.main()
