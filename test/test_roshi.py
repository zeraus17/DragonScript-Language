import pytest  # type: ignore[import-not-found]
from dragonscript.lexer import Lexer
from dragonscript.parser import Parser
from dragonscript.interpreter import Interpreter, ArgumentError

def run_code(code: str) -> list[str]:
    output = []
    class MockOutput:
        def write(self, text):
            text_str = str(text).strip()
            if text_str:
                output.append(text_str)

    tokens = Lexer(code).tokenize()
    program = Parser(tokens).parse()
    Interpreter(output=MockOutput()).interpret(program)
    return output

def test_roshi_ejecucion_correcta():
    code = """
    ROSHI entrenar(guerrero) {
        SCOUTER "Entrenando a " + guerrero
    }
    entrenar("Goku")
    """
    output = run_code(code)
    assert output == ["Entrenando a Goku"]

def test_roshi_error_argumentos():
    code = """
    ROSHI entrenar(a, b) {
        SCOUTER a
    }
    entrenar(1)
    """
    with pytest.raises(ArgumentError):
        run_code(code)