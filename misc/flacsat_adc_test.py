import spidev, time

bus = 0
device = 1

spi = spidev.SpiDev()
spi.open(bus, device)
spi.max_speed_hz = 400000
spi.mode = 0

power_mode = 3
dout = 0
range_ref = 0
coding = 1
seq = 0
write = 1
shadow = 0

# Init ADC after power up by sending ones for two cycles
spi.writebytes([0xff, 0xff])
spi.writebytes([0xff, 0xff])

while 1:
	for channel in range(0, 16):
		byte1 = 0x00 | (write << 7) | (seq << 6) | channel << 2 | (power_mode)
		byte2 = 0x00 | (shadow << 7) | (dout << 6) | (range_ref << 5) | (coding << 4)

		spi.writebytes([byte1, byte2])
		ret = spi.readbytes(2)
		output = ((ret[0] << 8) | (ret[1])) & 0xfff
		output *= 5/4096
		print(f"Channel {channel}: {output}")

	time.sleep(0.5)
