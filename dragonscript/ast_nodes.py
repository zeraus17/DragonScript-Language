"""
ast_nodes.py
============
Nodos del Árbol de Sintaxis Abstracta (AST) de DragonScript.

Cada nodo es una simple clase de datos (usamos ``dataclass``) que representa
una construcción del lenguaje. El Parser produce estos nodos y el Interpreter
los recorre (tree-walking).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


class Node:
    """Clase base de todos los nodos del AST."""
    line: int = 0


# --------------------------------------------------------------- estructura
@dataclass
class Program(Node):
    statements: list[Node] = field(default_factory=list)
    line: int = 0


@dataclass
class Block(Node):
    statements: list[Node] = field(default_factory=list)
    line: int = 0


# --------------------------------------------------------------- literales
@dataclass
class NumberLiteral(Node):
    value: float | int
    line: int = 0


@dataclass
class StringLiteral(Node):
    value: str
    line: int = 0


@dataclass
class BooleanLiteral(Node):
    value: bool
    line: int = 0


@dataclass
class NullLiteral(Node):
    line: int = 0


@dataclass
class ArrayLiteral(Node):
    elements: list[Node] = field(default_factory=list)
    line: int = 0


@dataclass
class RangeLiteral(Node):
    """Rango de enteros inclusivo: ``[inicio..fin]`` -> lista [inicio, ..., fin]."""
    start: Node
    end: Node
    line: int = 0


@dataclass
class Identifier(Node):
    name: str
    line: int = 0


# ------------------------------------------------------------- expresiones
@dataclass
class BinaryOp(Node):
    left: Node
    operator: str
    right: Node
    line: int = 0


@dataclass
class UnaryOp(Node):
    operator: str
    operand: Node
    line: int = 0


@dataclass
class MemberAccess(Node):
    obj: Node
    member: str
    line: int = 0


@dataclass
class IndexAccess(Node):
    obj: Node
    index: Node
    line: int = 0


@dataclass
class TechniqueCall(Node):
    callee: Node
    arguments: list[Node] = field(default_factory=list)
    line: int = 0


# ------------------------------------------------------------- sentencias
@dataclass
class KIDeclaration(Node):
    """Declaración de variable: ``KI nombre = valor``."""
    name: str
    value: Optional[Node] = None
    line: int = 0


@dataclass
class Assignment(Node):
    """Asignación a una variable existente: ``nombre = valor``."""
    target: Node
    value: Node
    line: int = 0


@dataclass
class CompoundAssignment(Node):
    """Asignación compuesta: ``nombre += valor`` (y -=, *=, /=)."""
    target: Node
    operator: str  # '+=', '-=', '*=', '/='
    value: Node
    line: int = 0


@dataclass
class Scouter(Node):
    """Instrucción de salida: ``SCOUTER expr``."""
    expression: Node
    line: int = 0


@dataclass
class IfStatement(Node):
    condition: Node
    then_branch: Block
    # Lista de (condición, bloque) para cada ``ELSE IF``.
    elif_branches: list[tuple[Node, Block]] = field(default_factory=list)
    else_branch: Optional[Block] = None
    line: int = 0


@dataclass
class WhileStatement(Node):
    condition: Node
    body: Block
    line: int = 0


@dataclass
class ForEachStatement(Node):
    """Recorrido enumerativo: ``RASTREAR x EN grupo { ... }``.

    Recorre cada elemento de ``iterable`` (una lista o cadena), ligando cada
    valor a la variable ``var_name`` dentro del cuerpo.
    """
    var_name: str
    iterable: Node
    body: Block
    line: int = 0


@dataclass
class GravityStatement(Node):
    """Bucle temático: ``GRAVITY N { ... }`` ejecuta el bloque N veces."""
    count: Node
    body: Block
    line: int = 0


@dataclass
class TechniqueDeclaration(Node):
    """Definición de función: ``TECHNIQUE nombre(params) { ... }``.

    Cuando aparece dentro de una clase (``WARRIOR``) y va precedida de
    ``STATIC``, ``is_static`` es ``True`` y el método no recibe ``SELF``.
    """
    name: str
    params: list[str] = field(default_factory=list)
    body: Block = field(default_factory=Block)
    is_static: bool = False
    line: int = 0


@dataclass
class WarriorDeclaration(Node):
    """Definición de clase: ``WARRIOR Nombre [EVOLVES Padre1, Padre2] { ... }``.

    * ``methods``            — métodos de instancia y estáticos (TechniqueDeclaration).
    * ``class_attributes``   — atributos de clase compartidos ``(nombre, valor_node)``.
    """
    name: str
    parents: list[str] = field(default_factory=list)
    methods: list["TechniqueDeclaration"] = field(default_factory=list)
    class_attributes: list[tuple[str, "Node"]] = field(default_factory=list)
    line: int = 0


@dataclass
class CreateExpression(Node):
    """Instanciación de una clase: ``CREATE Nombre(args)``."""
    class_name: str
    arguments: list[Node] = field(default_factory=list)
    line: int = 0


@dataclass
class ReturnStatement(Node):
    value: Optional[Node] = None
    line: int = 0


@dataclass
class ExpressionStatement(Node):
    """Una expresión usada como sentencia (por ejemplo, una llamada)."""
    expression: Node
    line: int = 0
