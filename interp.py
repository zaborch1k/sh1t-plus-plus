# interp

class Interp:
    def __init__(self, prog):
        self.bprog = list(prog.values())
        self.prog = self.bprog
        print(self.prog)#
    
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
                # вызов ошибки из gui
                print('undefined %s variable at line %s' %
                      (var, self.stat[self.pc])) #
                raise RuntimeError
    
    def assign(self, target, value):
        var = target
        self.vars[var] = self.eval(value)
    
    def add_prog(self, prog):
        print(f'*добавляю прог {prog}*')
        self.prog.insert(self.pc+1, prog)
        print(self.prog) #
    
    def run(self):
        self.vars = {}
        self.loops = {}
        self.error = None
        self.qmove = []
        self.pos = [11, 11]
        m = 21

        #self.stat = prog[self.pc] # реaлизовать 
        # в виде prog.keys(), когда сделаю prog cловарем. 
        # это будет список всех строк
        self.pc = 0

        if self.error:
            raise RuntimeError
        
        while 1:
            # line = self.stat[self.pc]
            # instr = ... # 
            try:
                instr = self.prog[self.pc]
                print('INSTR:', instr) #
            except:
                break
            op = instr[0]

            if op == 'SET':
                target = instr[1]
                value = instr[2]
                self.assign(target, value)
                print(self.vars) #

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
                print(self.pos) #
                print('queue to move:', self.qmove) #

            elif op == 'CALL':
                if instr[1] in self.vars:
                    self.add_prog(instr[2])
                else:
                    print('*oops, idk var %s*' % instr[1])
                    # error

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
                self.vars[instr[1]] = instr[2]

            elif op == 'REPEAT':
                for i in range(0, self.eval(instr[1])):
                    self.add_prog(instr[2])
            
            if self.pos[0] > m or self.pos[1] > m or self.pos[0] < 0 or self.pos[1] <0 :
                print('*вызов исключения в gui*')
                break
            # добавить syntaxerror из lexparse

            self.pc += 1


def get_data(data):
    print('hey there, i am from interp\n', data)
    do_interp(data)


def do_interp(data):
    from lexparse import parse
    i = Interp(parse(data))
    i.run()

# only for debugging
if __name__ == '__main__':
    from lexparse  import parse
    prog = parse(data)
    i = Interp(prog)
    try:
        i.run()
        raise SystemExit
    except RuntimeError:
        pass

