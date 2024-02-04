# файл с лексером и парсером
import pycparser.ply.lex as lex
import pycparser.ply.yacc as yacc
from pycparser.ply.lex import LexToken

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

error = None

def t_error(t):
    global error
    error = f"недопустимый символ '{t.value[0]}'"
    t.lexer.skip(1)
    


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
            
def check_nest_lvl():
    global nest_lvl
    nest_lvl += 1
    err = None
    if nest_lvl > 3:
        err = True
    return err


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
    '''statement : command NEWLINE'''
    p[0] = p[1]
    

def p_command_ifblock(p):
    '''command : IFBLOCK RIGHT block ENDIF
               | IFBLOCK DOWN block ENDIF
               | IFBLOCK UP block ENDIF
               | IFBLOCK LEFT block ENDIF'''
    err = check_nest_lvl()
    if err:
        p[0] = 'превышение максимального уровня вложенности (больше 3)'
    else:
        p[0] = (p[1], p[2], p[3])

def p_command_ifblock_error(p):
    '''command : IFBLOCK error'''
    global error
    error = f"недопустимый параметр для IFBLOCK: {p[2].value}"

def p_command_ifblock_error1(p):
    '''command : IFBLOCK RIGHT error
               | IFBLOCK DOWN error
               | IFBLOCK UP error
               | IFBLOCK LEFT error'''
    global error
    error = f'нет отступа после IFBLOCK {p[2]}'

def p_command_ifblock_error2(p):
    '''command : IFBLOCK RIGHT block error
               | IFBLOCK DOWN block error
               | IFBLOCK UP block error
               | IFBLOCK LEFT block error'''
    global error
    error = f'нет ENDIF для IFBLOCK'


def p_command_repeat(p):
    '''command : REPEAT expr block ENDREPEAT'''
    err = check_nest_lvl()
    if err:
        p[0] = 'превышение максимального уровня вложенности (больше 3)'
    else:
        p[0] = (p[1], p[2], p[3])

def p_command_repeat_error(p):
    '''command : REPEAT error'''
    global error
    error = f'недопустимый параметр для {p[1]}: {p[2].value}'

def p_command_repeat_error1(p):
    '''command : REPEAT expr error'''
    global error
    error = f'нет отступа после REPEAT'

def p_command_repeat_error2(p):
    '''command : REPEAT expr block error
               | REPEAT expr block'''
    global error
    error = f'нет ENDREPEAT для REPEAT'


def p_command_procedure(p):
    '''command : PROCEDURE ID block ENDPROC'''
    err = check_nest_lvl()
    if err:
        p[0] = 'превышение максимального уровня вложенности (больше 3)'
    else:
        p[0] = (p[1], p[2], p[3])

def p_command_procedure_error(p):
    '''command : PROCEDURE error'''
    global error
    if p[2].value == '\n':
        error = f'отсутствует имя процедуры'
    else:
        error = f'недопустимое имя процедуры: {p[2].value}'

def p_command_procedure_error1(p):
    '''command : PROCEDURE ID NEWLINE error
               | PROCEDURE ID error'''
    global error
    error = f'нет отступа после PROCEDURE'

def p_command_procedure_error2(p):
    '''command : PROCEDURE ID block error'''
    global error
    error = f'нет ENDPROC для PROCEDURE'


def p_command_call(p):
    '''command : CALL ID'''
    p[0] = (p[1], p[2])

def p_command_call_error(p):
    '''command : CALL error'''
    global error
    error = f"недопустимый параметр для {p[1]}: '{p[2].value}' "


def p_command_dir(p):
    '''command : RIGHT expr
               | LEFT expr
               | UP expr
               | DOWN expr'''
    p[0] = (p[1], p[2])

def p_command_dir_error(p):
    '''command : RIGHT error
               | LEFT error
               | UP error
               | DOWN error'''
    global error
    error = f"недопустимый параметр для {p[1]}: '{p[2].value}' "


def p_command_set(p):
    '''command : SET ID EQUALS expr'''
    p[0] = (p[1], p[2], p[4])

def p_command_set_error(p):
    '''command : SET error '''
    global error
    error = f"недопустимое имя переменной: '{p[2].value}'"

def p_command_set_error2(p):
    '''command : SET ID error '''
    global error
    error = f"нет '=' в выражении SET"

def p_command_set_error3(p):
    '''command : SET ID EQUALS error '''
    global error
    error = f"недопустимое значение для переменной: '{p[4].value}'"


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
    global error
    if p:
        error = f"недопустимая команда '{p.value}"
    else:
        pass


# only for debugging

data = '''SET X = X+5
'''


def parse(data):
    data = data + '\n'
    print(data)
    global error, l, nest_lvl
    l = 0
    nest_lvl = 0
    lexer = lex.lex(debug=True)
    lexer = IndentLex(lexer)
    parser = yacc.yacc(debug=True)
    p = parser.parse(data, lexer=lexer, debug=True)
    if error:
        return {'0': error}
    return p

print(parse(data))