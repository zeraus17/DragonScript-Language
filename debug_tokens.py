from dragonscript.lexer import Lexer

with open('clean_test.ds') as f:
    code = f.read()

lexer = Lexer(code)
tokens = lexer.tokenize()

for tok in tokens:
    print(f'{tok.type.name:12} {tok.lexeme:20} line={tok.line}')
