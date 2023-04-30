import time

import serial

class Printer:
    #XABS
    #YABS
    #x_mm_offset
    #y_mm_offset


    def __init__(self, comport, baudrate, z_height):
        self.zHeight = z_height
        self.comport = comport
        self.baudrate = baudrate
        self.serial = serial.Serial(
            port=self.comport,
            baudrate=self.baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        time.sleep(1)


    def home(self):
        self.serial.write((b'M503\r\n'))
        self.serial.write(b'M204 T20000\r\n')
        self.serial.write(b'G28 XYZ \r\n')
        self.serial.write(f'G1 Z{self.zHeight}'.encode())
        #self.serial.write(b'G1 X131 Y81\r\n')
        self.serial.write(b'G91\r\n')

    #def goToPoint(self):
    #    XBoundCenter = XABS + x_mm_offset
    #    YBoundCenter = YABS + y_mm_offset
    #    x_mm_offset_str = str(x_mm_offset)  # convert to String
    #    x_mm_offset_b = x_mm_offset_str.encode('UTF-8')
    #    y_mm_offset_str = str(y_mm_offset)  # convert to String
    #    y_mm_offset_b = y_mm_offset_str.encode('UTF-8')
    #    self.serial.write(b'G1X')
    #    self.serial.write(x_mm_offset_b)
    #    print(x_mm_offset_b)
    #    self.serial.write(b'Y')
    #    self.serial.write(y_mm_offset_b)
    #    print(y_mm_offset_b)
    #    self.serial.write(b'\r\n')







