# -*- coding: utf-8 -*-

from array import array

class ZCodeError(Exception):
    pass

class StoryFile(array):

    def __new__(cls, loadedfile):
        return array.__new__(cls, 'B')
    # Create the StoryFile object as a byte array

    def __init__(self, loadedfile):

        for line in loadedfile:
            self.fromstring(line)
            if len(self) > 0x7d000:
                raise ZCodeError(
                    'Z-code file exceeded maximum length of 512kb.')
        # Take an open file as input and read its contents into the array

        self.version = self[0]

        if self.version > 8:
            raise ZCodeError(
                'Z-code file reports invalid version {}.'.format(self.version))

        if self.version > 2:
            self.storedlength = catbytes(self[0x1a:0x1c])
            if self.version == 3:
                self.storedlength = self.storedlength * 2
            elif self.version < 6:
                self.storedlength = self.storedlength * 4 
            elif self.version < 9:
                self.storedlength = self.storedlength * 8
        
        self.storedsum = catbytes(self[0x1c:0x1e])

        if (self.version != 6):
            self.pc = catbytes(self[6:8]) # the program counter

        # Initialize opcode dictionaries below
        self.op2_opcodes = {0x1: 'je',
                            0x2: 'jl',
                            0x3: 'jg',
                            0x4: 'dec_chk',
                            0x5: 'inc_chk',
                            0x6: 'jin',
                            0x7: 'test',
                            0x8: 'or',
                            0x9: 'and',
                            0xa: 'test_attr',
                            0xb: 'set_attr',
                            0xc: 'clear_attr',
                            0xd: 'store',
                            0xe: 'insert_obj',
                            0xf: 'loadw',
                            0x10: 'loadb',
                            0x11: 'get_prop',
                            0x12: 'get_prop_addr',
                            0x13: 'get_next_prop',
                            0x14: 'add',
                            0x15: 'sub',
                            0x16: 'mul',
                            0x17: 'div',
                            0x18: 'mod'}
        self.op1_opcodes = {0x0: 'jz',
                            0x1: 'get_sibling',
                            0x2: 'get_child',
                            0x3: 'get_parent',
                            0x4: 'get_prop_len',
                            0x5: 'inc',
                            0x6: 'dec',
                            0x7: 'print_addr',
                            0x9: 'remove_obj',
                            0xa: 'print_obj',
                            0xb: 'ret',
                            0xc: 'jump',
                            0xd: 'print_paddr',
                            0xe: 'load',
                            0xf: 'not'}
        self.op0_opcodes = {0x0: 'rtrue',
                            0x1: 'rfalse',
                            0x2: 'print',
                            0x3: 'print_ret',
                            0x4: 'nop',
                            0x5: 'save',
                            0x6: 'restore',
                            0x7: 'restart',
                            0x8: 'ret_popped',
                            0x9: 'pop',
                            0xa: 'quit',
                            0xb: 'new_line'}
        self.var_opcodes = {0x0: 'call',
                            0x1: 'storew',
                            0x2: 'storeb',
                            0x3: 'put_prop',
                            0x4: 'sread',
                            0x5: 'print_char',
                            0x6: 'print_num',
                            0x7: 'random',
                            0x8: 'push',
                            0x9: 'pull'}
        self.ext_opcodes = {}

        if self.version >= 3:
            self.op0_opcodes.update({0xc: 'show_status',
                                     0xd: 'verify'})
            self.var_opcodes.update({0xa: 'split_window',
                                     0xb: 'set_window',
                                     0x13: 'output_stream',
                                     0x14: 'input_stream',
                                     0x15: 'sound_effect'})
            
        if self.version >= 4:
            self.op2_opcodes.update({0x19: 'call_2s'})
            self.op1_opcodes.update({0x8: 'call_1s'})
            del self.op0_opcodes[0xc]
            del self.var_opcodes[0x15]
            self.var_opcodes.update({0x0: 'call_vs',
                                     0xc: 'call_vs2',
                                     0xd: 'erase_window',
                                     0xe: 'erase_line',
                                     0xf: 'set_cursor',
                                     0x10: 'get_cursor',
                                     0x11: 'set_text_style',
                                     0x12: 'buffer_mode',
                                     0x16: 'read_char',
                                     0x17: 'scan_table'})
            
        if self.version >= 5:
            self.op2_opcodes.update({0x1a: 'call_2n',
                                     0x1b: 'set_colour',
                                     0x1c: 'throw'})
            self.op1_opcodes.update({0xf: 'call_1n'})
            del self.op0_opcodes[0x5]
            del self.op0_opcodes[0x6]
            self.op0_opcodes.update({0x9: 'catch',
                                     0xf: 'piracy'})
            self.var_opcodes.update({0x4: 'aread',
                                     0x15: 'sound_effect',
                                     0x18: 'not',
                                     0x19: 'call_vn',
                                     0x1a: 'call_vn2',
                                     0x1b: 'tokenise',
                                     0x1c: 'encode_text',
                                     0x1d: 'copy_table',
                                     0x1e: 'print_table',
                                     0x1f: 'check_arg_count'})
            self.ext_opcodes.update({0x0: 'save',
                                     0x1: 'restore',
                                     0x2: 'log_shift',
                                     0x3: 'art_shift',
                                     0x4: 'set_font',
                                     0x9: 'save_undo',
                                     0xa: 'restore_undo',
                                     0xb: 'print_unicode',
                                     0xc: 'check_unicode'})
            
        if self.version == 6:
            self.ext_opcodes.update({0x5: 'draw_picture',
                                     0x6: 'picture_data',
                                     0x7: 'erase_picture',
                                     0x8: 'set_margins',
                                     0x10: 'move_window',
                                     0x11: 'window_size',
                                     0x12: 'window_style',
                                     0x13: 'get_wind_prop',
                                     0x14: 'scroll_window',
                                     0x15: 'pop_stack',
                                     ox16: 'read_mouse',
                                     ox17: 'mouse_window',
                                     ox18: 'push_stack',
                                     ox19: 'push_wind_prop',
                                     ox1a: 'print_form',
                                     ox1b: 'make_menu',
                                     ox1c: 'picture_table'})

    def packedtobyte(self, packed):
        if self.version < 4:
            return(2 * packed)
        elif self.version < 6:
            return(4 * packed)

    def verify(self):
        if self.storedlength > len(self):
            raise ZCodeError('Z-code file contains invalid length data.')
        i = 0x40
        workingsum = 0
        while i < self.storedlength:
            workingsum = (workingsum + self[i]) % 0x10000
            i = i + 1
        return(workingsum == self.storedsum)

    def getopcode(self):
        opcode = self[self.pc]
        if (opcode & 0b11000000) == 0b11000000: # variable form
            if (opcode & 0b00100000) == 0b00000000:
                return(self.op2_opcodes[opcode & 0b00011111])
            else:
                return(self.var_opcodes[opcode & 0b00011111])
        elif (opcode & 0b11000000) == 0b10000000: #short form
            if (opcode & 0b00110000) == 0b00110000:
                return(self.op0_opcodes[opcode & 0b00001111])
            else:
                return(self.op1_opcodes[opcode & 0b00001111])
        elif opcode == 0xbe: # extended form
            return(self.ext_opcodes[self[self.pc + 1]])
        else: # long form
            return(self.op2_opcodes[opcode & 0b00011111])

def catbytes(bytes):
    result = 0
    for rawbyte in bytes:
        result = (result * 0x100) + rawbyte
    return(result)
