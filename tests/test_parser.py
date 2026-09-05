"""Tests del analizador sintáctico (Parser) de DragonScript."""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dragonscript.lexer import tokenize
from dragonscript.parser import parse
from dragonscript import ast_nodes as ast
from dragonscript.errors import ParserError


def build(source):
    return parse(tokenize(source))


class TestParser(unittest.TestCase):
    def test_ki_declaration(self):
        prog = build("KI power = 9000")
        self.assertIsInstance(prog.statements[0], ast.KIDeclaration)
        self.assertEqual(prog.statements[0].name, "power")
        self.assertIsInstance(prog.statements[0].value, ast.NumberLiteral)

    def test_scouter(self):
        prog = build('SCOUTER "hola"')
        self.assertIsInstance(prog.statements[0], ast.Scouter)
        self.assertIsInstance(prog.statements[0].expression, ast.StringLiteral)

    def test_operator_precedence(self):
        # 2 + 3 * 4 => 2 + (3 * 4)
        prog = build("KI x = 2 + 3 * 4")
        expr = prog.statements[0].value
        self.assertIsInstance(expr, ast.BinaryOp)
        self.assertEqual(expr.operator, "+")
        self.assertIsInstance(expr.right, ast.BinaryOp)
        self.assertEqual(expr.right.operator, "*")

    def test_comparison_precedence(self):
        # 1 + 2 > 3 => (1 + 2) > 3
        prog = build("KI x = 1 + 2 > 3")
        expr = prog.statements[0].value
        self.assertEqual(expr.operator, ">")
        self.assertIsInstance(expr.left, ast.BinaryOp)
        self.assertEqual(expr.left.operator, "+")

    def test_if_else_if_else(self):
        prog = build(
            "IF x > 1 {\n SCOUTER 1\n} ELSE IF x > 0 {\n SCOUTER 2\n} ELSE {\n SCOUTER 3\n}")
        node = prog.statements[0]
        self.assertIsInstance(node, ast.IfStatement)
        self.assertEqual(len(node.elif_branches), 1)
        self.assertIsNotNone(node.else_branch)

    def test_while(self):
        prog = build("WHILE i < 3 {\n i += 1\n}")
        self.assertIsInstance(prog.statements[0], ast.WhileStatement)

    def test_gravity(self):
        prog = build('GRAVITY 5 {\n SCOUTER "hola"\n}')
        node = prog.statements[0]
        self.assertIsInstance(node, ast.GravityStatement)
        self.assertIsInstance(node.count, ast.NumberLiteral)

    def test_technique_declaration_and_call(self):
        prog = build("TECHNIQUE suma(a, b) {\n RETURN a + b\n}\nSCOUTER suma(1, 2)")
        decl = prog.statements[0]
        self.assertIsInstance(decl, ast.TechniqueDeclaration)
        self.assertEqual(decl.params, ["a", "b"])
        call = prog.statements[1].expression
        self.assertIsInstance(call, ast.TechniqueCall)
        self.assertEqual(len(call.arguments), 2)

    def test_compound_assignment(self):
        prog = build("KI i = 0\ni += 5")
        node = prog.statements[1]
        self.assertIsInstance(node, ast.CompoundAssignment)
        self.assertEqual(node.operator, "+=")

    def test_member_access(self):
        prog = build("SCOUTER GOKU.KI")
        expr = prog.statements[0].expression
        self.assertIsInstance(expr, ast.MemberAccess)
        self.assertEqual(expr.member, "KI")

    def test_array_and_index(self):
        prog = build("KI a = [1, 2, 3]\nSCOUTER a[0]")
        self.assertIsInstance(prog.statements[0].value, ast.ArrayLiteral)
        self.assertIsInstance(prog.statements[1].expression, ast.IndexAccess)

    def test_syntax_error_is_thematic(self):
        with self.assertRaises(ParserError) as ctx:
            build("KI = 5")
        self.assertIn("Ki Sintáctico", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
