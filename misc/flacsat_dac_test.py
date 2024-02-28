import spidev
bus = 0
device = 0

spi = spidev.SpiDev()
spi.open(bus, device)
spi.max_speed_hz = 400000
spi.mode = 0

def write_channel(channel, value):
	# channel: 0-7, or 15 to apply to all channels
	# value: 0-4095 value
	byte1 = (0b0011 << 4) | channel
	byte2 = value >> 4
	byte3 = (value << 4) | 0xff
	spi.writebytes([byte1, byte2, byte3])

def channel_off(channel):
	# channel: 0-7, or 15 to apply to all channels
	byte1 = (0b0100 << 4) | channel
	byte2 = 0
	byte3 = 0
	spi.writebytes([byte1, byte2, byte3])
