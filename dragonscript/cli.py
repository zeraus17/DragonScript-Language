import sys
from pathlib import Path

from dragonscript.errors import DragonScriptError
from dragonscript.interpreter import Interpreter
from dragonscript.lexer import Lexer
from dragonscript.parser import Parser


def main():
    if len(sys.argv) < 2:
        print("Uso: dragonscript <archivo.ds>")
        sys.exit(1)

    filepath = Path(sys.argv[1]).resolve()
    with open(filepath, "r", encoding="utf-8") as f:
        user_code = f.read()

    # Cargar la biblioteca global (Biblioteca.ds) si existe
    stdlib_path = Path(__file__).parent / "Biblioteca.ds"
    stdlib_code = ""
    stdlib_lines = 0

    if stdlib_path.exists():
        with open(stdlib_path, "r", encoding="utf-8") as f:
            stdlib_code = f.read().strip()
            if stdlib_code:
                # Contamos cuántas líneas ocupa la librería para ajustar el reporte de errores
                stdlib_lines = stdlib_code.count("\n") + 2
                stdlib_code = f"{stdlib_code}\n\n"

    code_completo = stdlib_code + user_code

    try:
        tokens = Lexer(code_completo).tokenize()
        ast = Parser(tokens).parse()

        interpreter = Interpreter()
        interpreter.interpret(ast)

    except DragonScriptError as e:
        # Si el error ocurrió en el código del usuario, ajustamos el número de línea reportado
        if hasattr(e, "line") and e.line and e.line > stdlib_lines:
            e.line -= stdlib_lines
        raise e

    # Mantener la ventana de la GUI abierta si fue inicializada
    from dragonscript.runtime import gui_instance

    if gui_instance[0] is not None:
        gui_instance[0].mantener_abierto()


if __name__ == "__main__":
    main()