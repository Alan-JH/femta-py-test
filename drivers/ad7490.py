import spidev

class AD7490():
    MAX_SPEED = 400000
    SPI_MODE = 0

    # ADC Settings
    POWER_MODE = 3
    DOUT = 0
    RANGE_REF = 0
    CODING = 1
    SEQ = 0
    WRITE = 1
    SHADOW = 0

    # ADC VREF
    VREF = 2.5

    def __init__(self, bus, device):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = self.MAX_SPEED
        self.spi.mode = self.SPI_MODE
        # Init ADC after power up by sending ones for two cycles
        self.spi.writebytes([0xff, 0xff])
        self.spi.writebytes([0xff, 0xff])

    def read_channel_raw(self, channel):
        """
        Reads raw bit value from adc channel
        :param channel: (int) channel number, 0-15
        :return: (int) 12 bit value, 0-4095
        """
        byte1 = 0x00 | (self.WRITE << 7) | (self.SEQ << 6) | channel << 2 | (self.POWER_MODE)
        byte2 = 0x00 | (self.SHADOW << 7) | (self.DOUT << 6) | (self.RANGE_REF << 5) | (self.CODING << 4)

        self.spi.writebytes([byte1, byte2])
        ret = self.spi.readbytes(2)
        return  ((ret[0] << 8) | (ret[1])) & 0xfff

    def read_channel_voltage(self, channel):
        """
        Reads bit value from adc channel and converts to volts
        :param channel: (int) channel number, 0-15
        :return: (double) voltage value
        """
        return self.read_channel_raw(channel) * 2 * self.VREF / 4096