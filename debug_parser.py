from dragonscript.lexer import Lexer
from dragonscript.parser import Parser

with open('clean_test.ds') as f:
    code = f.read()

print("=== TOKENS ===")
lexer = Lexer(code)
tokens = lexer.tokenize()

for i, tok in enumerate(tokens):
    print(f"{i}: {tok.type.name:12} {tok.lexeme:20} line={tok.line}")

print("\n=== PARSING ===")
try:
    parser = Parser(tokens)
    ast = parser.parse()
    print("Success!")
except Exception as e:
    print(f"Error: {e}")
    print(f"\nCurrent token index: {parser.current}")
    print(f"Current token: {parser.tokens[parser.current]}")
