import os
import glob
import time

class TempProbe():

    def __init__(self):

        self.baseDir = "/sys/bus/w1/devices/"
        self.deviceDir = glob.glob(self.baseDir + "28*")[0]
        self.deviceFile = self.deviceDir + "/w1_slave"

    def readTempRaw(self):

        #Open the file, read the contents and close.
        inFile = open(self.deviceFile,"r")
        lines = inFile.readlines()
        inFile.close()

        return lines
        
    def readTemp(self):

        #Read an initial temperature from the device file
        lines = self.readTempRaw()

        #If the file does not say Yes then wait 0.2 secs and try again
        while (lines[0].strip()[-3:]).lower() != 'yes':
            time.sleep(0.2)
            lines = self.readTempRaw()

        #Look for the position of the = in the 2nd line
        equalPos = lines[1].find('t=')

        #If the t= was found
        if equalPos != -1:
            tempString = lines[1][equalPos+2:]
            tempC = float(tempString) / 1000.0
            tempF = tempC * 9.0 / 5.0 + 32.0
            return tempC, tempF
            


if __name__ == '__main__':

  try:
    lcd = TempProbe()
    while True:
        tC, tF = lcd.readTemp()
        print (tC, tF)
        time.sleep(1)
  except KeyboardInterrupt:
    pass
  finally:
    print ("Exit!")
    
