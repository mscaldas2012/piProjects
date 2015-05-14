import time

import smbus


# Gyro Register Defines

class L3G4200D:
    WHO_AM_I = 0x0F
    CTRL_1 = 0x20
    CTRL_2 = 0x21
    CTRL_3 = 0x22
    CTRL_4 = 0x23
    CTRL_5 = 0x24
    Reference = 0x25
    TEMP = 0x26

    StatusRegister = 0x27

    GYRO_X_DATA_LSB = 0x28
    GYRO_X_DATA_MSB = 0x29
    GYRO_Y_DATA_LSB = 0x28
    GYRO_Y_DTATA_MSB = 0x29
    GYRO_Z_DATA_LSB = 0x28
    GYRO_Z_DATA_MSB = 0x29

    FIFOControl = 0x2E
    FIFOSource = 0x2F

    InterruptControl = 0x30
    InterruptSource = 0x31

    InterruptThresholdXMSB = 0x32
    InterruptThresholdXLSB = 0x33
    InterruptThresholdYMSB = 0x34
    InterruptThresholdYLSB = 0x35
    InterruptThresholdZMSB = 0x36
    InterruptThresholdZLSB = 0x37
    InterruptDuration = 0x38


    # DLPF, Full Scale Setting
    FullScale_2000_sec = 0x18  # must be set at reset
    DLPF_256_8 = 0x00  # Consult datasheet for explanation
    DLPF_188_1 = 0x01
    DLPF_98_1 = 0x02
    DLPF_42_1 = 0x03
    DLPF_20_1 = 0x04
    DLPF_10_1 = 0x05
    DLPF_5_1 = 0x06


def __init__(self, addr):
    self.address = addr
    self.bus = smbus.SMBus(1)
    self.bus.write_byte_data(addr, self.CTRL_1, 0x1F)
    self.bus.write_byte_data(addr, self.CTRL_2, 0x08)
    self.bus.write_byte_data(addr, self.CTRL_4, 0x80)
    time.sleep(100)


def getAxes(self):
    gyro_x = readAxis(self.GYRO_X_DATA_MSB, self.GYRO_X_DATA_LSB)
    gyro_y = readAxis(self.GYRO_Y_DATA_MSB, self.GYRO_Y_DATA_LSB)
    gyro_z = readAxis(self.GYRO_Z_DATA_MSB, self.GYRO_Z_DATA_LSB)
    return (gyro_x, gyro_y, gyro_z)


def readAxis(self, _msb, _lsb):
    msb = self.bus.read_byte_data(self.address, _msb)
    lsb = self.bus.read_byte_data(self.address, _lsb)
    return ((msb << 8) | lsb)

