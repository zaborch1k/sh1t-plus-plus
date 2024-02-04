# interp

class Interp:
    def __init__(self, prog):
        print(prog)
        self.prog = list(prog.values())
    
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
                return float(self.eval(expr[2]) / self.eval(expr[3]))
        elif etype == 'var':
            var = expr[1]
            if var in self.vars:
                if self.vars[var][0] == 'func':
                    self.error = 'присвоение переменной значения процедуры'
                else:
                    return self.vars[var]
            else:
                self.error = 'обращение к неопределенной переменной'
    
    def assign(self, target, value, type):
        var = target
        if var in self.vars.keys() and type == 'func' and self.vars[var][0] == 'func':
            self.error = 'объявление уже существующей процедуры'
        elif type == 'var':
            value = self.eval(value)
            while not self.error:
                self.error = self.check_range_error(value)
                self.vars[var] = (type, value)
                break
        elif type == 'func':
            self.vars[var] = (type, value)
    
    def check_range_error(self, num):
        msg = None
        if not isinstance(num, int):
            msg = 'не принимает нецелые значения'
        elif num < 1:
            msg = 'не может быть < 1'
        elif num > 1000:
            msg = 'не может быть > 1000'

        if msg:
            return f'неверное значение параметра процедуры({msg})' 
        else:
            return None
    
    def run(self):
        self.vars = {}
        self.error = None
        self.qmove = []
        self.pos = [11, 11]
        m = 21
        print('i am running')
        self.pc = 0

        while 1:
            print('\nnew NEW NEW NEW\n') ##
            try:
                if isinstance(self.prog[0], str):
                    self.error = self.prog[0]
                    self.prog = []
                    op = None
                else:
                    instr = self.prog[self.pc]
                    print('INSTR:', instr) #
                    op = instr[0]
            except:
                from gui import movedata
                movedata((self.qmove, self.error))
                break

            if op == 'SET':
                target = instr[1]
                value = instr[2]
                self.assign(target, value, 'var')

            elif op in ('RIGHT', 'LEFT', 'DOWN', 'UP'):
                num = self.eval(instr[1])
                self.error = self.check_range_error(num)

                if not self.error:
                    self.qmove.append((op, num))
                    if op == 'RIGHT':
                        self.pos[0] += num
                    elif op == 'LEFT':
                        self.pos[0] -= num
                    elif op == 'UP':
                        self.pos[1] += num
                    else:
                        self.pos[1] -= num

            elif op == 'CALL':
                if instr[1] in self.vars:
                    del self.prog[self.pc]
                    self.prog.insert(self.pc+1, self.vars[instr[1]][1])
                    self.pc -= 1
                else:
                    self.error = 'вызов неопределенной процедуры'

            elif op == 'IFBLOCK':
                marker = False
                if instr[1] == 'RIGHT':
                    if self.pos[0] == m:
                        marker = True
                if instr[1] == 'LEFT':
                    if self.pos[0] == 0:
                        marker = True
                if instr[1] == 'UP':
                    if self.pos[1] == m:
                        marker = True
                else:
                    if self.pos[1] == 0:
                        marker = True
                
                if marker:
                    del self.prog[self.pc]
                    self.prog.insert(self.pc+1, instr[2])
                    self.pc -= 1

            elif op == 'PROCEDURE':
                self.assign(instr[1], instr[2], 'func')

            elif op == 'REPEAT':
                self.error = self.check_range_error(self.eval(instr[1]))
                if not self.error:
                    del self.prog[self.pc]
                    for i in range(0, self.eval(instr[1])):
                        self.prog.insert(self.pc+1, instr[2])
                    self.pc -= 1
            
            if self.pos[0] > m or self.pos[1] > m or self.pos[0] < 0 or self.pos[1] <0 :
                del self.qmove[-1]
                self.error = 'попытка выйти за границы поля'
                
            if self.error:
                print((self.qmove, self.error))
                self.prog = {}
            self.pc += 1
            print('pos:', self.pos) #
            print('queue to move:', self.qmove) #
            print('vars:', self.vars) #


def get_data(data):
    do_interp(data)


def do_interp(data):
    from lexparse_b import parse
    i = 0
    data = parse(data)
    i = Interp(data)
    i.run()
