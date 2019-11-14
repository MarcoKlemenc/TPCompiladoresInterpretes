from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Print
        self.lexer.add('PRINT', r'IMPRIMIR')
        # Operators
        self.lexer.add('MUL', r'POR')
        self.lexer.add('DIV', r'DIVIDIDO')
        self.lexer.add('SUM', r'MAS')
        self.lexer.add('SUB', r'MENOS')
        # Number
        self.lexer.add('NUMBER', r'\d+')
        self.lexer.add('DECIMAL_POINT', r'\.')
        # String
        self.lexer.add('STRING', r'\'\'.*\'\'')
        # Variables
        self.lexer.add('VAR_NAME', r'[a-z_]+')
        self.lexer.add('VAR_ASSIGN', r'ES')
        # Ignore spaces
        self.lexer.ignore('\s+')
        # Ignore comments
        self.lexer.ignore('@.*')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build(), [r.name for r in self.lexer.rules]
