"""Tests de integración del intérprete de DragonScript."""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dragonscript import run_source_capture
from dragonscript.errors import (UndefinedVariableError, DivisionByZeroError,
                                 StackOverflowError_, ArgumentError, TypeErrorDS)


class TestInterpreter(unittest.TestCase):
    def run_code(self, code):
        return run_source_capture(code)

    # -------------------------------------------------- programa objetivo
    def test_primer_programa(self):
        code = """
KI power = 9000
SCOUTER power
IF power > 8000 {
    SCOUTER "¡Es más de 8000!"
}
"""
        self.assertEqual(self.run_code(code), "9000\n¡Es más de 8000!\n")

    # ---------------------------------------------------------- básicos
    def test_hello(self):
        self.assertEqual(self.run_code('SCOUTER "Hola"'), "Hola\n")

    def test_arithmetic(self):
        self.assertEqual(self.run_code("SCOUTER 2 + 3 * 4"), "14\n")

    def test_integer_division_exact(self):
        self.assertEqual(self.run_code("SCOUTER 10 / 2"), "5\n")

    def test_float_result(self):
        self.assertEqual(self.run_code("SCOUTER 7 / 2"), "3.5\n")

    def test_modulo(self):
        self.assertEqual(self.run_code("SCOUTER 10 % 3"), "1\n")

    def test_string_concatenation(self):
        self.assertEqual(self.run_code('SCOUTER "Nivel: " + 9000'), "Nivel: 9000\n")

    def test_booleans(self):
        self.assertEqual(self.run_code("SCOUTER TRUE"), "TRUE\n")
        self.assertEqual(self.run_code("SCOUTER NOT TRUE"), "FALSE\n")

    def test_logical_operators(self):
        self.assertEqual(self.run_code("SCOUTER TRUE AND FALSE"), "FALSE\n")
        self.assertEqual(self.run_code("SCOUTER FALSE OR TRUE"), "TRUE\n")

    # ------------------------------------------------------- control flow
    def test_if_else(self):
        code = """
KI x = 5
IF x > 10 {
    SCOUTER "grande"
} ELSE {
    SCOUTER "pequeño"
}
"""
        self.assertEqual(self.run_code(code), "pequeño\n")

    def test_else_if(self):
        code = """
KI x = 5
IF x > 10 {
    SCOUTER "a"
} ELSE IF x > 3 {
    SCOUTER "b"
} ELSE {
    SCOUTER "c"
}
"""
        self.assertEqual(self.run_code(code), "b\n")

    def test_while(self):
        code = """
KI i = 0
WHILE i < 3 {
    SCOUTER i
    i += 1
}
"""
        self.assertEqual(self.run_code(code), "0\n1\n2\n")

    def test_gravity(self):
        code = 'GRAVITY 3 {\n SCOUTER "x"\n}'
        self.assertEqual(self.run_code(code), "x\nx\nx\n")

    # ---------------------------------------------------------- funciones
    def test_function_call(self):
        code = """
TECHNIQUE entrenar(g, c) {
    RETURN g + c
}
SCOUTER entrenar(1000, 500)
"""
        self.assertEqual(self.run_code(code), "1500\n")

    def test_recursion_factorial(self):
        code = """
TECHNIQUE factorial(n) {
    IF n <= 1 {
        RETURN 1
    }
    RETURN n * factorial(n - 1)
}
SCOUTER factorial(5)
"""
        self.assertEqual(self.run_code(code), "120\n")

    def test_builtin_functions(self):
        self.assertEqual(self.run_code("SCOUTER ABS(-7)"), "7\n")
        self.assertEqual(self.run_code("SCOUTER MAX(3, 9, 5)"), "9\n")

    def test_arrays(self):
        code = "KI a = [10, 20, 30]\nSCOUTER a[1]\nSCOUTER LEN(a)"
        self.assertEqual(self.run_code(code), "20\n3\n")

    def test_compound_assignments(self):
        code = "KI x = 10\nx += 5\nx -= 2\nx *= 2\nSCOUTER x"
        self.assertEqual(self.run_code(code), "26\n")

    # ------------------------------------------------------------- errores
    def test_undefined_variable(self):
        with self.assertRaises(UndefinedVariableError):
            self.run_code("SCOUTER no_existe")

    def test_division_by_zero(self):
        with self.assertRaises(DivisionByZeroError):
            self.run_code("SCOUTER 1 / 0")

    def test_wrong_argument_count(self):
        code = "TECHNIQUE f(a, b) {\n RETURN a\n}\nSCOUTER f(1)"
        with self.assertRaises(ArgumentError):
            self.run_code(code)

    def test_type_error(self):
        with self.assertRaises(TypeErrorDS):
            self.run_code('SCOUTER 5 - "hola"')

    def test_stack_overflow(self):
        code = """
TECHNIQUE infinito(n) {
    RETURN infinito(n + 1)
}
SCOUTER infinito(1)
"""
        with self.assertRaises(StackOverflowError_):
            self.run_code(code)


if __name__ == "__main__":
    unittest.main()
