# interp бэкап
import lexparse_b

class Interp:
    def __init__(self, prog):
        if not isinstance(prog, list):
            self.bprog = [prog]
        else:
            self.bprog = prog
        print(self.bprog)
        self.prog = self.bprog
    
    def check_loops_etc(self):
        for pc in range(len(self.stat)):
            lineno = self.stat[pc]
            if self.prog[lineno][0] == 'REPEAT':
                pass
            elif self.prog[lineno][0] == 'IFBLOCK':
                pass
            elif self.prog[lineno][0] == 'varsEDURE':
                pass
    
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
        self.error = 0

        #self.stat = prog[self.pc] # реaлизовать 
        # в виде prog.keys(), когда сделаю prog cловарем. 
        # это будет список всех строк
        self.pc = 0

        if self.error:
            raise RuntimeError
        
        print('lets go')
        
        while 1:
            # line = self.stat[self.pc] ^ сверху написано
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
                print('*жосткая связь с графикой*')
                # отправка (-> gui): move(instr[1], self.eval(instr[2])))


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

            elif op == 'blank':
                pass

            self.pc += 1
            print(self.pc) # 

# only for debugging
'''
prog = [('RIGHT', ('num', 3)), ('DOWN', ('num', 4))]
i = Interp(prog)
try:
    i.run()
    raise SystemExit
except RuntimeError:
    pass
'''



