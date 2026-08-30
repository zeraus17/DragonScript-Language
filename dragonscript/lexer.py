"""
lexer.py
========
Analizador léxico (tokenizador) de DragonScript.

Convierte el código fuente (texto) en una lista de :class:`Token`. Soporta
números enteros y flotantes, cadenas UTF-8 (con acentos y signos ¡ ¿),
identificadores y palabras clave, operadores aritméticos, de comparación y de
asignación compuesta, comentarios con ``#`` y saltos de línea como
separadores de sentencias.
"""

from __future__ import annotations

from .tokens import Token, TokenType, KEYWORDS
from .errors import LexerError


class Lexer:
    """Tokenizador de un solo paso sobre el texto fuente."""

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: list[Token] = []

    # ------------------------------------------------------------------ utils
    def _peek(self, offset: int = 0) -> str:
        idx = self.pos + offset
        if idx < len(self.source):
            return self.source[idx]
        return "\0"

    def _advance(self) -> str:
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def _at_end(self) -> bool:
        return self.pos >= len(self.source)

    def _add(self, type_: TokenType, lexeme: str, value=None, col: int | None = None):
        self.tokens.append(
            Token(type_, lexeme, value, self.line, col if col is not None else self.column))

    # ------------------------------------------------------------------ main
    def tokenize(self) -> list[Token]:
        """Devuelve la lista completa de tokens, terminada en EOF."""
        while not self._at_end():
            self._scan_token()
        # Aseguramos un NEWLINE final para simplificar el parser, y luego EOF.
        if self.tokens and self.tokens[-1].type != TokenType.NEWLINE:
            self._add(TokenType.NEWLINE, "\\n")
        self._add(TokenType.EOF, "")
        return self.tokens

    def _scan_token(self) -> None:
        start_col = self.column
        ch = self._advance()

        # Espacios en blanco (excepto salto de línea) -> ignorar
        if ch in " \t\r":
            return

        # Salto de línea -> separador de sentencias
        if ch == "\n":
            # Evitamos NEWLINE duplicados consecutivos.
            if self.tokens and self.tokens[-1].type != TokenType.NEWLINE:
                self._add(TokenType.NEWLINE, "\\n", col=start_col)
            return

        # Comentarios con '#'
        if ch == "#":
            while not self._at_end() and self._peek() != "\n":
                self._advance()
            return

        # Cadenas
        if ch == '"':
            self._string(start_col)
            return

        # Números
        if ch.isdigit():
            self._number(ch, start_col)
            return

        # Identificadores / keywords
        if ch.isalpha() or ch == "_":
            self._identifier(ch, start_col)
            return

        # Operadores y delimitadores
        self._operator(ch, start_col)

    # ------------------------------------------------------------- literales
    def _string(self, start_col: int) -> None:
        chars: list[str] = []
        while not self._at_end() and self._peek() != '"':
            c = self._advance()
            if c == "\\":  # secuencias de escape sencillas
                nxt = self._advance()
                chars.append({"n": "\n", "t": "\t", '"': '"',
                              "\\": "\\"}.get(nxt, nxt))
            else:
                chars.append(c)
        if self._at_end():
            raise LexerError("Cadena sin cerrar (falta comilla doble)", self.line)
        self._advance()  # consumir la comilla de cierre
        self._add(TokenType.STRING, '"' + "".join(chars) + '"',
                  value="".join(chars), col=start_col)

    def _number(self, first: str, start_col: int) -> None:
        num = [first]
        is_float = False
        while not self._at_end() and self._peek().isdigit():
            num.append(self._advance())
        if self._peek() == "." and self._peek(1).isdigit():
            is_float = True
            num.append(self._advance())  # el punto
            while not self._at_end() and self._peek().isdigit():
                num.append(self._advance())
        text = "".join(num)
        value = float(text) if is_float else int(text)
        self._add(TokenType.NUMBER, text, value=value, col=start_col)

    def _identifier(self, first: str, start_col: int) -> None:
        chars = [first]
        while not self._at_end() and (self._peek().isalnum() or self._peek() == "_"):
            chars.append(self._advance())
        text = "".join(chars)
        type_ = KEYWORDS.get(text, TokenType.IDENTIFIER)
        self._add(type_, text, col=start_col)

    # ----------------------------------------------------------- operadores
    def _operator(self, ch: str, start_col: int) -> None:
        def match(expected: str) -> bool:
            if self._peek() == expected:
                self._advance()
                return True
            return False

        # Punto '.' o rango '..' (para [1..10])
        if ch == ".":
            if match("."):
                self._add(TokenType.DOTDOT, "..", col=start_col)
            else:
                self._add(TokenType.DOT, ".", col=start_col)
            return

        # Delimitadores y operadores de un solo carácter.
        simple = {
            "(": TokenType.LPAREN, ")": TokenType.RPAREN,
            "{": TokenType.LBRACE, "}": TokenType.RBRACE,
            "[": TokenType.LBRACKET, "]": TokenType.RBRACKET,
            ",": TokenType.COMMA,
            ":": TokenType.COLON,
            "%": TokenType.PERCENT,
        }
        if ch in simple:
            self._add(simple[ch], ch, col=start_col)
            return

        if ch == "+":
            self._add(TokenType.PLUS_ASSIGN if match("=") else TokenType.PLUS,
                      "+=" if self.source[self.pos - 1] == "=" else "+", col=start_col)
            return
        if ch == "-":
            if match("="):
                self._add(TokenType.MINUS_ASSIGN, "-=", col=start_col)
            elif match(">"):
                self._add(TokenType.ARROW, "->", col=start_col)
            else:
                self._add(TokenType.MINUS, "-", col=start_col)
            return
        if ch == "*":
            self._add(TokenType.STAR_ASSIGN if match("=") else TokenType.STAR,
                      "*=" if self.source[self.pos - 1] == "=" else "*", col=start_col)
            return
        if ch == "/":
            self._add(TokenType.SLASH_ASSIGN if match("=") else TokenType.SLASH,
                      "/=" if self.source[self.pos - 1] == "=" else "/", col=start_col)
            return
        if ch == "=":
            self._add(TokenType.EQ if match("=") else TokenType.ASSIGN,
                      "==" if self.source[self.pos - 1] == "=" else "=", col=start_col)
            return
        if ch == "!":
            if match("="):
                self._add(TokenType.NEQ, "!=", col=start_col)
                return
            raise LexerError(f"Carácter desconocido: '!' en línea {self.line}",
                             self.line)
        if ch == "<":
            self._add(TokenType.LTE if match("=") else TokenType.LT,
                      "<=" if self.source[self.pos - 1] == "=" else "<", col=start_col)
            return
        if ch == ">":
            self._add(TokenType.GTE if match("=") else TokenType.GT,
                      ">=" if self.source[self.pos - 1] == "=" else ">", col=start_col)
            return

        raise LexerError(f"Carácter desconocido: '{ch}' en línea {self.line}",
                         self.line)


def tokenize(source: str) -> list[Token]:
    """Función de conveniencia: tokeniza una cadena fuente."""
    return Lexer(source).tokenize()
