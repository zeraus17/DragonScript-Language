"""Tests del analizador léxico (Lexer) de DragonScript."""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dragonscript.lexer import tokenize
from dragonscript.tokens import TokenType
from dragonscript.errors import LexerError


def types(source):
    """Devuelve la lista de tipos de token (sin NEWLINE ni EOF)."""
    return [t.type for t in tokenize(source)
            if t.type not in (TokenType.NEWLINE, TokenType.EOF)]


class TestLexer(unittest.TestCase):
    def test_keywords(self):
        toks = types("KI SCOUTER IF ELSE WHILE GRAVITY TECHNIQUE RETURN "
                     "AND OR NOT TRUE FALSE NULL")
        self.assertEqual(toks, [
            TokenType.KI, TokenType.SCOUTER, TokenType.IF, TokenType.ELSE,
            TokenType.WHILE, TokenType.GRAVITY, TokenType.TECHNIQUE,
            TokenType.RETURN, TokenType.AND, TokenType.OR, TokenType.NOT,
            TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
        ])

    def test_numbers_int_and_float(self):
        toks = tokenize("9000 3.14")
        nums = [t for t in toks if t.type == TokenType.NUMBER]
        self.assertEqual(nums[0].value, 9000)
        self.assertIsInstance(nums[0].value, int)
        self.assertEqual(nums[1].value, 3.14)
        self.assertIsInstance(nums[1].value, float)

    def test_string_utf8(self):
        toks = tokenize('SCOUTER "¡Es más de 8000!"')
        strings = [t for t in toks if t.type == TokenType.STRING]
        self.assertEqual(strings[0].value, "¡Es más de 8000!")

    def test_string_unclosed_raises(self):
        with self.assertRaises(LexerError):
            tokenize('SCOUTER "sin cerrar')

    def test_identifier(self):
        toks = tokenize("KI power = 9000")
        ident = [t for t in toks if t.type == TokenType.IDENTIFIER]
        self.assertEqual(ident[0].lexeme, "power")

    def test_operators(self):
        toks = types("+ - * / % == != < > <= >= = ( ) { } [ ] , . ->")
        self.assertEqual(toks, [
            TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH,
            TokenType.PERCENT, TokenType.EQ, TokenType.NEQ, TokenType.LT,
            TokenType.GT, TokenType.LTE, TokenType.GTE, TokenType.ASSIGN,
            TokenType.LPAREN, TokenType.RPAREN, TokenType.LBRACE,
            TokenType.RBRACE, TokenType.LBRACKET, TokenType.RBRACKET,
            TokenType.COMMA, TokenType.DOT, TokenType.ARROW,
        ])

    def test_compound_assignment_operators(self):
        toks = types("+= -= *= /=")
        self.assertEqual(toks, [
            TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN,
            TokenType.STAR_ASSIGN, TokenType.SLASH_ASSIGN,
        ])

    def test_comments_are_ignored(self):
        toks = types("# esto es un comentario\nKI x = 1")
        self.assertEqual(toks, [
            TokenType.KI, TokenType.IDENTIFIER, TokenType.ASSIGN,
            TokenType.NUMBER,
        ])

    def test_newline_tokens(self):
        toks = tokenize("KI x = 1\nSCOUTER x")
        self.assertTrue(any(t.type == TokenType.NEWLINE for t in toks))
        self.assertEqual(toks[-1].type, TokenType.EOF)

    def test_unknown_character_raises_thematic_error(self):
        with self.assertRaises(LexerError) as ctx:
            tokenize("KI x = 5 @ 3")
        self.assertIn("Scouter", str(ctx.exception))

    def test_line_tracking(self):
        toks = tokenize("KI x = 1\nKI y = 2")
        y_tokens = [t for t in toks if t.lexeme == "y"]
        self.assertEqual(y_tokens[0].line, 2)


if __name__ == "__main__":
    unittest.main()
