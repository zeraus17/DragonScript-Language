"""
tokens.py
=========
Definición de los tipos de token del lenguaje DragonScript.

Cada token producido por el Lexer es una instancia de :class:`Token`, que
almacena su tipo (:class:`TokenType`), el lexema original, un valor ya
convertido (para números) y la posición (línea y columna) para reportar
errores temáticos de Dragon Ball.
"""

from __future__ import annotations

from enum import Enum, auto


class TokenType(Enum):
    """Enumeración de todos los tipos de token soportados."""

    # --- Palabras clave (keywords) temáticas de Dragon Ball ---
    KI = auto()          # declaración de variable  -> let / var
    SCOUTER = auto()     # instrucción de salida     -> print
    ROSHI = auto()
    IF = auto()          # condicional (SENSAR)      -> if
    ELSE = auto()        # alternativa (SINO)        -> else
    WHILE = auto()       # bucle condicional (MIENTRAS) -> while
    FOREACH = auto()     # recorrido enumerativo (RASTREAR) -> for-each
    IN_ = auto()         # pertenencia en recorrido (EN)   -> in
    GRAVITY = auto()     # bucle "repetir N" (GRAVEDAD)    -> repeat N
    TECHNIQUE = auto()   # definición de función (TECNICA) -> def / function
    RETURN = auto()      # retorno de función (TRANSMITIR) -> return
    AND = auto()         # y lógico (FUSION)          -> and
    OR = auto()          # o lógico (DESEO)           -> or
    NOT = auto()         # negación lógica (INVERTIR) -> not
    TRUE = auto()        # literal verdadero (CANON)  -> true
    FALSE = auto()       # literal falso (RELLENO)    -> false
    NULL = auto()        # literal nulo (VACIO)       -> null / None

    # --- Palabras clave de POO (Programación Orientada a Objetos) ---
    # Temática: Corporación Cápsula. Una CAPSULA es el molde/plano (clase) y
    # ACTIVAR una cápsula produce un objeto concreto (instancia).
    WARRIOR = auto()     # definición de clase (CAPSULA)   -> class
    CREATE = auto()      # instanciación (ACTIVAR)         -> new
    EVOLVES = auto()     # herencia (EVOLUCIONA)           -> extends / inherits
    STATIC = auto()      # miembro estático/de clase (LEGENDARIO) -> static

    # --- Literales e identificadores ---
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()

    # --- Operadores aritméticos ---
    PLUS = auto()        # +
    MINUS = auto()       # -
    STAR = auto()        # *
    SLASH = auto()       # /
    PERCENT = auto()     # %

    # --- Operadores de comparación ---
    EQ = auto()          # ==
    NEQ = auto()         # !=
    LT = auto()          # <
    GT = auto()          # >
    LTE = auto()         # <=
    GTE = auto()         # >=

    # --- Asignación ---
    ASSIGN = auto()          # =
    PLUS_ASSIGN = auto()     # +=
    MINUS_ASSIGN = auto()    # -=
    STAR_ASSIGN = auto()     # *=
    SLASH_ASSIGN = auto()    # /=

    # --- Delimitadores ---
    LPAREN = auto()      # (
    RPAREN = auto()      # )
    LBRACE = auto()      # {
    RBRACE = auto()      # }
    LBRACKET = auto()    # [
    RBRACKET = auto()    # ]
    COMMA = auto()       # ,
    DOT = auto()         # .
    DOTDOT = auto()      # ..  (rangos: [1..10])
    COLON = auto()       # :
    ARROW = auto()       # ->

    # --- Especiales ---
    NEWLINE = auto()     # salto de línea (separador de sentencias)
    EOF = auto()         # fin de fichero


# Mapa de palabras reservadas -> tipo de token.
#
# DragonScript usa palabras reservadas TEMÁTICAS DEL UNIVERSO DRAGON BALL, en
# español. Para no romper programas antiguos, las palabras originales en inglés
# (IF, WHILE, ...) siguen aceptándose como *alias ocultos* del mismo token.
KEYWORDS = {
    # ---- Palabras temáticas oficiales (en español) ----
    "KI": TokenType.KI,                 # declarar variable (energía que guardás)
    "SCOUTER": TokenType.SCOUTER,       # mostrar / medir en pantalla
    "ROSHI": TokenType.ROSHI,
    "SENSAR": TokenType.IF,             # if      -> "sensar" el ki (comprobar)
    "ESQUIVAR": TokenType.ELSE,         # else    -> esquivar (si no se cumple)
    "ENTRENAR": TokenType.WHILE,        # while   -> entrenar mientras se cumpla
    "RASTREAR": TokenType.FOREACH,      # foreach -> rastrear cada elemento
    "EN": TokenType.IN_,                # in      -> RASTREAR x EN grupo
    "GRAVEDAD": TokenType.GRAVITY,      # repetir N veces (cámara de gravedad)
    "TECNICA": TokenType.TECHNIQUE,     # función / procedimiento
    "TRANSMITIR": TokenType.RETURN,     # return  -> teletransportar el resultado
    "FUSION": TokenType.AND,            # and     -> las dos se fusionan
    "DESEO": TokenType.OR,              # or      -> alcanza con un deseo
    "INVERTIR": TokenType.NOT,          # not     -> invertir (Time Reversal)
    "CANON": TokenType.TRUE,            # true    -> lo canónico
    "RELLENO": TokenType.FALSE,         # false   -> el relleno (filler)
    "VACIO": TokenType.NULL,            # null    -> la nada (Dead Zone)
    "CAPSULA": TokenType.WARRIOR,       # clase / registro (molde de Corp. Cápsula)
    "ACTIVAR": TokenType.CREATE,        # crear objeto (activar una cápsula)
    "EVOLUCIONA": TokenType.EVOLVES,    # herencia
    "LEGENDARIO": TokenType.STATIC,     # miembro estático / de clase

    # ---- Alias ocultos en inglés (compatibilidad hacia atrás) ----
    "IF": TokenType.IF,
    "ELSE": TokenType.ELSE,
    "WHILE": TokenType.WHILE,
    "GRAVITY": TokenType.GRAVITY,
    "TECHNIQUE": TokenType.TECHNIQUE,
    "RETURN": TokenType.RETURN,
    "AND": TokenType.AND,
    "OR": TokenType.OR,
    "NOT": TokenType.NOT,
    "TRUE": TokenType.TRUE,
    "FALSE": TokenType.FALSE,
    "NULL": TokenType.NULL,
    "WARRIOR": TokenType.WARRIOR,
    "CREATE": TokenType.CREATE,
    "INVOCAR": TokenType.CREATE,        # alias histórico de ACTIVAR
    "EVOLVES": TokenType.EVOLVES,
    "STATIC": TokenType.STATIC,
    # NOTA: "GUERRERO" ya NO es palabra clave de clase. Ahora queda libre para
    # usarse como el cabezal del TABLERO (se define como valor global en runtime).
}


class Token:
    """Representa una unidad léxica del código fuente."""

    __slots__ = ("type", "lexeme", "value", "line", "column")

    def __init__(self, type_: TokenType, lexeme: str, value=None,
                 line: int = 0, column: int = 0):
        self.type = type_
        self.lexeme = lexeme
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self) -> str:  # pragma: no cover - utilidad de depuración
        return (f"Token({self.type.name}, {self.lexeme!r}, "
                f"value={self.value!r}, line={self.line}, col={self.column})")

    def __eq__(self, other) -> bool:
        if not isinstance(other, Token):
            return NotImplemented
        return (self.type == other.type
                and self.lexeme == other.lexeme
                and self.value == other.value)
