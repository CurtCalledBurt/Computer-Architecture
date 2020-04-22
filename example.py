PRINT = 1
HALT = 2
SAVE_REG = 3
PRINT_REG = 4

memory = [PRINT, PRINT, SAVE_REG, 0, 20, PRINT_REG, 0, HALT]

register = [0] * 8

pc = 0
running = True

while running:
    inst = memory[pc]

    if inst == PRINT:
        print("hey, look")
        pc += 1

    elif inst == HALT:
        running = False
    
    elif inst == SAVE_REG:
        reg_num = memory[pc+1]
        value = memory[pc+2]
        register[reg_num] = value
        pc += 3
    
    elif inst == PRINT_REG:
        reg_num = memory[pc+1]
        value = register[reg_num]
        print(value)
        pc += 2

    else:
        print("command not found, breaking program")
        running = False
