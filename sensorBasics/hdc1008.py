#!/usr/bin/python
import time
import smbus


bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

HDC1008_ADDR = 0x40

#Set configuration with two bytes written to 0x02
myBytes = [0x10, 0x00]
bus.write_i2c_block_data(HDC1008_ADDR,0x02,myBytes)
#time.sleep(0.0635)

#Set Pointer to 0x00 and sleep
bus.write_byte(HDC1008_ADDR,0x00)    
time.sleep(0.20)

#Read temp as two bytes from 0x00
data = bus.read_byte_data(HDC1008_ADDR,2)
print(data)
