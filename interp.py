from mvp_lang_copy_2 import *
import sys

#do_parse('test.txt')

class Interp:
    def __init__(self, prog):
        self.prog = prog
        self.error = 0
    
    def eval(self, expr):
        etype = expr[0]
        if etype == 'num':
            return expr[1]
        elif etype == 'binop':
            if expr[1] == '+':
                return self.eval(expr[2]) + self.eval(expr[3])
            elif expr[1] == '-':
                return self.eval(expr[2]) - self.eval(expr[3])
            elif expr[1] == '*':
                return self.eval(expr[2]) * self.eval(expr[3])
            elif expr[1] == '/':
                return float(self.eval(expr[2])) / self.eval(expr[3])
        elif etype == 'var':
            var = expr[1]
            if var in self.vars:
                return self.vars[var]
            else:
                print('undefinded variable %s (line:%s)' %
                (var, self.stat[self.pc]))
                raise RuntimeError
        
    def assign(self, target, value):
        var = target
        self.vars[var] = self.eval(value)
        print('assign {self.vars[var]}')
    
    def run(self):
        self.vars = {}
        self.errors = 0
        
        self.stat = list(self.prog)
        self.stat.sort()
        self.pc = 0
        

        if self.error:
            raise RuntimeError
    
        while 1:
            line = self.stat[self.pc]
            instr = self.prog[line]

            op = instr[0]

            if op == 'SET':
                target = instr[1]
                value = instr[2]
                self.assign(target, value)
        
            elif op in ('RIGHT', 'LEFT', 'DOWN', 'UP'):
                value = self.eval(instr[1])
                print('*жосткая связь с графикой*')
                # отправить op и value

        def new(self):
            self.prog = {}
        

        def add_statement(self, prog):
            for line, stat in prog.items():
                self.prog[line] = stat


def parse(file):
    with open(file) as file:
        while line := file.readline():
            r = yacc.parse(line, lexer=lexer)
            return r

b = Interp(parse('test.txt'))
b.run()

