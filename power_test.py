from drivers.ad7490 import AD7490 
from drivers.ds18b20 import probe_devices, DS18B20
from drivers.ltc2620 import LTC2620
import time

ADC_CS = 1
DAC_CS = 0
SPI_BUS = 0
ADC_CHANNELS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] # Disable channels by removing from this list
INTERVAL = 0 # Sleep interval

filename = input("Enter data log file name: ")

dac = LTC2620(SPI_BUS, DAC_CS)
adc = AD7490(SPI_BUS, ADC_CS)

temp_sensors = [DS18B20(temp_dir) for temp_dir in probe_devices()]

dac.write_channel_raw(15, 0) # Start with all channels at zero

st_time = time.perf_counter()

print("ADC Channels Active: " + str(ADC_CHANNELS))
print(str(len(temp_sensors)) + " Temp sensors active")

step = 0
step_increment = (int)(0.25 * 4096 / 5) # 0.25W step increment
max_step = (int)(3.25 * 4096 / 5) # max 3.25V = 1W
step_time = 10
last_step = time.perf_counter()

static = (int)(1 * 4096 / 5) # 1V = 255mW
T_pulse_on = 10
T_pulse_off = 20
pulse = 0
last_pulse = time.perf_counter()

while True:
    if (pulse and time.perf_counter() - last_pulse > T_pulse_off):
        dac.write_channel_raw(4, 0) # pulse off
        pulse = 0
        last_pulse = time.perf_counter()
        print("Pulsing Thruster 1 off")
    elif ((not pulse) and time.perf_counter() - last_pulse > T_pulse_on):
        dac.write_channel_raw(4, static) # pulse on
        pulse = 1
        last_pulse = time.perf_counter()
        print("Pulsing Thruster 1 on")
    dac.write_channel_raw(5, static) # static thruster

    if (time.perf_counter() - last_step > step_time):
        step += step_increment
        if (step > max_step):
            step = 0
        last_step = time.perf_counter()
        print("Step set voltage: " + str(step))
    dac.write_channel_raw(6, step)

    adc_readings = [adc.read_channel_raw(i) for i in ADC_CHANNELS]
    temp_readings = [ts.read_temp() for ts in temp_sensors]
    t = time.perf_counter() - st_time 

    f = open(filename, "a")
    f.write(",".join([str(t)] + [str(i) for i in adc_readings] + [str(i) for i in temp_readings] + [str(static * pulse), str(static), str(step)]) + "\n")
    f.close()

    print("Time: " + str(t) +  " ADC Raw: " + str(adc_readings))
    print("Temps: " + str(temp_readings))

    time.sleep(INTERVAL)