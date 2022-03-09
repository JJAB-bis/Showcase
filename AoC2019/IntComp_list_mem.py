DAYS = [2, 5, 7]
import unittest

class IntComp:

    class Instruction:
        def __init__(self, instr):
            self.modes = [int(i) for i in instr[:3]]
            self.code   = int(instr[3:])
            # print(self)
        def __str__(self):
            return f"code: {self.code}, modes: {self.modes}"
        def __len__(self):
            return len(self.args)

    def __init__(self, f=None, instr_size=4):
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
        self.relative_base       = 0

    def copy(self):
        n = IntComp()
        n.input_program = self.input_program.copy()
        return n
    
    def run(self, memory:[int,...]=None, debugging:'Debugging_Manager' = None):
        self.memory = self.input_program.copy() if memory is None else memory.copy()
        self.output = []
        self.instruction_pointer = 0
        self.running = True
        while self.running:
                
            instr = self.get_instruction()
            if instr.code == 3:
                yield from self.OPCODES[instr.code](instr)
                continue
            self.OPCODES[instr.code](instr)
        yield self.output
    
    def get_instruction(self, instr_size=5):
        # print('-----', self.memory)
        instr = self.Instruction(f"{self.memory[self.instruction_pointer]:>0{instr_size}}")
        self.instruction_pointer += 1
        return instr
    
    def get_index(self, mode):
        if   mode == 0:
            return self.memory[self.instruction_pointer]
        elif mode == 1:
            return self.instruction_pointer
        elif mode == 2:
            return self.memory[self.instruction_pointer] + self.relative_base
        else:
            raise ValueError(f'{mode=}, is not supported yet')

    def get_param(self, mode):
        indx = self.get_index(mode)
        self.instruction_pointer += 1
        return self.memory[indx]


    def set_mem(self, value, mode):
        indx = self.get_index(mode)
        self.memory[indx] = value
        self.instruction_pointer += 1


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
        lines = [int(each) for each in f.read().strip().split(',')]
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

