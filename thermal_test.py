from drivers.ad7490 import AD7490 
from drivers.ds18b20 import probe_devices, DS18B20
from drivers.ltc2620 import LTC2620
import time

ADC_CS = 1
DAC_CS = 0
SPI_BUS = 0
ADC_CHANNELS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] # Disable channels by removing from this list
INTERVAL = 1 # Sleep interval

filename = input("Enter data log file name: ")

dac = LTC2620(SPI_BUS, DAC_CS)
adc = AD7490(SPI_BUS, ADC_CS)

temp_sensors = [DS18B20(temp_dir) for temp_dir in probe_devices()]

dac.channel_off(15) # Turn off all channels for test

st_time = time.perf_counter()

print("ADC Channels Active: " + str(ADC_CHANNELS))
print(str(len(temp_sensors)) + " Temp sensors active")

while True:
    adc_readings = [adc.read_channel_raw(i) for i in ADC_CHANNELS]
    temp_readings = [ts.read_temp() for ts in temp_sensors]
    t = time.perf_counter() - st_time 

    f = open(filename, "w")
    f.write(",".join([str(t)] + [str(i) for i in adc_readings] + [str(i) for i in temp_readings]) + "\n")
    f.close()

    print("Time: " + str(t) +  " ADC Raw: " + str(adc_readings))
    print("Temps: " + str(temp_readings))

    time.sleep(INTERVAL)