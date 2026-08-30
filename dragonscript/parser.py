"""
parser.py
=========
Parser descendente recursivo de DragonScript.

Consume la lista de tokens producida por el :class:`~dragonscript.lexer.Lexer`
y construye el AST (:mod:`dragonscript.ast_nodes`). Implementa la precedencia
de operadores tradicional:

    or  <  and  <  igualdad  <  comparación  <  suma  <  producto  <  unario
"""

from __future__ import annotations

from . import ast_nodes as ast
from .errors import ParserError
from .tokens import Token, TokenType


class Parser:

  def __init__(self, tokens: list[Token]):
    self.tokens = tokens
    self.pos = 0

  # ------------------------------------------------------------ utilidades
  def _peek(self, offset: int = 0) -> Token:
    idx = self.pos + offset
    if idx < len(self.tokens):
      return self.tokens[idx]
    return self.tokens[-1]  # EOF

  def _current(self) -> Token:
    return self._peek()

  def _advance(self) -> Token:
    tok = self.tokens[self.pos]
    if self.pos < len(self.tokens) - 1:
      self.pos += 1
    return tok

  def _check(self, type_: TokenType) -> bool:
    return self._current().type == type_

  def _match(self, *types: TokenType) -> bool:
    if self._current().type in types:
      self._advance()
      return True
    return False

  def _expect(self, type_: TokenType, message: str) -> Token:
    if self._check(type_):
      return self._advance()
    tok = self._current()
    raise ParserError(f"{message} (se encontró '{tok.lexeme}')", tok.line)

  def _skip_newlines(self) -> None:
    while self._check(TokenType.NEWLINE):
      self._advance()

  # ------------------------------------------------------------------ main
  def parse(self) -> ast.Program:
    program = ast.Program(line=1)
    self._skip_newlines()
    while not self._check(TokenType.EOF):
      program.statements.append(self._statement())
      self._skip_newlines()
    return program

  # ------------------------------------------------------------ sentencias
  def _statement(self) -> ast.Node:
    tok = self._current()

    if tok.type == TokenType.KI:
      return self._ki_declaration()
    if tok.type == TokenType.ROSHI:
      return self._roshi_declaration()
    if tok.type == TokenType.SCOUTER:
      return self._scouter()
    if tok.type == TokenType.IF:
      return self._if_statement()
    if tok.type == TokenType.WHILE:
      return self._while_statement()
    if tok.type == TokenType.FOREACH:
      return self._foreach_statement()
    if tok.type == TokenType.GRAVITY:
      return self._gravity_statement()
    if tok.type == TokenType.TECHNIQUE:
      return self._technique_declaration()
    if tok.type == TokenType.WARRIOR:
      return self._warrior_declaration()
    if tok.type == TokenType.RETURN:
      return self._return_statement()

    # Asignación o expresión suelta.
    return self._assignment_or_expression()

  def _block(self) -> ast.Block:
    statements: list[ast.Statement] = []

    # Ignorar saltos de línea opcionales antes de la llave de apertura
    while self._match(TokenType.NEWLINE):
      pass

    self._expect(
        TokenType.LBRACE, "Se esperaba '{' para iniciar el cuerpo del bloque"
    )

    # Ignorar saltos de línea tras abrir la llave
    while self._match(TokenType.NEWLINE):
      pass

    while not self._check(TokenType.RBRACE) and not self._check(TokenType.EOF):
      statements.append(self._statement())
      while self._match(TokenType.NEWLINE):
        pass

    self._expect(
        TokenType.RBRACE, "Se esperaba '}' para cerrar el cuerpo del bloque"
    )

    # Ignorar saltos de línea opcionales tras cerrar la llave
    while self._match(TokenType.NEWLINE):
      pass

    return ast.Block(statements=statements)

  def _ki_declaration(self) -> ast.KIDeclaration:
    line = self._advance().line  # consume KI
    name = self._expect(
        TokenType.IDENTIFIER, "Se esperaba un nombre de variable tras 'KI'"
    ).lexeme
    value = None
    if self._match(TokenType.ASSIGN):
      value = self._expression()
    self._end_statement()
    return ast.KIDeclaration(name=name, value=value, line=line)

  def _scouter(self) -> ast.Scouter:
    line = self._advance().line  # consume SCOUTER
    expr = self._expression()
    self._end_statement()
    return ast.Scouter(expression=expr, line=line)

  def _if_statement(self) -> ast.IfStatement:
    line = self._advance().line  # consume IF
    condition = self._expression()
    then_branch = self._block()
    node = ast.IfStatement(
        condition=condition, then_branch=then_branch, line=line
    )

    # Cadena de ELSE / ELSE IF
    while self._check(TokenType.ELSE):
      self._advance()  # consume ELSE
      if self._check(TokenType.IF):
        self._advance()  # consume IF
        elif_cond = self._expression()
        elif_block = self._block()
        node.elif_branches.append((elif_cond, elif_block))
      else:
        node.else_branch = self._block()
        break
    return node

  def _while_statement(self) -> ast.WhileStatement:
    line = self._advance().line  # consume WHILE
    condition = self._expression()
    body = self._block()
    return ast.WhileStatement(condition=condition, body=body, line=line)

  def _foreach_statement(self) -> ast.ForEachStatement:
    line = self._advance().line  # consume RASTREAR (FOREACH)
    var_name = self._expect(
        TokenType.IDENTIFIER,
        "Se esperaba un nombre de variable tras 'RASTREAR'",
    ).lexeme
    self._expect(
        TokenType.IN_, "Se esperaba 'EN' tras la variable del recorrido"
    )
    iterable = self._expression()
    body = self._block()
    return ast.ForEachStatement(
        var_name=var_name, iterable=iterable, body=body, line=line
    )

  def _gravity_statement(self) -> ast.GravityStatement:
    line = self._advance().line  # consume GRAVITY
    count = self._expression()
    body = self._block()
    return ast.GravityStatement(count=count, body=body, line=line)

  def _technique_declaration(self) -> ast.TechniqueDeclaration:
    line = self._advance().line  # consume TECHNIQUE
    name = self._expect(
        TokenType.IDENTIFIER, "Se esperaba el nombre de la técnica"
    ).lexeme
    self._expect(
        TokenType.LPAREN, "Se esperaba '(' tras el nombre de la técnica"
    )
    params: list[str] = []
    if not self._check(TokenType.RPAREN):
      params.append(
          self._expect(
              TokenType.IDENTIFIER, "Se esperaba un parámetro"
          ).lexeme
      )
      while self._match(TokenType.COMMA):
        params.append(
            self._expect(
                TokenType.IDENTIFIER, "Se esperaba un parámetro"
            ).lexeme
        )
    self._expect(TokenType.RPAREN, "Se esperaba ')' tras los parámetros")
    self._skip_newlines()  
    body = self._block()
    return ast.TechniqueDeclaration(
        name=name, params=params, body=body, line=line
    )

  def _roshi_declaration(self) -> ast.TechniqueDeclaration:
    line = self._advance().line  # consume ROSHI
    name = self._expect(
        TokenType.IDENTIFIER, "Se esperaba el nombre del procedimiento tras 'ROSHI'"
    ).lexeme
    self._expect(
        TokenType.LPAREN, "Se esperaba '(' tras el nombre del procedimiento"
    )
    params: list[str] = []
    if not self._check(TokenType.RPAREN):
      params.append(
          self._expect(
              TokenType.IDENTIFIER, "Se esperaba un parámetro"
          ).lexeme
      )
      while self._match(TokenType.COMMA):
        params.append(
            self._expect(
                TokenType.IDENTIFIER, "Se esperaba un parámetro"
            ).lexeme
        )
    self._expect(TokenType.RPAREN, "Se esperaba ')' tras los parámetros")
    self._skip_newlines()  
    body = self._block()

    # Validación para evitar TRANSMITIR/RETURN dentro de un ROSHI:
    for stmt in body.statements:
      if isinstance(stmt, ast.ReturnStatement) and stmt.value is not None:
        raise ParserError("¡Un entrenamiento de ROSHI no debe TRANSMITIR ningún valor!", stmt.line)

    return ast.TechniqueDeclaration(
        name=name, params=params, body=body, line=line
    )

  def _warrior_declaration(self) -> ast.WarriorDeclaration:
    line = self._advance().line  # consume WARRIOR
    name = self._expect(
        TokenType.IDENTIFIER, "Se esperaba el nombre de la clase tras 'WARRIOR'"
    ).lexeme
    parents: list[str] = []
    if self._match(TokenType.EVOLVES):
      parents.append(
          self._expect(
              TokenType.IDENTIFIER,
              "Se esperaba el nombre de la clase padre tras 'EVOLVES'",
          ).lexeme
      )
      while self._match(TokenType.COMMA):
        parents.append(
            self._expect(
                TokenType.IDENTIFIER,
                "Se esperaba un nombre de clase padre tras ','",
            ).lexeme
        )

    self._expect(
        TokenType.LBRACE, "Se esperaba '{' para abrir el cuerpo de la clase"
    )
    self._skip_newlines()

    methods: list[ast.TechniqueDeclaration] = []
    class_attributes: list[tuple[str, ast.Node]] = []

    while not self._check(TokenType.RBRACE) and not self._check(TokenType.EOF):
      is_static = self._match(TokenType.STATIC)

      if self._check(TokenType.TECHNIQUE):
        method = self._technique_declaration()
        method.is_static = is_static
        methods.append(method)
      elif self._check(TokenType.IDENTIFIER):
        # Atributo de clase (compartido): ``nombre = valor``.
        attr_name = self._advance().lexeme
        self._expect(
            TokenType.ASSIGN,
            "Se esperaba '=' en la declaración del atributo de clase",
        )
        value = self._expression()
        self._end_statement()
        class_attributes.append((attr_name, value))
      else:
        tok = self._current()
        raise ParserError(
            f"Elemento no válido dentro de la clase '{name}' "
            f"(se encontró '{tok.lexeme}')",
            tok.line,
        )
      self._skip_newlines()

    self._expect(
        TokenType.RBRACE, "Se esperaba '}' para cerrar el cuerpo de la clase"
    )
    return ast.WarriorDeclaration(
        name=name,
        parents=parents,
        methods=methods,
        class_attributes=class_attributes,
        line=line,
    )

  def _return_statement(self) -> ast.ReturnStatement:
    line = self._advance().line  # consume RETURN
    value = None
    if (
        not self._check(TokenType.NEWLINE)
        and not self._check(TokenType.RBRACE)
        and not self._check(TokenType.EOF)
    ):
      value = self._expression()
    self._end_statement()
    return ast.ReturnStatement(value=value, line=line)

  def _assignment_or_expression(self) -> ast.Node:
    line = self._current().line
    expr = self._expression()

    # Asignación simple
    if self._check(TokenType.ASSIGN):
      self._advance()
      value = self._expression()
      self._end_statement()
      self._validate_assign_target(expr)
      return ast.Assignment(target=expr, value=value, line=line)

    # Asignación compuesta
    compound = {
        TokenType.PLUS_ASSIGN: "+=",
        TokenType.MINUS_ASSIGN: "-=",
        TokenType.STAR_ASSIGN: "*=",
        TokenType.SLASH_ASSIGN: "/=",
    }
    if self._current().type in compound:
      op = compound[self._current().type]
      self._advance()
      value = self._expression()
      self._end_statement()
      self._validate_assign_target(expr)
      return ast.CompoundAssignment(
          target=expr, operator=op, value=value, line=line
      )

    # Expresión suelta (por ejemplo, una llamada a técnica).
    self._end_statement()
    return ast.ExpressionStatement(expression=expr, line=line)

  def _validate_assign_target(self, target: ast.Node) -> None:
    if not isinstance(
        target, (ast.Identifier, ast.MemberAccess, ast.IndexAccess)
    ):
      raise ParserError(
          "Objetivo de asignación inválido", getattr(target, "line", 0)
      )

  def _end_statement(self) -> None:
    """Consume el separador de sentencia (NEWLINE o EOF o '}')."""
    if self._check(TokenType.NEWLINE):
      self._advance()
    elif self._check(TokenType.EOF) or self._check(TokenType.RBRACE):
      return
    else:
      tok = self._current()
      raise ParserError(
          f"Se esperaba un salto de línea al final de la sentencia "
          f"(se encontró '{tok.lexeme}')",
          tok.line,
      )

  # ------------------------------------------------------------ expresiones
  def _expression(self) -> ast.Node:
    return self._logic_or()

  def _logic_or(self) -> ast.Node:
    left = self._logic_and()
    while self._check(TokenType.OR):
      line = self._advance().line
      right = self._logic_and()
      left = ast.BinaryOp(left=left, operator="OR", right=right, line=line)
    return left

  def _logic_and(self) -> ast.Node:
    left = self._equality()
    while self._check(TokenType.AND):
      line = self._advance().line
      right = self._equality()
      left = ast.BinaryOp(left=left, operator="AND", right=right, line=line)
    return left

  def _equality(self) -> ast.Node:
    left = self._comparison()
    while self._current().type in (TokenType.EQ, TokenType.NEQ):
      op = "==" if self._current().type == TokenType.EQ else "!="
      line = self._advance().line
      right = self._comparison()
      left = ast.BinaryOp(left=left, operator=op, right=right, line=line)
    return left

  def _comparison(self) -> ast.Node:
    left = self._term()
    ops = {
        TokenType.LT: "<",
        TokenType.GT: ">",
        TokenType.LTE: "<=",
        TokenType.GTE: ">=",
    }
    while self._current().type in ops:
      op = ops[self._current().type]
      line = self._advance().line
      right = self._term()
      left = ast.BinaryOp(left=left, operator=op, right=right, line=line)
    return left

  def _term(self) -> ast.Node:
    left = self._factor()
    ops = {TokenType.PLUS: "+", TokenType.MINUS: "-"}
    while self._current().type in ops:
      op = ops[self._current().type]
      line = self._advance().line
      right = self._factor()
      left = ast.BinaryOp(left=left, operator=op, right=right, line=line)
    return left

  def _factor(self) -> ast.Node:
    left = self._unary()
    ops = {TokenType.STAR: "*", TokenType.SLASH: "/", TokenType.PERCENT: "%"}
    while self._current().type in ops:
      op = ops[self._current().type]
      line = self._advance().line
      right = self._unary()
      left = ast.BinaryOp(left=left, operator=op, right=right, line=line)
    return left

  def _unary(self) -> ast.Node:
    if self._current().type in (TokenType.MINUS, TokenType.NOT):
      op = "-" if self._current().type == TokenType.MINUS else "NOT"
      line = self._advance().line
      operand = self._unary()
      return ast.UnaryOp(operator=op, operand=operand, line=line)
    return self._postfix()

  def _postfix(self) -> ast.Node:
    expr = self._primary()
    while True:
      if self._check(TokenType.LPAREN):
        expr = self._finish_call(expr)
      elif self._check(TokenType.DOT):
        line = self._advance().line
        # Tras el punto se admite un identificador o un lexema de
        # palabra clave (p. ej. GOKU.KI), tratándolo como nombre.
        tok = self._current()
        if tok.type == TokenType.IDENTIFIER or tok.lexeme.isidentifier():
          self._advance()
          member = tok.lexeme
        else:
          raise ParserError(
              f"Se esperaba un nombre de propiedad tras '.' "
              f"(se encontró '{tok.lexeme}')",
              tok.line,
          )
        expr = ast.MemberAccess(obj=expr, member=member, line=line)
      elif self._check(TokenType.LBRACKET):
        line = self._advance().line
        index = self._expression()
        self._expect(
            TokenType.RBRACKET, "Se esperaba ']' tras el índice"
        )
        expr = ast.IndexAccess(obj=expr, index=index, line=line)
      else:
        break
    return expr

  def _finish_call(self, callee: ast.Node) -> ast.TechniqueCall:
    line = self._advance().line  # consume '('
    args: list[ast.Node] = []
    if not self._check(TokenType.RPAREN):
      args.append(self._expression())
      while self._match(TokenType.COMMA):
        args.append(self._expression())
    self._expect(TokenType.RPAREN, "Se esperaba ')' tras los argumentos")
    return ast.TechniqueCall(callee=callee, arguments=args, line=line)

  def _primary(self) -> ast.Node:
    tok = self._current()

    if tok.type == TokenType.NUMBER:
      self._advance()
      return ast.NumberLiteral(value=tok.value, line=tok.line)
    if tok.type == TokenType.STRING:
      self._advance()
      return ast.StringLiteral(value=tok.value, line=tok.line)
    if tok.type == TokenType.TRUE:
      self._advance()
      return ast.BooleanLiteral(value=True, line=tok.line)
    if tok.type == TokenType.FALSE:
      self._advance()
      return ast.BooleanLiteral(value=False, line=tok.line)
    if tok.type == TokenType.NULL:
      self._advance()
      return ast.NullLiteral(line=tok.line)
    if tok.type == TokenType.IDENTIFIER:
      self._advance()
      return ast.Identifier(name=tok.lexeme, line=tok.line)
    if tok.type == TokenType.CREATE:
      return self._create_expression()
    if tok.type == TokenType.LPAREN:
      self._advance()
      expr = self._expression()
      self._expect(
          TokenType.RPAREN, "Se esperaba ')' para cerrar la expresión"
      )
      return expr
    if tok.type == TokenType.LBRACKET:
      return self._array_literal()

    raise ParserError(f"Expresión inesperada: '{tok.lexeme}'", tok.line)

  def _create_expression(self) -> ast.CreateExpression:
    line = self._advance().line  # consume CREATE
    class_name = self._expect(
        TokenType.IDENTIFIER, "Se esperaba el nombre de la clase tras 'CREATE'"
    ).lexeme
    self._expect(
        TokenType.LPAREN, "Se esperaba '(' tras el nombre de la clase"
    )
    args: list[ast.Node] = []
    if not self._check(TokenType.RPAREN):
      args.append(self._expression())
      while self._match(TokenType.COMMA):
        args.append(self._expression())
    self._expect(
        TokenType.RPAREN, "Se esperaba ')' tras los argumentos de CREATE"
    )
    return ast.CreateExpression(
        class_name=class_name, arguments=args, line=line
    )

  def _array_literal(self) -> ast.Node:
    line = self._advance().line  # consume '['
    elements: list[ast.Node] = []
    self._skip_newlines()
    if not self._check(TokenType.RBRACKET):
      first = self._expression()
      # ¿Es un rango [inicio..fin]?
      if self._check(TokenType.DOTDOT):
        self._advance()  # consume '..'
        end = self._expression()
        self._skip_newlines()
        self._expect(
            TokenType.RBRACKET, "Se esperaba ']' para cerrar el rango"
        )
        return ast.RangeLiteral(start=first, end=end, line=line)
      elements.append(first)
      while self._match(TokenType.COMMA):
        self._skip_newlines()
        if self._check(TokenType.RBRACKET):
          break
        elements.append(self._expression())
    self._skip_newlines()
    self._expect(TokenType.RBRACKET, "Se esperaba ']' para cerrar el array")
    return ast.ArrayLiteral(elements=elements, line=line)


def parse(tokens: list[Token]) -> ast.Program:
  """Función de conveniencia: construye el AST a partir de tokens."""
  return Parser(tokens).parse()