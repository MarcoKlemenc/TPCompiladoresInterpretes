from rply import ParserGenerator
from .ast import Number, String, Boolean, OpBuilder, Print


class Parser():
    def __init__(self, module, builder, printf, tokens):
        self.pg = ParserGenerator(tokens, precedence=[('left', ['SUM', 'SUB']), ('left', ['MUL', 'DIV'])])
        self.module = module
        self.builder = builder
        self.printf = printf
        self.variables = {}

    def parse(self):
        @self.pg.production('prog : ')
        @self.pg.production('prog : prog expr')
        def program(p):
            if len(p) == 2:
                res = p[0] if p[0] else []
                if p[1] not in res:
                    res.append(p[1])
                return res
            return p

        @self.pg.production('expr : PRINT expr')
        def printing(p):
            return Print(self.builder, self.module, self.printf, p[1], p[1].format())

        @self.pg.production('expr : expr SUM expr')
        @self.pg.production('expr : expr SUB expr')
        @self.pg.production('expr : expr MUL expr')
        @self.pg.production('expr : expr DIV expr')
        def arithmetic_operation(p):
            left = p[0]
            right = p[2]
            operator = p[1].gettokentype()
            op_builder = OpBuilder(self.builder, self.module)
            return op_builder.build_op(left, right, operator)

        @self.pg.production('expr : expr EQUAL expr')
        @self.pg.production('expr : expr DIFFERENT expr')
        @self.pg.production('expr : expr GREATER expr')
        @self.pg.production('expr : expr LESS expr')
        def conditional(p):
            operator = p[1].gettokentype()
            if operator == 'EQUAL':
                return Boolean(self.builder, self.module, p[0].eq(p[2]))
            if operator == 'DIFFERENT':
                return Boolean(self.builder, self.module, p[0].ne(p[2]))
            if operator == 'GREATER':
                return Boolean(self.builder, self.module, p[0].gt(p[2]))
            if operator == 'LESS':
                return Boolean(self.builder, self.module, p[0].lt(p[2]))

        @self.pg.production('expr : TRUE')
        @self.pg.production('expr : FALSE')
        def boolean_variables(p):
            operator = p[0].gettokentype()
            if operator == 'TRUE':
                return Boolean(self.builder, self.module, True)
            if operator == 'FALSE':
                return Boolean(self.builder, self.module, False)

        @self.pg.production('expr : expr AND expr')
        @self.pg.production('expr : expr OR expr')
        def boolean_operations(p):
            operator = p[1].gettokentype()
            if operator == 'AND':
                return Boolean(self.builder, self.module, p[0].value and p[2].value)
            if operator == 'OR':
                return Boolean(self.builder, self.module, p[0].value or p[2].value)

        @self.pg.production('expr : expr IF expr ELSE expr')
        def if_struct(p):
            return p[0] if p[2].value else p[4]

        @self.pg.production('expr : NUMBER')
        def number(p):
            return Number(self.builder, self.module, p[0].value)

        @self.pg.production('expr : NUMBER DECIMAL_POINT NUMBER')
        def float(p):
            return Number(self.builder, self.module, p[0].value+p[1].value+p[2].value)

        @self.pg.production('expr : STRING')
        def string(p):
            return String(self.builder, self.module, p[0].value[1:-1])

        @self.pg.production('expr : VAR_NAME VAR_ASSIGN expr')
        def var_assign(p):
            self.variables[p[0].value] = p[2]
            return p[2]

        @self.pg.production('expr : VAR_NAME')
        def var_read(p):
            return self.variables.get(p[0].value) or False

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
