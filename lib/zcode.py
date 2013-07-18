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
        # Take an open file as input and read its contents into the array.

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
            self.pc = catbytes(self[6:8])

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

def catbytes(bytes):
    result = 0
    for rawbyte in bytes:
        result = (result * 0x100) + rawbyte
    return(result)
