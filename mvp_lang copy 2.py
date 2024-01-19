import lex
import parcer as yacc

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
    "NUMBER",
    "PLUS",
    "RPAREN",
    "TIMES",
    'NEWLINE',
    # чтобы обрабатывать отступы?
    'IDENT',
    'DEPEND',
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

def t_NUMBER(t):
    r"-?\d+"
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n'
    t.lexer.lineno += len(t.value)
    t.lexer.skip(1)
    t.type = 'NEWLINE'
    return t


def t_ignor(t):
    r'[ \n]+'
    pass


def t_error(t):
    print(f"\nIllegal character {t.value[0]!r} in line {lexer.lineno}") #
    t.lexer.skip(1)


lexer = lex.lex()
lexer.lineno = 0


# парсер

def p_program(p):
    '''program : statement'''
    if p[1]:
        p[0] = {}
        line, stat = p[1]
        p[0][line] = stat


def p_statement(p):
    '''statement : command NEWLINE
                 | command'''
    if len(p) == 2:
        lexer.lineno += 1
    lineno = lexer.lineno
    p[0] = (lineno, p[1])


def p_statement_blank(p):
    '''statement : NEWLINE
                 |  '''
    if len(p) == 1:
        lexer.lineno += 1
    lineno = lexer.lineno
    p[0] = (lineno, 'blank',)


"""
# просто идеи
def p_command_repeat(p):
    '''command : REPEAT expr NEWLINE block ENDREPEAT'''
    

def p_command_procedure(p):
    '''command : PROCEDURE ID NEWLINE block ENDPROC'''
    
def p_command_call(p):
    '''command : CALL ID'''
    

def p_block_commands(p):
    '''block : ''' # Есть идея группировать код с одинаковым кол-вом пробелов (кратным 4)
                   # в некий 'блок кода'

def p_command_ifblock(p):
    'command : IFBLOCK (RIGHT/DOWN/UP/LEft) NEWLINE block NEWLINE ENDIF'
    pass
"""


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
    print(f"\nSyntax error {p.value!r} (line:{lexer.lineno})")

parser = yacc.yacc()


def do_parse(file):
    with open(file) as file:
        while line := file.readline():
            print(f"Line: {line}", end="")
            r = yacc.parse(line, lexer=lexer)
            if r:
                print(f"  {r}")
