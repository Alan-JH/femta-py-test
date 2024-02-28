import os
import glob
import time

BASE_DIR = '/sys/bus/w1/devices/'

def probe_devices():
    """
    Probes and returns a list of file directories to read from to read temp sensors
    :return: (list) string directories with one wire slave devices
    """
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    return glob.glob(BASE_DIR + '28*')

class DS18B20():
    def __init__(self, device_folder):
        # Device folder: file directory as returned by probe_devices for the given temp sensor
        self.device_file = device_folder + '/w1_slave'

    def read_temp_raw(self):
        """
        Reads and returns raw temperature readout
        :return: (list) lines read from file
        """
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        """
        Reads and returns temperature in degrees C
        :return: (double) temp, C (-999 if error)
        """
        lines = self.read_temp_raw()
        #while lines[0].strip()[-3:] != 'YES': # Original implementation retries indefinitely until valid reading
        #    time.sleep(0.2)
        #    lines = self.read_temp_raw(self)
        if lines[0].strip()[-3:] != 'YES':
            return -999 # This implementation will only try once, in the interest of having a consistent readout time
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c
        return -999