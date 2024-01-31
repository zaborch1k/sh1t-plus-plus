# файл с лексером и парсером
import lex
import parcer as yacc
from lex import LexToken

# лексер
keywords = (
    "SET",
    'RIGHT',
    'LEFT',
    'UP',
    'DOWN',
    'IFBLOCK',
    'ENDIF',
    'REPEAT',
    'ENDREPEAT',
    'PROCEDURE',
    'ENDPROC',
    'CALL',
)

tokens = keywords + (
    "DIVIDE",
    "EQUALS",
    "ID",
    "LPAREN",
    "MINUS",
    'NUMBER',
    "PLUS",
    "RPAREN",
    "TIMES",
    'NEWLINE',
    'INDENT',
    'DEDENT',
    'WS'
)

def t_ID(t):
    r"[a-zA-Z][a-zA-Z]*"
    if t.value in keywords:
        t.type = t.value
    return t

t_PLUS    = r"\+"
t_MINUS   = r"-"
t_TIMES   = r"\*"
t_DIVIDE  = r"/"
t_EQUALS  = r"="
t_LPAREN  = r"\("
t_RPAREN  = r"\)"
t_WS = r'[^\n\S]+'
t_NEWLINE = r'\n'

def t_NUMBER(t):
    r"-?\d+"
    t.value = int(t.value)
    return t

def t_error(t):
    pass


# второй лексер, для обработки отступов
class IndentLex:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tok = None
        self.data = None
        self.lineno = 0

    def input(self, data):
        self.lexer.input(data)

    def token(self):
        if self.tok is None:
            self.tok = self._token()

        try:
            return next(self.tok)
        except StopIteration:
            return None

    def empty_tok(self):
        tok = LexToken()
        (tok.type,
         tok.value,
         tok.lineno,
         tok.lexpos) = ('', '', 0, 0)

        return tok

    def logical_lines(self):
        for t in self.lexer:
            tokens = []
            indent = 0

            while t.type != 'NEWLINE':
                if t.type != 'WS':
                    tokens.append(t)
                elif not tokens:
                    indent = len(t.value)
                t = self.lexer.token()
            tokens.append(t)

            if tokens[0].type == 'NEWLINE' and len(tokens) == 1:
                continue

            if tokens:
                yield tokens, indent
        yield 'EOF', 0

    def __iter__(self):
        return self._token()

    def _token(self):
        indent_stack = [0]

        for tokens, indent in self.logical_lines():
            indent = indent
            indent_tok = self.empty_tok()
            
            if tokens == 'EOF':
                while len(indent_stack) > 1:
                    indent_tok.type = 'DEDENT'
                    indent_stack.pop()
                    yield indent_tok
                break

            last_indent = indent_stack[-1]

            if last_indent < indent:
                indent_stack.append(indent)
                indent_tok.type = 'INDENT'

                yield indent_tok
            elif last_indent > indent:
                indent_tok.type = 'DEDENT'
                while indent_stack[-1] > indent:
                    indent_stack.pop()
                    yield indent_tok
                if indent_stack[-1] != indent:
                    raise IndentationError("unindent") 
            yield from tokens

# парсер
l = 0

def p_program(p):
    '''program : program statement
               | statement
               | '''
    global l 
    if len(p) == 2 and p[1]:
        p[0] = {}
        p[0][l] = p[1]
    elif len(p) == 3 and p[1]:
        p[1][l] = p[2]
        print(p[1])
        p[0] = p[1]
    l += 1
    


def p_block(p):
    '''block : NEWLINE INDENT groupstat DEDENT'''
    p[0] = (p[3])

def p_groupstat(p):
    '''groupstat : groupstat statement
                 | '''
    if len(p) == 3 and p[1]:
        p[0] = (p[1], p[2])
    elif len(p) == 3 and p[2]:
        p[0] = p[2]


def p_statement(p):
    '''statement : command NEWLINE
                 | command'''
    p[0] = p[1]
    """
    if len(p) == 3:
        lexer.lineno += 1
    p[0] = (lexer.lineno, p[1])"""


def p_command_ifblock(p):
    '''command : IFBLOCK RIGHT block ENDIF
               | IFBLOCK DOWN block ENDIF
               | IFBLOCK UP block ENDIF
               | IFBLOCK LEFT block ENDIF'''
    p[0] = (p[1], p[2], p[3])


def p_command_repeat(p):
    '''command : REPEAT expr block ENDREPEAT'''
    p[0] = (p[1], p[2], p[3])
    

def p_command_procedure(p):
    '''command : PROCEDURE ID block ENDPROC'''
    p[0] = (p[1], p[2], p[3])
    

def p_command_call(p):
    '''command : CALL ID'''
    p[0] = (p[1], p[2])


def p_command_dir(p):
    '''command : RIGHT expr
               | LEFT expr
               | UP expr
               | DOWN expr'''
    p[0] = (p[1], p[2])


def p_command_set(p):
    '''command : SET ID EQUALS expr'''
    p[0] = (p[1], p[2], p[4])


def p_expr(p):
    '''expr : expr PLUS factor
            | expr MINUS factor
            | factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binop', p[2], p[1], p[3])


def p_factor(p):
    '''factor : factor TIMES fact
              | factor DIVIDE fact
              | fact'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binop', p[2], p[1], p[3])


def p_fact_number(p):
    "fact : NUMBER"
    p[0] = ("num", p[1])

def p_fact_var(p):
    "fact : ID"
    p[0] = ("var", p[1])

def p_fact_paren(p):
    "fact : LPAREN expr RPAREN"
    p[0] = p[2]


def p_error(p):
    # вызвать кнопочку error из gui
    pass


# only for debugging

data = '''
IFBLOCK RIGHT
    RIGHT 5
ENDIF


'''

lexer = lex.lex()
lexer = IndentLex(lexer)
'''
print()
lexer.input(data)
for t in lexer:
    print(t)

parser = yacc.yacc()
res = parser.parse(data, lexer=lexer)
print(res)
'''
# 
def parse(data, lexer=lexer):
    parser = yacc.yacc()
    parser.error = 0
    p = parser.parse(data, lexer=lexer)
    if parser.error:
        return None
    return p

