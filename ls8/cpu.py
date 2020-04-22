"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 0xF4

    def load(self):
        """Load a program into memory."""

        address = 0

        # get the prgram file name from sys.argv
        program_filename = sys.argv[1]

        # "./" means "in the current directory", which is the folder that our current file is in, which is Computer-Architecture/ls8
 
        f = open(f"./examples/{program_filename}", 'r')

        for line in f:
            # process text
            # split strings on '#' to remove comments from numbers
            line = line.split('#') # line is now an array
            # we know the program is the first non-whitespace in each line wherever it appears, so ...
            # extract the first thing in the line array, and remove whitespace from it
            line = line[0].strip()
            # if it is empty, do nothing, move on to next line
            if line == '':
                continue
            
            # convert the instruction string into a binary integer
            instruction = int(line, 2)
            
            # store the instruction in RAM
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def ram_read(self, pc):
        return self.ram[pc]

    def ram_write(self, pc, value):
        self.ram[pc] = value

    def run(self):
        """Run the CPU."""

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110

        running = True
        while running:
            inst = self.ram[self.pc]

            inst_len = ((inst & 0b11000000) >> 6) + 1

            ALU = ((inst & 0b00100000) >> 5) 

            # load value into given register
            if inst == LDI:
                reg_num = self.ram[self.pc+1]
                value = self.ram[self.pc+2]
                self.reg[reg_num] = value

            # print value in given register
            elif inst == PRN:
                reg_num = self.ram[self.pc+1]
                value = self.reg[reg_num]
                print(value)

            elif inst == MUL:
                # multiply 2 numbers together, placing the result in the first given register
                reg_num1 = self.ram[self.pc+1]
                reg_num2 = self.ram[self.pc+2]
                value1 = self.reg[reg_num1]
                value2 = self.reg[reg_num2]
                value3 = value1 * value2
                self.reg[reg_num1] = value3
            
            elif inst == PUSH:
                # decrement sp counter, 
                # place value from given register where the sp is currently pointing 
                self.sp -= 1
                reg_num = self.ram[self.pc+1]
                self.ram[self.sp] = self.reg[reg_num]
            
            elif inst == POP:
                # if stack is empty:
                # place value where sp is currently pointing into given register
                # do NOT increment sp counter
                if self.sp == 0xF4:
                    reg_num = self.ram[self.pc+1]
                    self.reg[reg_num] = self.ram[self.sp]

                # if stack has something in it:
                # place value where sp is currently pointing into the given register,
                # increment sp counter
                else:
                    reg_num = self.ram[self.pc+1]
                    self.reg[reg_num] = self.ram[self.sp]
                    self.sp += 1

            # end program
            elif inst == HLT:
                running = False

            else:
                print("Error: Command not found, ending program")
                running = False
            
            self.pc += inst_len

