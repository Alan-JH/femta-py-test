import spidev

class LTC2620():
    MAX_SPEED = 400000
    SPI_MODE = 0

    def __init__(self, bus, device):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = self.MAX_SPEED
        self.spi.mode = self.SPI_MODE

    def write_channel_raw(self, channel, value):
        """
        Writes raw bit value to adc channel
        :param channel: (int) channel number, 0-7, or 15 to set all channels
        :param value: (int) raw 12 bit value, 0-4095
        :return: spi.writebytes raw result
        """
        byte1 = (0b0011 << 4) | channel
        byte2 = value >> 4
        byte3 = (value << 4) | 0xff
        return self.spi.writebytes([byte1, byte2, byte3])

    def channel_off(self, channel):
        """
        Turns adc channel off
        :param channel: (int) channel number, 0-7, or 15 to turn off all channels
        :return: spi.writebytes raw result
        """
        byte1 = (0b0100 << 4) | channel
        return self.spi.writebytes([byte1, 0, 0])