import serial

class Printer:
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

    def home(self):
        self.serial.write(b'G28 XYZ \r\n')
        self.serial.write(f'G1 Z{self.zHeight}'.encode())
        self.serial.write(b'G1 X131 Y81\r\n')
        self.serial.write(b'G91\r\n')







