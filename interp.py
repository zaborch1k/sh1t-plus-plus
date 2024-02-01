# interp

class Interp:
    def __init__(self, prog):
        print(prog)
        self.prog = list(prog.values())
        print(self.prog, 'interp')#
    
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
                self.error = 'обращение к неопределенной переменной'
    
    def assign(self, target, value, type):
        var = target
        #self.vars[var] = self.eval(value)
        if var in self.vars.keys() and type == 'func' and self.vars[var][0] == 'func':
            self.error = 'объявление уже существующей процедуры'
        elif type == 'var':
            self.vars[var] = (type, self.eval(value))
        elif type == 'func':
            self.vars[var] = (type, value)

    
    def add_prog(self, prog):
        print(f'*добавляю прог {prog}*')
        print(self.prog)
        pc = self.pc
        pc += 1
        for i in prog:
            self.prog.insert(pc, i)
            pc += 1
            print('II', i)
        print('im done', self.prog) #
    
    def run(self):
        self.vars = {}
        self.loops = {}
        self.error = None
        self.qmove = []
        self.pos = [11, 11]
        m = 21
        print('i am running')

        #self.stat = prog[self.pc] # реaлизовать 
        # в виде prog.keys(), когда сделаю prog cловарем. 
        # это будет список всех строк
        self.pc = 0

        #if self.error:
         #   raise RuntimeError
        
        while 1:
            # line = self.stat[self.pc]
            # instr = ... # 
            print('new NEW NEW NEW')
            try:
                instr = self.prog[self.pc]
                print('INSTR:', instr) #
            except:
                break
            op = instr[0]

            if op == 'SET':
                target = instr[1]
                value = instr[2]
                self.assign(target, value, 'var')

            elif op in ('RIGHT', 'LEFT', 'DOWN', 'UP'):
                num = self.eval(instr[1])
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
                    self.add_prog(self.vars[instr[1]][1])
                else:
                    self.error = 'вызов неопределенной функции'

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
                    self.add_prog(instr[2])

            elif op == 'PROCEDURE':
                self.assign(instr[1], instr[2], 'func')
                print(instr[2])
                #self.vars[instr[1]] = instr[2]

            elif op == 'REPEAT':
                for i in range(0, self.eval(instr[1])):
                    self.add_prog(instr[2])
            
            if self.pos[0] > m or self.pos[1] > m or self.pos[0] < 0 or self.pos[1] <0 :
                del self.qmove[-1]
                self.error = 'попытка выйти за границы поля'
            # добавить syntaxerror из lexparse
                
            if self.error:
                print('*отправка данных в gui*')
                print((self.qmove, self.error))
                break
            self.pc += 1
            print('pos:', self.pos) #
            print('queue to move:', self.qmove) #
            print('vars:', self.vars) #


def get_data(data):
    do_interp(data)


def do_interp(data):
    from lexparse import parse
    i = 0
    data = parse(data)
    i = Interp(data)
    i.run()
