"""
interpreter.py
==============
Intérprete tree-walking de DragonScript.

Recorre el AST producido por el Parser y lo evalúa usando entornos anidados
(:mod:`dragonscript.environment`). Soporta expresiones aritméticas y lógicas,
control de flujo (IF/ELSE, WHILE, GRAVITY), definición y llamada de técnicas
(funciones) con recursividad y closures básicos, y salida mediante SCOUTER.
"""

from __future__ import annotations

import sys
from typing import Any

from . import ast_nodes as ast
from .environment import Environment
from .runtime import (Technique, BuiltinFunction, ReturnSignal, ds_repr,
                      is_truthy, register_builtins, VERSION)
from .objects import (DSClass, DSInstance, BoundMethod, UnboundMethod,
                      OPERATOR_DUNDERS)
from .errors import (DragonScriptError, RuntimeError_, DivisionByZeroError,
                     TypeErrorDS, StackOverflowError_, ArgumentError,
                     UndefinedVariableError)

# Centinela para indicar "sin sobrecarga de operador aplicable".
_NO_OVERLOAD = object()

# Límite de profundidad de recursión de técnicas de DragonScript.
MAX_CALL_DEPTH = 400

# Cada llamada a técnica consume varias tramas (frames) de Python; elevamos el
# límite de recursión de Python para que se dispare antes nuestro error
# temático de "Stack overflow" que el RecursionError genérico de Python.
sys.setrecursionlimit(max(sys.getrecursionlimit(), MAX_CALL_DEPTH * 20))


class Interpreter:
    def __init__(self, output=None):
        self.globals = Environment()
        self.environment = self.globals
        self._out = output if output is not None else sys.stdout
        self._call_depth = 0
        register_builtins(self.globals, self._out)

    # ------------------------------------------------------------------ API
    def interpret(self, program: ast.Program) -> None:
        """Ejecuta un programa completo."""
        for stmt in program.statements:
            self._execute(stmt)

    def _emit(self, text: str) -> None:
        self._out.write(text + "\n")

    # ------------------------------------------------------------- ejecución
    def _execute(self, node: ast.Node) -> Any:
        method = getattr(self, "_exec_" + type(node).__name__, None)
        if method is None:
            raise RuntimeError_(f"Nodo no soportado: {type(node).__name__}",
                                getattr(node, "line", None))
        return method(node)

    def _exec_Block(self, node: ast.Block, env: Environment | None = None) -> None:
        previous = self.environment
        self.environment = env if env is not None else Environment(previous)
        try:
            for stmt in node.statements:
                self._execute(stmt)
        finally:
            self.environment = previous

    def _exec_KIDeclaration(self, node: ast.KIDeclaration) -> None:
        value = self._evaluate(node.value) if node.value is not None else None
        self.environment.define(node.name, value)

    def _exec_Assignment(self, node: ast.Assignment) -> None:
        value = self._evaluate(node.value)
        self._assign_to_target(node.target, value, node.line)

    def _exec_CompoundAssignment(self, node: ast.CompoundAssignment) -> None:
        target = node.target
        if not isinstance(target, (ast.Identifier, ast.MemberAccess, ast.IndexAccess)):
            raise RuntimeError_("La asignación compuesta requiere una variable "
                                "o propiedad", node.line)
        current = self._evaluate(target)
        rhs = self._evaluate(node.value)
        op = node.operator[0]  # '+', '-', '*', '/'
        result = self._apply_binary(op, current, rhs, node.line)
        self._assign_to_target(target, result, node.line)

    def _assign_to_target(self, target: ast.Node, value: Any, line: int) -> None:
        """Asigna ``value`` al objetivo (variable, propiedad o índice)."""
        if isinstance(target, ast.Identifier):
            self.environment.assign(target.name, value, line)
        elif isinstance(target, ast.IndexAccess):
            obj = self._evaluate(target.obj)
            index = self._evaluate(target.index)
            self._set_index(obj, index, value, line)
        elif isinstance(target, ast.MemberAccess):
            obj = self._evaluate(target.obj)
            via_self = (isinstance(target.obj, ast.Identifier)
                        and target.obj.name in ("SELF", "YO"))
            self._set_member(obj, target.member, value, line, via_self)
        else:
            raise RuntimeError_("Objetivo de asignación no soportado", line)

    def _set_member(self, obj: Any, member: str, value: Any, line: int,
                    via_self: bool) -> None:
        if isinstance(obj, DSInstance):
            if member.startswith("_") and not via_self:
                raise RuntimeError_(
                    f"'{member}' es privado: solo el propio guerrero puede "
                    f"modificarlo (usa SELF).", line)
            obj.fields[member] = value
            return
        if isinstance(obj, DSClass):
            obj.class_attributes[member] = value
            return
        # Objetos del runtime Dragon Ball (Fase 2) u otros con atributos.
        if hasattr(obj, member):
            try:
                setattr(obj, member, value)
                return
            except (AttributeError, TypeError):
                pass
        if isinstance(obj, dict):
            obj[member] = value
            return
        raise RuntimeError_(
            f"No se puede asignar la propiedad '{member}' en ese valor.", line)

    def _exec_Scouter(self, node: ast.Scouter) -> None:
        value = self._evaluate(node.expression)
        self._emit(self._stringify(value))

    def _stringify(self, value: Any) -> str:
        """Convierte a texto respetando el método mágico ``__str__`` si la
        instancia lo define."""
        if isinstance(value, DSInstance):
            method = value.klass.find_method("__str__")
            if method is not None:
                result = self._call_technique(method, [], 0, self_obj=value)
                return self._stringify(result)
        return ds_repr(value)

    def _exec_IfStatement(self, node: ast.IfStatement) -> None:
        if is_truthy(self._evaluate(node.condition)):
            self._exec_Block(node.then_branch)
            return
        for cond, block in node.elif_branches:
            if is_truthy(self._evaluate(cond)):
                self._exec_Block(block)
                return
        if node.else_branch is not None:
            self._exec_Block(node.else_branch)

    def _exec_WhileStatement(self, node: ast.WhileStatement) -> None:
        while is_truthy(self._evaluate(node.condition)):
            self._exec_Block(node.body)

    def _exec_ForEachStatement(self, node: ast.ForEachStatement) -> None:
        iterable = self._evaluate(node.iterable)
        if not isinstance(iterable, (list, str)):
            raise TypeErrorDS(
                "RASTREAR solo puede recorrer un grupo (lista) o un texto.",
                node.line)
        for element in iterable:
            loop_env = Environment(self.environment)
            loop_env.define(node.var_name, element)
            self._exec_Block(node.body, env=loop_env)

    def _exec_GravityStatement(self, node: ast.GravityStatement) -> None:
        count = self._evaluate(node.count)
        if isinstance(count, bool) or not isinstance(count, (int, float)):
            raise TypeErrorDS("GRAVITY requiere un número de repeticiones.",
                              node.line)
        for _ in range(int(count)):
            self._exec_Block(node.body)

    def _exec_TechniqueDeclaration(self, node: ast.TechniqueDeclaration) -> None:
        technique = Technique(node, self.environment)
        self.environment.define(node.name, technique)

    def _exec_WarriorDeclaration(self, node: ast.WarriorDeclaration) -> None:
        # Resolver las clases padre (deben existir y ser clases).
        parents: list[DSClass] = []
        for parent_name in node.parents:
            parent = self.environment.get(parent_name, node.line)
            if not isinstance(parent, DSClass):
                raise TypeErrorDS(
                    f"'{parent_name}' no es un WARRIOR del que se pueda evolucionar.",
                    node.line)
            parents.append(parent)

        # Métodos de instancia y estáticos.
        methods: dict[str, Technique] = {}
        static_methods: dict[str, Technique] = {}
        for m in node.methods:
            technique = Technique(m, self.environment)
            if m.is_static:
                static_methods[m.name] = technique
            else:
                methods[m.name] = technique

        # Atributos de clase (compartidos), evaluados en el momento de definir.
        class_attributes: dict[str, Any] = {}
        for attr_name, value_node in node.class_attributes:
            class_attributes[attr_name] = self._evaluate(value_node)

        try:
            klass = DSClass(node.name, parents, methods, static_methods,
                            class_attributes)
        except ValueError as exc:
            raise TypeErrorDS(str(exc), node.line)

        self.environment.define(node.name, klass)

    def _exec_ReturnStatement(self, node: ast.ReturnStatement) -> None:
        value = self._evaluate(node.value) if node.value is not None else None
        raise ReturnSignal(value)

    def _exec_ImportStatement(self, node: ast.ImportStatement) -> None:
        """Carga y ejecuta un módulo .ds (por ahora soporta Biblioteca)."""
        import os
        from pathlib import Path
        from .lexer import tokenize
        from .parser import parse as parse_tokens

        module_name = node.module.strip().strip('"').strip("'")
        # Buscar el archivo en varios sitios posibles
        candidates = [
            Path(__file__).parent / f"{module_name}.ds",
            Path(__file__).parent / "modules" / f"{module_name}.ds",
            Path.cwd() / f"{module_name}.ds",
            Path.cwd() / "dragonscript" / f"{module_name}.ds",
        ]
        source = None
        for cand in candidates:
            if cand.is_file():
                source = cand.read_text(encoding="utf-8")
                break
        if source is None:
            # Fallback: si es Biblioteca y estamos en web (Pyodide), se inyecta desde el playground
            raise RuntimeError_(
                f"¡El Scouter no encuentra el módulo '{module_name}'! "
                f"Asegurate de que exista {module_name}.ds",
                node.line,
            )
        tokens = tokenize(source)
        program = parse_tokens(tokens)
        # Ejecutar en el mismo environment (como #include)
        for stmt in program.statements:
            self._execute(stmt)

    def _exec_ExpressionStatement(self, node: ast.ExpressionStatement) -> None:
        self._evaluate(node.expression)

    # ------------------------------------------------------------ evaluación
    def _evaluate(self, node: ast.Node) -> Any:
        method = getattr(self, "_eval_" + type(node).__name__, None)
        if method is None:
            raise RuntimeError_(f"Expresión no soportada: {type(node).__name__}",
                                getattr(node, "line", None))
        return method(node)

    def _eval_NumberLiteral(self, node: ast.NumberLiteral) -> Any:
        return node.value

    def _eval_StringLiteral(self, node: ast.StringLiteral) -> Any:
        return node.value

    def _eval_BooleanLiteral(self, node: ast.BooleanLiteral) -> Any:
        return node.value

    def _eval_NullLiteral(self, node: ast.NullLiteral) -> Any:
        return None

    def _eval_ArrayLiteral(self, node: ast.ArrayLiteral) -> Any:
        return [self._evaluate(e) for e in node.elements]

    def _eval_RangeLiteral(self, node: ast.RangeLiteral) -> Any:
        start = self._evaluate(node.start)
        end = self._evaluate(node.end)
        for v in (start, end):
            if isinstance(v, bool) or not isinstance(v, int):
                raise TypeErrorDS(
                    "Un rango [inicio..fin] requiere números enteros.", node.line)
        # Rango inclusivo ascendente. Si inicio > fin, el grupo queda vacío.
        return list(range(start, end + 1))

    def _eval_Identifier(self, node: ast.Identifier) -> Any:
        return self.environment.get(node.name, node.line)

    def _eval_UnaryOp(self, node: ast.UnaryOp) -> Any:
        operand = self._evaluate(node.operand)
        if node.operator == "-":
            if isinstance(operand, bool) or not isinstance(operand, (int, float)):
                raise TypeErrorDS("No puedes negar algo que no es número.", node.line)
            return -operand
        if node.operator == "NOT":
            return not is_truthy(operand)
        raise RuntimeError_(f"Operador unario desconocido: {node.operator}", node.line)

    def _eval_BinaryOp(self, node: ast.BinaryOp) -> Any:
        # Operadores lógicos con cortocircuito.
        if node.operator == "AND":
            left = self._evaluate(node.left)
            if not is_truthy(left):
                return left
            return self._evaluate(node.right)
        if node.operator == "OR":
            left = self._evaluate(node.left)
            if is_truthy(left):
                return left
            return self._evaluate(node.right)

        left = self._evaluate(node.left)
        right = self._evaluate(node.right)
        return self._apply_binary(node.operator, left, right, node.line)

    def _apply_binary(self, op: str, left: Any, right: Any, line: int) -> Any:
        # Sobrecarga de operadores: si el operando izquierdo es una instancia
        # y su clase define el método mágico correspondiente, lo usamos.
        overloaded = self._try_operator_overload(op, left, right, line)
        if overloaded is not _NO_OVERLOAD:
            return overloaded

        # Igualdad / desigualdad
        if op == "==":
            return left == right
        if op == "!=":
            return left != right

        # Concatenación de grupos (listas) con '+'
        if op == "+" and isinstance(left, list) and isinstance(right, list):
            return left + right

        # Concatenación de cadenas con '+'
        if op == "+":
            if isinstance(left, str) or isinstance(right, str):
                return self._stringify(left) + self._stringify(right) \
                    if not (isinstance(left, str) and isinstance(right, str)) \
                    else left + right
            self._check_numbers(left, right, line)
            return left + right

        # Comparaciones
        if op in ("<", ">", "<=", ">="):
            if isinstance(left, str) and isinstance(right, str):
                pass  # comparación lexicográfica permitida
            else:
                self._check_numbers(left, right, line)
            if op == "<":
                return left < right
            if op == ">":
                return left > right
            if op == "<=":
                return left <= right
            return left >= right

        # Aritmética restante
        self._check_numbers(left, right, line)
        if op == "-":
            return left - right
        if op == "*":
            return left * right
        if op == "/":
            if right == 0:
                raise DivisionByZeroError(line)
            result = left / right
            # Mantener enteros cuando la división es exacta.
            if isinstance(left, int) and isinstance(right, int) and result.is_integer():
                return int(result)
            return result
        if op == "%":
            if right == 0:
                raise DivisionByZeroError(line)
            return left % right

        raise RuntimeError_(f"Operador desconocido: {op}", line)

    def _check_numbers(self, left: Any, right: Any, line: int) -> None:
        for v in (left, right):
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                raise TypeErrorDS(
                    "No puedes operar aritméticamente con ese tipo.", line)

    def _try_operator_overload(self, op: str, left: Any, right: Any, line: int) -> Any:
        """Intenta resolver el operador mediante un método mágico de la clase
        del operando izquierdo. Devuelve ``_NO_OVERLOAD`` si no aplica."""
        if not isinstance(left, DSInstance):
            return _NO_OVERLOAD
        dunder = OPERATOR_DUNDERS.get(op)
        if dunder is None:
            return _NO_OVERLOAD
        method = left.klass.find_method(dunder)
        if method is None:
            # Caso especial: si define __eq__ pero no __neq__, derivamos !=.
            if op == "!=":
                eq = left.klass.find_method("__eq__")
                if eq is not None:
                    result = self._call_technique(eq, [right], line, self_obj=left)
                    return not is_truthy(result)
            return _NO_OVERLOAD
        return self._call_technique(method, [right], line, self_obj=left)

    # --------------------------------------------------------- acceso/llamada
    def _eval_MemberAccess(self, node: ast.MemberAccess) -> Any:
        obj = self._evaluate(node.obj)
        member = node.member
        via_self = (isinstance(node.obj, ast.Identifier)
                    and node.obj.name in ("SELF", "YO"))

        # --- Instancias de clases DragonScript ---
        if isinstance(obj, DSInstance):
            if member.startswith("_") and not via_self:
                raise RuntimeError_(
                    f"'{member}' es privado: solo el propio guerrero puede "
                    f"acceder a él (usa SELF).", node.line)
            # 1) Campo de instancia
            if member in obj.fields:
                return obj.fields[member]
            # 2) Método de instancia -> método ligado (lleva SELF)
            method = obj.klass.find_method(member)
            if method is not None:
                return BoundMethod(obj, method)
            # 3) Método estático accesible desde la instancia
            static = obj.klass.find_static(member)
            if static is not None:
                return static
            # 4) Atributo de clase (compartido)
            found, value = obj.klass.find_class_attr(member)
            if found:
                return value
            raise RuntimeError_(
                f"El guerrero '{obj.klass.name}' no tiene la propiedad "
                f"'{member}'.", node.line)

        # --- Clases (acceso a miembros estáticos / atributos / métodos) ---
        if isinstance(obj, DSClass):
            static = obj.find_static(member)
            if static is not None:
                return static
            found, value = obj.find_class_attr(member)
            if found:
                return value
            # Método de instancia accedido vía la clase -> método NO ligado.
            # Permite llamar al método de un padre pasando SELF explícito,
            # p. ej. ``Padre.__init__(SELF, ...)``.
            method = obj.find_method(member)
            if method is not None:
                return UnboundMethod(obj, method)
            raise RuntimeError_(
                f"La clase '{obj.name}' no tiene el miembro "
                f"'{member}'.", node.line)

        # --- Objetos del runtime Dragon Ball (Fase 2) / dicts ---
        if isinstance(obj, dict) and member in obj:
            return obj[member]
        if hasattr(obj, member):
            return getattr(obj, member)
        raise RuntimeError_(
            f"El objeto no tiene la propiedad '{member}'.", node.line)

    def _eval_CreateExpression(self, node: ast.CreateExpression) -> Any:
        klass = self.environment.get(node.class_name, node.line)
        if not isinstance(klass, DSClass):
            raise TypeErrorDS(
                f"'{node.class_name}' no es un WARRIOR que se pueda crear con "
                f"CREATE.", node.line)
        instance = DSInstance(klass)
        args = [self._evaluate(a) for a in node.arguments]

        init = klass.find_method("__init__")
        if init is not None:
            self._call_technique(init, args, node.line, self_obj=instance)
        elif args:
            raise ArgumentError(
                f"El guerrero '{klass.name}' no define un constructor "
                f"(__init__), pero recibió {len(args)} argumento(s).", node.line)
        return instance

    def _eval_IndexAccess(self, node: ast.IndexAccess) -> Any:
        obj = self._evaluate(node.obj)
        index = self._evaluate(node.index)
        if isinstance(obj, (list, str)):
            if not isinstance(index, int) or isinstance(index, bool):
                raise TypeErrorDS("El índice debe ser un número entero.", node.line)
            try:
                return obj[index]
            except IndexError:
                raise RuntimeError_("Índice fuera de rango.", node.line)
        raise TypeErrorDS("Ese valor no se puede indexar.", node.line)

    def _set_index(self, obj: Any, index: Any, value: Any, line: int) -> None:
        if isinstance(obj, list) and isinstance(index, int) and not isinstance(index, bool):
            try:
                obj[index] = value
                return
            except IndexError:
                raise RuntimeError_("Índice fuera de rango.", line)
        raise TypeErrorDS("No se puede asignar a ese índice.", line)

    def _eval_TechniqueCall(self, node: ast.TechniqueCall) -> Any:
        callee = self._evaluate(node.callee)
        args = [self._evaluate(a) for a in node.arguments]

        if isinstance(callee, BuiltinFunction):
            return callee.call(args)

        if isinstance(callee, BoundMethod):
            return self._call_technique(callee.technique, args, node.line,
                                        self_obj=callee.instance)

        if isinstance(callee, UnboundMethod):
            # El primer argumento es la instancia (SELF explícito).
            if not args:
                raise ArgumentError(
                    f"El método '{callee.name}' llamado desde la clase "
                    f"'{callee.klass.name}' necesita recibir SELF como primer "
                    f"argumento.", node.line)
            return self._call_technique(callee.technique, args[1:], node.line,
                                        self_obj=args[0])

        if isinstance(callee, Technique):
            return self._call_technique(callee, args, node.line)

        raise TypeErrorDS("Eso no es una técnica que puedas invocar.", node.line)

    def _call_technique(self, technique: Technique, args: list[Any], line: int,
                        self_obj: Any = None) -> Any:
        if len(args) != technique.arity:
            # Mensaje adaptado: si es un método, hablamos de un método.
            etiqueta = "El método" if self_obj is not None else "La técnica"
            raise ArgumentError(
                f"{etiqueta} '{technique.name}' esperaba {technique.arity} "
                f"argumento(s), recibió {len(args)}.", line)

        self._call_depth += 1
        if self._call_depth > MAX_CALL_DEPTH:
            self._call_depth -= 1
            raise StackOverflowError_(line)

        env = Environment(technique.closure)
        # Los métodos de instancia reciben SELF de forma implícita.
        if self_obj is not None:
            env.define("SELF", self_obj)
            env.define("YO", self_obj)  # alias en español de SELF
        for name, value in zip(technique.declaration.params, args):
            env.define(name, value)

        previous = self.environment
        self.environment = env
        try:
            for stmt in technique.declaration.body.statements:
                self._execute(stmt)
            return None
        except ReturnSignal as ret:
            return ret.value
        finally:
            self.environment = previous
            self._call_depth -= 1


def run(program: ast.Program, output=None) -> None:
    """Función de conveniencia: interpreta un programa."""
    Interpreter(output=output).interpret(program)
