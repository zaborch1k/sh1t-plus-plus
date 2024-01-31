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
                print('undefined %s variable at line %s' %
                      (var, self.stat[self.pc]))
                raise RuntimeError
    
    def assign(self, target, value):
        var = target
        self.vars[var] = self.eval(value)
    
    def run(self):
        self.vars = {}
        self.loops = {}
        self.error = None
        self.qmove = []
        self.pos = [11, 11]
        self.m = 21

        #self.stat = prog[self.pc] # реaлизовать 
        # в виде prog.keys(), когда сделаю prog cловарем. 
        # это будет список всех строк
        self.pc = 0

        if self.error:
            raise RuntimeError
        
        print('lets go')
        
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
                print(self.pos)
                print('queue to move:', self.qmove)

            elif op == 'CALL':
                if instr[1] in self.vars:
                    print('*i find a var %s*' %instr[1])
                    self.prog.insert(self.pc+1, self.vars[instr[1]])
                    print(self.prog)
                else:
                    print('*oops, idk var %s*' % instr[1])
                    # error

            elif op == 'IFBLOCK':
                print('*жосткая связь c графикой*')
                # отправка gui -> instr[1]
                # получение ответа-переменной -> marker = func()
                marker = True # 
                if marker == True:
                    self.prog.insert(self.pc+1, self.vars[instr[1]])
                    print(self.prog)
                    # пока не работает обр. нескольких строк в block
                    pass

            elif op == 'PROCEDURE':
                self.vars[instr[1]] = instr[2]
                print(self.vars) # 

            elif op == 'REPEAT':
                for i in range(0, self.eval(instr[1])):
                    self.prog.insert(self.pc+1, instr[2])
                    print(self.prog) #
            
            if self.pos[0] > 21 or self.pos[1] > 21 or self.pos[0] < 0 or self.pos[1] <0 :
                print('*вызов исключения в gui*')
                break

            if self.error:
                # добавить вызов error из lexparser
                pass

            self.pc += 1
            print(self.pc) # 


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

