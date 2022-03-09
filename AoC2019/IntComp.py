DAYS = [2, 5, 7, 9, 11]
import unittest
print('test_output')
class IntComp:

    class Instruction: #TODO her is a bug probably :S
        def __init__(self, instr):
            # print( instr, end = ' ' )
            self.instr = instr
            self.modes = [int(i) for i in instr[:3]]
            self.code   = int(instr[3:])
            # print(self)
        def __str__(self):
            return f"code: {self.code}, modes: {self.modes}"
        def __repr__(self):
            return f"{self.instr=}"
        def __len__(self):
            return len(self.args)

    def __init__(self, f=None, instr_size=5):
        self.OPCODES = {
            1  : self.OpCode1,
            2  : self.OpCode2,
            3  : self.OpCode3,
            4  : self.OpCode4,
            5  : self.OpCode5,
            6  : self.OpCode6,
            7  : self.OpCode7,
            8  : self.OpCode8,
            9  : self.OpCode9,
            99 : self.OpCode99
        }
        self.input_program       = None if f is None else self._strip_inp(f)
        self.instr_size          = instr_size
        self.instruction_pointer = None
        self.memory              = None

    def copy(self):
        n = IntComp()
        n.input_program = self.input_program.copy()
        return n
    
    def run(self, memory:{int:int}=None, relative_base:int=0, status_updates=False):
        self.memory = self.input_program.copy() if memory is None else {i:each for i,each in enumerate(memory) }
        self.output = []
        self.instruction_pointer = 0
        self.relative_base       = relative_base
        self.running = True
        
        self.status_updates = status_updates
        self.status  = 'Running'; 
        if self.status_updates: print(self.status)
        self.log = []

        while self.running:
                
            instr = self.get_instruction()
            self.log.append(instr)
            if instr.code == 3:
                self.status  = 'Awaiting input'
                if self.status_updates: print(self.status)
                yield from self.OPCODES[instr.code](instr)
                self.status  = 'Running'
                if self.status_updates: print(self.status)
                continue
            try:
                self.OPCODES[instr.code](instr)
            except Exception as e:
                if repr(instr) != "self.instr='00000'":
                    print( repr("self.instr='00000'"), repr("self.instr='00000'"))
                    print(self.log)
                self.OPCODES[ 99 ](instr)
        self.status  = 'Finished'
        if self.status_updates: print(self.status)
        yield self.output
    
    def get_instruction(self, instr_size=None):
        instr = self.Instruction(f"{self.memory[self.get_index(1)]:>0{self.instr_size if instr_size is None else instr_size}}")
        # print(instr)
        self.instruction_pointer += 1
        return instr

    def get_param(self, mode):
        indx = self.get_index(mode)
        self.instruction_pointer += 1
        return self.memory[indx]

    def set_mem(self, value, mode):
        indx = self.get_index(mode)
        self.memory[indx] = value
        self.instruction_pointer += 1
    
    def get_out(self, n:int):
        return self.output[-n:]

    def get_index(self, mode):
        if   mode == 0:
            indx = self.memory[self.instruction_pointer]
        elif mode == 1:
            indx = self.instruction_pointer
        elif mode == 2:
            indx = self.memory[self.instruction_pointer] + self.relative_base
        else:
            raise ValueError(f'{mode=}, is not supported yet')
        try:
            self.memory[indx] * 2
            return indx
        except KeyError as e:
            self.memory[indx] = 0
            return indx

    def DEPRECATED_get_param(self, mode):
        if   mode == 0:
            param = self.memory[self.memory[self.instruction_pointer]]
        elif mode == 1:
            param = self.memory[self.instruction_pointer]
        elif mode == 2:
            param = self.memory[self.memory[self.instruction_pointer] + self.relative_base]
        self.instruction_pointer += 1
        return param

    def DEPRECATED_set_mem(self, value, mode):
        if mode == 0:
            self.memory[self.memory[self.instruction_pointer]] = value
        elif mode == 1:
            self.memory[self.instruction_pointer] = value
        elif mode == 2:
            self.memory[self.memory[self.instruction_pointer] + self.relative_base] = value
        self.instruction_pointer += 1

    def _strip_inp(self,f):
        lines = {i : int(each) for i, each in enumerate(f.read().strip().split(',')) }
        return lines

    
    def OpCode1(self,instr):
        m3,m2,m1  = instr.modes
        param1 = self.get_param(m1)
        param2 = self.get_param(m2)
        value = param1 + param2
        self.set_mem(value, m3)

    def OpCode2(self,instr):
        m3,m2,m1  = instr.modes
        param1 = self.get_param(m1)
        param2 = self.get_param(m2)
        value = param1 * param2
        self.set_mem(value, m3)

    def OpCode3(self,instr):
        *_,m1  = instr.modes
        value = int((yield))
        self.set_mem(value, m1)

    def OpCode4(self,instr):
        *_,m1  = instr.modes
        param1 = self.get_param(m1)
        self.output.append(param1)
    
    def OpCode5(self,instr):
        *_,m2,m1  = instr.modes
        param1 = self.get_param(m1)
        param2 = self.get_param(m2)
        if param1 != 0:
            self.instruction_pointer = param2

    def OpCode6(self,instr):
        *_,m2,m1  = instr.modes
        param1 = self.get_param(m1)
        param2 = self.get_param(m2)
        if param1 == 0:
            self.instruction_pointer = param2
    
    def OpCode7(self,instr):
        m3,m2,m1  = instr.modes
        param1 = self.get_param(m1)
        param2 = self.get_param(m2)
        self.set_mem(int(param1 < param2), m3)

    def OpCode8(self,instr):
        m3,m2,m1  = instr.modes
        param1 = self.get_param(m1)
        param2 = self.get_param(m2)
        self.set_mem(int(param1 == param2), m3)

    def OpCode9(self,instr):
        _,_,m1  = instr.modes
        param1 = self.get_param(m1)
        self.relative_base += param1
        

    def OpCode99(self,*args):
        try:
            self.running = False
        except Exception as e:
            raise e



if __name__ == "__main__":
    from test_IntComp import *
    unittest.main()

