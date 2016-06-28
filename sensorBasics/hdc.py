import smbus
import time

class HDC: 

	#Registers
	REG_TEMP =   0
	REG_HUMID =  1
	REG_CONFIG = 2

	I2C_BUS = 1 #1 for PI or 2 for PCDuino, 

	#Configuration bits
	CFG_RST = 1<<15
	CFG_MODE_SINGLE = 0 << 12
	CFG_MODE_BOTH = 1 << 12

        #As determined by sudo i2cdetect -y 1
	ADDRESS = 0x40

	def __init__(self, bus_num=I2C_BUS):
		 self.bus=smbus.SMBus(bus_num)

        def readRaw(self,reg):
		#configure the HDC1008 for one reading
		config = 0
		config |= self.CFG_MODE_SINGLE
		self.bus.write_byte_data(self.ADDRESS, self.REG_CONFIG, config)

		#tell the thing to take a reading
		self.bus.write_byte(self.ADDRESS, reg)
		time.sleep(0.015)

		#get the reading back from the thing
		raw = self.bus.read_byte(self.ADDRESS)
		raw = (raw<<8) + self.bus.read_byte(self.ADDRESS)
		return raw

	def readTemperature(self):
                #Get Raw Temp
                raw = self.readRaw(self.REG_TEMP)

		#use TI's formula to turn it into people numbers
		tempC = (raw/65536.0)* 165  - 40

		#convert temp to farenheid
		tempF = tempC * (9.0/5.0) + 32
		return tempC, tempF
	
	def readHum(self):
		#Get Raw Humid
                raw = self.readRaw(self.REG_HUMID)
		
		hum = (raw/(2.0**16))*100
		return hum


"""Running in STAND ALONE mode."""
if __name__ == "__main__":
		
        HDC1008=HDC()

        print (HDC1008.readTemperature())
        print (HDC1008.readHum())
