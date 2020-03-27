"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    """
    When the LS-8 is booted, the following steps occur:
        R0-R6 are cleared to 0. [DONE]
        R7 is set to 0xF4. [DONE]
        PC and FL registers are cleared to 0. [DONE]
        RAM is cleared to 0. [DONE]
    """
    def __init__(self):
        """Construct a new CPU."""

        # Memory:
        """
        The CPU class to hold 256 bytes of memory [DONE]
        """
        self.ram = bytearray([0] * 256)

        # 8 general registers
        """
        R5 is reserved as the interrupt mask (IM)
        R6 is reserved as the interrupt status (IS)
        R7 is reserved as the stack pointer (SP)
        """
        self.reg = bytearray([0] * 7 + [0xF4])

        # Internal registers:
        """
        PC: Program Counter, address of the currently executing instruction
        """
        self.pc = 0

        """
        IR: Instruction Register, contains a copy of the currently executing instruction
        """
        self.ir = 0

        """
        MAR: Memory Address Register, holds the memory address we're reading or writing
        """
        self.mar = 0

        """
        MDR: Memory Data Register, holds the value to write or the value just read
        """
        self.mdr = 0

        """
        FL: Flags, bits: 00000LGE
        L Less-than: during a CMP, set to 1 if registerA is less than registerB, zero otherwise.
        G Greater-than: during a CMP, set to 1 if registerA is greater than registerB, zero otherwise.
        E Equal: during a CMP, set to 1 if registerA is equal to registerB, zero otherwise.
        
        8 bits == 1 byte, so:
        L: 00000100
        G: 00000010
        E: 00000001
        """
        self.fl = [0b00000000]

        """
        Instruction Registry Dictionary:
        
        [0b10100111] == CMP
        [0b00000001] == HLT
        [0b01010101] == JEQ
        [0b01010100] == JMP
        [0b01010110] == JNE
        [0b10000010] == LDI
        [0b10100010] == MUL
        [0b01000110] == POP
        [0b01000111] == PRN
        [0b01000101] == PUSH
        """
        self.ir = {
            0b10100111: self.CMP_handler,
            0b00000001: self.HLT_handler,
            0b01010101: self.JEQ_handler,
            0b01010100: self.JMP_handler,
            0b01010110: self.JNE_handler,
            0b10000010: self.LDI_handler,
            0b10100010: self.MUL_handler,
            0b01000110: self.POP_handler,
            0b01000111: self.PRN_handler,
            0b01000101: self.PUSH_handler
        }

    def ram_read(self, mar):
        """
        Should accept the address to read and return the value stored there.
        """
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        """
        Should accept a value to write, and the address to write it to.
        """
        self.ram[mar] = mdr
        # return self.ram[mar]

    def load(self, file):
        """Load a program into memory."""

        try:
            with open(file) as f:
                address = 0
                for line in f:
                    # Split the line if it has comments
                    removed_comments = line.strip().split("#")

                    # Take the 0th element and strip out spaces
                    line_string_value = removed_comments[0].strip()

                    # If line is blank, skip it
                    if line_string_value == "":
                        continue

                    # Convert line to an int value, base 2
                    num = int(line_string_value, 2)

                    # Save it to memory
                    self.ram[address] = num

                    # Increment the address counter
                    address += 1

                # Close the file when done.
                f.close()

        except FileNotFoundError:
            print("--- File Not Found ---")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def CMP_handler(self):
        """
        This is an instruction handled by the ALU.
        CMP registerA registerB

        LS-8 Spec:
            Compare the values in two registers.
            If they are equal, set the Equal E flag to 1, otherwise set it to 0.
            If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
            If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.

            Machine code:

                10100111 00000aaa 00000bbb
                A7 0a 0b
        """
        pass

    def HLT_handler(self):
        """
        Add the HLT instruction definition to cpu.py so that you can
        refer to it by name instead of by numeric value.

        In run() in your switch, exit the loop if a HLT instruction is
        encountered, regardless of whether or not there are more lines
        of code in the LS-8 program you loaded.

        We can consider HLT to be similar to Python's exit() in that
        we stop whatever we are doing, wherever we are.

        LS-8 Spec:
            Halt the CPU (and exit the emulator).

            Machine Code:
                00000001
                01
        """
        sys.exit(0)

    def JEQ_handler(self):
        """
        LS-8 Spec:
            If equal flag is set (true), jump to the address stored in the
            given register.

            Machine code:
                01010101 00000rrr
                55 0r
        """
        pass

    def JMP_handler(self):
        """
        Jump to the address stored in the given register.

        LS-8 Spec:
            Set the PC to the address stored in the given register.

            Machine code:
                01010100 00000rrr
                54 0r
        """
        pass

    def JNE_handler(self):
        """
        LS-8 Spec:
            If E flag is clear (false, 0), jump to the address stored in the given register.

            Machine code:
                01010110 00000rrr
                56 0r
        """
        pass

    def LDI_handler(self):
        """
        This instruction sets a specified register to a specified value.

        LS-8 Spec:
            Set the value of a register to an integer.

            Machine Code:
                10000010 00000rrr iiiiiiii
                82 0r ii
        """
        # Get the address and value from Memory
        address = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)

        # Write it to the registry
        self.reg[address] = value

        # Advance the Program Counter
        self.pc += 3

    def MUL_handler(self):
        """
        This is an instruction handled by the ALU.

        MUL registerA registerB

        Multiply the values in two registers together and store
        the result in registerA.

        LS-8 Spec:
            Machine code:
                10100010 00000aaa 00000bbb
                A2 0a 0b
        """
        # Get the values from Memory
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)

        # Hit up the ALU to multiply
        self.alu("MUL", reg_a, reg_b)

        # Advance the Program Counter
        self.pc += 3

    def POP_handler(self):
        """
        Pop the value at the top of the stack into the given register.

        LS-8 Spec:
            Copy the value from the address pointed to by SP to the
             given register.

            Increment SP.

            Machine code:
                01000110 00000rrr
                46 0r
        """
        # Get the value from Memory using the Stack Pointer
        address = self.ram_read(self.pc + 1)
        value = self.ram[self.reg[7]]

        # Copy it to the given registry
        self.reg[address] = value

        # Increment the Stack Pointer
        self.reg[7] += 1

        # Increment the Program Counter
        self.pc += 2

    def PRN_handler(self):
        """
        This is a very similar process to adding LDI, but the handler is
        simpler.

        LS-8 Spec:
            Print numeric value stored in the given register.
            Print to the console the decimal integer value that is stored
             in the given register.
        
            Machine code:
                01000111 00000rrr
                47 0r
        """
        # Get the address
        address = self.ram_read(self.pc + 1)

        # Print the value
        print(self.reg[address])

        # Advance the Program Counter
        self.pc += 2

    def PUSH_handler(self):
        """
        Push the value in the given register on the stack.

        LS-8 Spec:
            Decrement the SP.
            Copy the value in the given register to the address
             pointed to by SP.

            Machine code:
                01000101 00000rrr
                45 0r
        """
        # Get the value from Register
        address = self.ram_read(self.pc + 1)
        value = self.reg[address]

        # Decrement the Stack Pointer
        self.reg[7] -= 1

        # Copy in the given registry value using the Stack Pointer
        self.ram[self.reg[7]] = value

        # Increment the Program Counter
        self.pc += 2


    def run(self):
        """
        Run the CPU.

        It needs to read the memory address that's stored in register
        PC, and store that result in IR, the Instruction Register. This
        can just be a local variable in run().

        Some instructions requires up to the next two bytes of data
        after the PC in memory to perform operations on. Sometimes the
        byte value is a register number, other times it's a constant
        value (in the case of LDI). Using ram_read(), read the bytes at
        PC+1 and PC+2 from RAM into variables operand_a and operand_b in
        case the instruction needs them.

        Then, depending on the value of the opcode, perform the actions
        needed for the instruction per the LS-8 spec. Maybe an if-elif
        cascade...? There are other options, too.

        After running code for any particular instruction, the PC needs
        to be updated to point to the next instruction for the next
        iteration of the loop in run(). The number of bytes an instruction
        uses can be determined from the two high bits (bits 6-7) of the
        instruction opcode. See the LS-8 spec for details.
        """
        while True:
            IR = self.ram[self.pc]

            # Get dictionary entry then execute returned instruction
            instruction = self.ir[IR]
            instruction()
