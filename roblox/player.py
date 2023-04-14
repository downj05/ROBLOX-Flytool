import math
from numpy import zeros as zeros
from pymem import Pymem
import pymem.process
import logging
"""Pointers, need to read from config file/user input."""
humanoidRootPartPointer = [0x03D16174,0x4,0x5C,0x8,0x18,0xE4, 0x30]
"""
Attack pymem to Roblox, get its base address
for memory reading and writing.
"""

programName = "RobloxPlayerBeta.exe"
program = Pymem(process_name=programName)
programBaseAddress = pymem.process.module_from_name(program.process_handle, programName).lpBaseOfDll


class Vector3:
    def __init__(self, start_address):
        self.base = start_address

    @property
    def x(self):
        return program.read_float(self.base + 0x0) # No offset
    @x.setter
    def x(self, value):
        program.write_float(self.base+0x0,value) # No offset

    @property
    def y(self):
        return program.read_float(self.base + 0x4) # Y has offset 4
    @y.setter
    def y(self, value):
        program.write_float(self.base+0x4,value) # Y has offset 4

    @property
    def z(self):
        return program.read_float(self.base + 0x8) # Z has offset 8
    @z.setter
    def z(self, value):
        program.write_float(self.base+0x8,value) # Z has offset 8

    def pretty_print(self, round=3):
        return f"X: {str(self.x)[:6]} Y: {str(self.y)[:6]} Z: {str(self.z)[:6]}"
    
class Float:
    def __init__(self, start_address):
        self.base = start_address

    @property
    def value(self):
        return program.read_float(self.base)

    @value.setter
    def value(self, value):
        program.write_float(self.base, value)


"""
Matrix to Euler function, returns yaw, pitch, and roll from a supplied rotational matrix/CFrame.
"""
def mat2eul(matrix, degrees=True):

    if matrix[0][1] > 0.998:
        heading = math.atan2(matrix[2][0], matrix[2][2])
        attitude = math.pi / 2
        bank = 0
    elif matrix[0][1] > -0.998:
        heading = math.atan2(matrix[2][0], matrix[2][2])
        attitude = -math.pi / 2
        bank = 0
    else:
        heading = math.atan2(-matrix[0][2], matrix[0][0])
        attitude = math.asin(matrix[0][1])
        bank = math.atan2(-matrix[2][1], matrix[1][1])

    if degrees: # Convert from radians
        return -heading*180/math.pi, -attitude*180/math.pi, -bank*180/math.pi
    else:
        return -heading, -attitude, -bank

class CFrame:
    def __init__(self, start_address):
        self.base = start_address
        self._matrix = [[0,0,0],
                        [0,0,0],
                        [0,0,0]]

    @property
    def matrix(self):
        m = zeros(9)
        for i,f in enumerate(range(9)): # 3x3 matrix = 9
            # Read all values, create a flattened matrix, reshape to 3x3
            m[i] = round(program.read_float(self.base+(0x4*f)), 4) # Round to 4 for decent precision
        return m.reshape(3,3)

    @property
    def angles(self):
        return mat2eul(self.matrix)




class Player:
    """
    Player Class
    """
    def __init__(self, rootPartBaseAddress=0x00000000):
        self.HumanoidRootPart = self.HumanoidRootPart(baseAddress=rootPartBaseAddress)
    def update(self):
        """
        Updates the values of every sub-class of the player.
        Currently we only have the humanoid root part.
        """
        self.HumanoidRootPart.update()

    class HumanoidRootPart:
        """
        Humanoid Root Part class, the part of a player that controls
        the players location, velocity, orientation and gravity.
        Has a base address for memory read and write, we also have
        a dictionary containing the offsets for each of the variables.
        """
        def __init__(self, baseAddress=0x00000000):
            """
            We obtain the addresses by calling our getBaseAddress() method,
            we call this function upon initiating our root part.
            We can read our values each time we call our update() method.
            """

            self.baseAddress = baseAddress
            # If base address is not set, dereference preconfigured static pointer
            if self.baseAddress == 0:
                self.baseAddress = self.getBaseAddress()
            else:
                logging.debug(f'Using provided base address {hex(baseAddress)}')

            self.gravity = Float(self.baseAddress+0xA0)

            self.cframe = CFrame(self.baseAddress+0xA8)

            self.position = Vector3(self.baseAddress+0xCC)

            self.velocity = Vector3(self.baseAddress+0xD8)

        def getBaseAddress(self):
            """
            Dereferences the multi-level pointer for the humanoid root part.
            Starts by adding Roblox's base address with the pointers base address,
            then referencing the address, adding the newewly found address with the
            next offset and so on until reaching the Humanoid Root Part's base address.
            """

            # Get base address of programme
            address = program.read_int(programBaseAddress+humanoidRootPartPointer[0])

            logging.debug(f'"{programName}" + {hex(humanoidRootPartPointer[0]).upper()} -> {hex(address).upper()}')
            # Iterate over offsets, excluding pointer base address and the final offset
            for offset in humanoidRootPartPointer[1:-1]:
                logging.debug(f'[{hex(address).upper()} + {hex(offset).upper()}] -> {hex(program.read_int(address+offset)).upper()}')
                address = program.read_int(address+offset)

            # We add the final offset on instead of dereferencing it
            logging.debug(f'{hex(address).upper()} + {hex(humanoidRootPartPointer[-1]).upper()} = {hex(address+humanoidRootPartPointer[-1]).upper()}')
            self.baseAddress = address+humanoidRootPartPointer[-1]
            return self.baseAddress




        # def getRotation(self):
        #     """
        #     Retrieves the humanoid root parts CFrame, runs a matrix to euler function and returns the first
        #     component.
        #     """
        #     matrix = self.CFrame
        #     yaw,pitch,roll = mat2eul(matrix=matrix)
        #     return yaw,pitch,roll
