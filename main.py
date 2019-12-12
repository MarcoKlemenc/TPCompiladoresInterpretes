from compilador.codegen import CodeGen
from compilador.lexer import Lexer
from compilador.parser import Parser
import sys

fname = sys.argv[1]
with open(fname) as f:
    text_input = f.read()

lexer, token_names = Lexer().get_lexer()
tokens = lexer.lex(text_input)

codegen = CodeGen()

module = codegen.module
builder = codegen.builder
printf = codegen.printf

pg = Parser(module, builder, printf, token_names)
pg.parse()
for token in pg.get_parser().parse(tokens):
    token.eval()

codegen.create_ir()
codegen.save_ir("output.ll")
