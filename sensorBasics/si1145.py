#!/usr/bin/python

import smbus
import time

class SI1145():

  """I2C Bus: Set as 1 for PI or 2 for PCDuino"""
  I2C_BUS = 1

  """COMMANDS"""
  SI1145_PARAM_QUERY = 0x80
  SI1145_PARAM_SET = 0xA0
  SI1145_NOP = 0x0
  SI1145_RESET    = 0x01
  SI1145_BUSADDR    = 0x02
  SI1145_PS_FORCE    = 0x05
  SI1145_ALS_FORCE    = 0x06
  SI1145_PSALS_FORCE    = 0x07
  SI1145_PS_PAUSE = 0x09
  SI1145_ALS_PAUSE    = 0x0A
  SI1145_PSALS_PAUSE    = 0xB
  SI1145_PS_AUTO    = 0x0D
  SI1145_ALS_AUTO   = 0x0E
  SI1145_PSALS_AUTO = 0x0F
  SI1145_GET_CAL    = 0x12

  """Parameters"""
  SI1145_PARAM_I2CADDR = 0x00
  SI1145_PARAM_CHLIST   = 0x01
  SI1145_PARAM_CHLIST_ENUV = 0x80
  SI1145_PARAM_CHLIST_ENAUX = 0x40
  SI1145_PARAM_CHLIST_ENALSIR = 0x20
  SI1145_PARAM_CHLIST_ENALSVIS = 0x10
  SI1145_PARAM_CHLIST_ENPS1 = 0x01
  SI1145_PARAM_CHLIST_ENPS2 = 0x02
  SI1145_PARAM_CHLIST_ENPS3 = 0x04

  SI1145_PARAM_PSLED12SEL   = 0x02
  SI1145_PARAM_PSLED12SEL_PS2NONE = 0x00
  SI1145_PARAM_PSLED12SEL_PS2LED1 = 0x10
  SI1145_PARAM_PSLED12SEL_PS2LED2 = 0x20
  SI1145_PARAM_PSLED12SEL_PS2LED3 = 0x40
  SI1145_PARAM_PSLED12SEL_PS1NONE = 0x00
  SI1145_PARAM_PSLED12SEL_PS1LED1 = 0x01
  SI1145_PARAM_PSLED12SEL_PS1LED2 = 0x02
  SI1145_PARAM_PSLED12SEL_PS1LED3 = 0x04

  SI1145_PARAM_PSLED3SEL   = 0x03
  SI1145_PARAM_PSENCODE   = 0x05
  SI1145_PARAM_ALSENCODE  = 0x06

  SI1145_PARAM_PS1ADCMUX   = 0x07
  SI1145_PARAM_PS2ADCMUX   = 0x08
  SI1145_PARAM_PS3ADCMUX   = 0x09
  SI1145_PARAM_PSADCOUNTER   = 0x0A
  SI1145_PARAM_PSADCGAIN = 0x0B
  SI1145_PARAM_PSADCMISC = 0x0C
  SI1145_PARAM_PSADCMISC_RANGE = 0x20
  SI1145_PARAM_PSADCMISC_PSMODE = 0x04

  SI1145_PARAM_ALSIRADCMUX   = 0x0E
  SI1145_PARAM_AUXADCMUX   = 0x0F

  SI1145_PARAM_ALSVISADCOUNTER   = 0x10
  SI1145_PARAM_ALSVISADCGAIN = 0x11
  SI1145_PARAM_ALSVISADCMISC = 0x12
  SI1145_PARAM_ALSVISADCMISC_VISRANGE = 0x20

  SI1145_PARAM_ALSIRADCOUNTER   = 0x1D
  SI1145_PARAM_ALSIRADCGAIN = 0x1E
  SI1145_PARAM_ALSIRADCMISC = 0x1F
  SI1145_PARAM_ALSIRADCMISC_RANGE = 0x20

  SI1145_PARAM_ADCCOUNTER_511CLK = 0x70

  SI1145_PARAM_ADCMUX_SMALLIR  = 0x00
  SI1145_PARAM_ADCMUX_LARGEIR  = 0x03

  """REGISTERS"""
  SI1145_REG_PARTID  = 0x00
  SI1145_REG_REVID  = 0x01
  SI1145_REG_SEQID  = 0x02

  SI1145_REG_INTCFG  = 0x03
  SI1145_REG_INTCFG_INTOE = 0x01
  SI1145_REG_INTCFG_INTMODE = 0x02

  SI1145_REG_IRQEN  = 0x04
  SI1145_REG_IRQEN_ALSEVERYSAMPLE = 0x01
  SI1145_REG_IRQEN_PS1EVERYSAMPLE = 0x04
  SI1145_REG_IRQEN_PS2EVERYSAMPLE = 0x08
  SI1145_REG_IRQEN_PS3EVERYSAMPLE = 0x10

  SI1145_REG_IRQMODE1 = 0x05
  SI1145_REG_IRQMODE2 = 0x06

  SI1145_REG_HWKEY  = 0x07
  SI1145_REG_MEASRATE0 = 0x08
  SI1145_REG_MEASRATE1  = 0x09
  SI1145_REG_PSRATE  = 0x0A
  SI1145_REG_PSLED21  = 0x0F
  SI1145_REG_PSLED3  = 0x10
  SI1145_REG_UCOEFF0  = 0x13
  SI1145_REG_UCOEFF1  = 0x14
  SI1145_REG_UCOEFF2  = 0x15
  SI1145_REG_UCOEFF3  = 0x16
  SI1145_REG_PARAMWR  = 0x17
  SI1145_REG_COMMAND  = 0x18
  SI1145_REG_RESPONSE  = 0x20
  SI1145_REG_IRQSTAT  = 0x21
  SI1145_REG_IRQSTAT_ALS  = 0x01

  SI1145_REG_ALSVISDATA0 = 0x22
  SI1145_REG_ALSVISDATA1 = 0x23
  SI1145_REG_ALSIRDATA0 = 0x24
  SI1145_REG_ALSIRDATA1 = 0x25
  SI1145_REG_PS1DATA0 = 0x26
  SI1145_REG_PS1DATA1 = 0x27
  SI1145_REG_PS2DATA0 = 0x28
  SI1145_REG_PS2DATA1 = 0x29
  SI1145_REG_PS3DATA0 = 0x2A
  SI1145_REG_PS3DATA1 = 0x2B
  SI1145_REG_UVINDEX0 = 0x2C
  SI1145_REG_UVINDEX1 = 0x2D
  SI1145_REG_PARAMRD = 0x2E
  SI1145_REG_CHIPSTAT = 0x30

  #As determined by sudo i2cdetect -y 1
  SI1145_ADDR = 0x60

  #Configuration bits
  CFG_RST = 1<<15
  CFG_MODE_SINGLE = 0 << 12
  CFG_MODE_BOTH = 1 << 12
  REG_CONFIG = 2
        
  """PORTED METHOD - Initialisation Method."""
  def __init__(self, bus_num=I2C_BUS):
    self.bus=smbus.SMBus(bus_num)

    #uint8_t id = read8(SI1145_REG_PARTID);
    #if (id != 0x45) return false; // look for SI1145

    self.reset()

    ## Enable UVindex measurement coefficients!
    #write8(SI1145_REG_UCOEFF0, 0x29);
    self.bus.write_byte_data(self.SI1145_ADDR, self.SI1145_REG_UCOEFF0, 0x29)
    #write8(SI1145_REG_UCOEFF1, 0x89);
    self.bus.write_byte_data(self.SI1145_ADDR, self.SI1145_REG_UCOEFF1, 0x89)
    #write8(SI1145_REG_UCOEFF2, 0x02);
    self.bus.write_byte_data(self.SI1145_ADDR, self.SI1145_REG_UCOEFF2, 0x02)
    #write8(SI1145_REG_UCOEFF3, 0x00);
    self.bus.write_byte_data(self.SI1145_ADDR, self.SI1145_REG_UCOEFF3, 0x00)

    # Enable UV sensor
    #writeParam(SI1145_PARAM_CHLIST, SI1145_PARAM_CHLIST_ENUV |
    #SI1145_PARAM_CHLIST_ENALSIR | SI1145_PARAM_CHLIST_ENALSVIS |
    #SI1145_PARAM_CHLIST_ENPS1);
    self.writeParam(self.SI1145_PARAM_CHLIST,self.SI1145_PARAM_CHLIST_ENUV | self.SI1145_PARAM_CHLIST_ENALSIR | self.SI1145_PARAM_CHLIST_ENALSVIS | self.SI1145_PARAM_CHLIST_ENPS1 )

    ## Enable interrupt on every sample
    #write8(SI1145_REG_INTCFG, SI1145_REG_INTCFG_INTOE);
    self.bus.write_byte_data(self.SI1145_ADDR, self.SI1145_REG_INTCFG, self.SI1145_REG_INTCFG_INTOE)
    #write8(SI1145_REG_IRQEN, SI1145_REG_IRQEN_ALSEVERYSAMPLE);  
    self.bus.write_byte_data(self.SI1145_ADDR, self.SI1145_REG_IRQEN, self.SI1145_REG_IRQEN_ALSEVERYSAMPLE)

    # Measurement rate for auto
    #write8(SI1145_REG_MEASRATE0, 0xFF); // 255 * 31.25uS = 8ms
    self.bus.write_byte_data(self.SI1145_ADDR, self.SI1145_REG_MEASRATE0, 0xFF)

    #auto run
    #write8(SI1145_REG_COMMAND, SI1145_PSALS_AUTO);
    self.bus.write_byte_data(self.SI1145_ADDR, self.SI1145_REG_COMMAND, self.SI1145_PSALS_AUTO)


  """PORTED METHOD - uint8_t Adafruit_SI1145::writeParam(uint8_t p, uint8_t v) {"""
  def writeParam(self,p,v):

    ## Don't think I need to print these statements
    #Serial.print("Param 0x"); Serial.print(p, HEX);
    #print("Param 0x",p,"HEX")
    #Serial.print(" = 0x"); Serial.println(v, HEX);
    #print("= 0x",v,"HEX")

    #write8(SI1145_REG_PARAMWR, v);
    self.bus.write_byte_data(self.SI1145_ADDR, self.SI1145_REG_PARAMWR, v)

    #write8(SI1145_REG_COMMAND, p | SI1145_PARAM_SET);
    self.bus.write_byte_data(self.SI1145_ADDR, self.SI1145_REG_COMMAND, p | self.SI1145_PARAM_SET)

    #return read8(SI1145_REG_PARAMRD);
    return self.bus.read_byte_data(self.SI1145_ADDR, self.SI1145_REG_PARAMRD)


  """PORTED METHOD - uint8_t Adafruit_SI1145::readParam(uint8_t p) {"""
  def readParam(p):
    #write8(SI1145_REG_COMMAND, p | SI1145_PARAM_QUERY);
    self.bus.write_byte_data(self.SI1145_ADDR, self.SI1145_REG_COMMAND, p | self.SI1145_PARAM_QUERY)

    #return read8(SI1145_REG_PARAMRD);
    return self.bus.read_byte_data(self.SI1145_ADDR, self.SI1145_REG_PARAMRD)



  """PORTED METHOD - Read method used to read 16 bits"""
  """uint16_t Adafruit_SI1145::read16(uint8_t a) {"""
  def read16(self,reg):
    #Wire.beginTransmission(_addr); // start transmission to device
    #Wire.write(a); // sends register address to read from
    #Wire.endTransmission(); // end transmission
    self.bus.write_byte(self.SI1145_ADDR, reg)
    time.sleep(0.015)

    #Wire.requestFrom(_addr, (uint8_t)2);// send data n-bytes read
    #ret = Wire.read(); // receive DATA
    lsb = self.bus.read_byte_data(self.SI1145_ADDR,reg)

    #ret |= (uint16_t)Wire.read() << 8; // receive DATA
    #ret |= self.bus.read_byte(self.SI1145_ADDR) << 8
    msb = self.bus.read_byte(self.SI1145_ADDR)

    print(lsb,msb)                
    return ( msb << 8 ) + lsb

  """void Adafruit_SI1145::reset() {"""
  def reset(self):
    #write8(SI1145_REG_MEASRATE0, 0);
    self.bus.write_byte_data(self.SI1145_ADDR, self.SI1145_REG_MEASRATE0, 0)
    #write8(SI1145_REG_MEASRATE1, 0);
    self.bus.write_byte_data(self.SI1145_ADDR, self.SI1145_REG_MEASRATE1, 0)
    #write8(SI1145_REG_IRQEN, 0);
    self.bus.write_byte_data(self.SI1145_ADDR, self.SI1145_REG_IRQEN, 0)
    #write8(SI1145_REG_IRQMODE1, 0);
    self.bus.write_byte_data(self.SI1145_ADDR, self.SI1145_REG_IRQMODE1, 0)
    #write8(SI1145_REG_IRQMODE2, 0);
    self.bus.write_byte_data(self.SI1145_ADDR, self.SI1145_REG_IRQMODE2, 0)
    #write8(SI1145_REG_INTCFG, 0);
    self.bus.write_byte_data(self.SI1145_ADDR, self.SI1145_REG_INTCFG, 0)
    #write8(SI1145_REG_IRQSTAT, 0xFF);
    self.bus.write_byte_data(self.SI1145_ADDR, self.SI1145_REG_IRQSTAT, 0xFF)
    #write8(SI1145_REG_COMMAND, SI1145_RESET);
    self.bus.write_byte_data(self.SI1145_ADDR, self.SI1145_REG_COMMAND, self.SI1145_RESET)
    #delay(10);
    time.sleep(0.10)
    #write8(SI1145_REG_HWKEY, 0x17);
    self.bus.write_byte_data(self.SI1145_ADDR, self.SI1145_REG_HWKEY, 0x17)
    #delay(10);
    time.sleep(0.10)

  """returns visible+IR light levels"""
  """uint16_t Adafruit_SI1145::readVisible(void) {"""
  def readVisible(self):
    #return read16(0x22);
    #raw = self.read16(0x22)
    lsb = self.bus.read_byte_data(self.SI1145_ADDR,self.SI1145_REG_ALSVISDATA0)
    msb = self.bus.read_byte_data(self.SI1145_ADDR,self.SI1145_REG_ALSVISDATA1)
    raw = ( msb << 8 ) + lsb
    print("Vis: %d [%d,%d]" %(raw,msb,lsb))
    return raw


  """returns IR light levels"""
  """uint16_t Adafruit_SI1145::readIR(void) {"""
  def readIR(self):
    #return read16(0x24);
    lsb = self.bus.read_byte_data(self.SI1145_ADDR,self.SI1145_REG_ALSIRDATA0)
    msb = self.bus.read_byte_data(self.SI1145_ADDR,self.SI1145_REG_ALSIRDATA1)
    raw = ( msb << 8 ) + lsb
    print("IR: %d [%d,%d]" %(raw,msb,lsb))
    return raw

    
  """returns the UV index * 100 (divide by 100 to get the index)"""
  """uint16_t Adafruit_SI1145::readUV(void) {"""
  def readUV(self):
    #return read16(0x2C);
    lsb = self.bus.read_byte_data(self.SI1145_ADDR,self.SI1145_REG_UVINDEX0)
    msb = self.bus.read_byte_data(self.SI1145_ADDR,self.SI1145_REG_UVINDEX1)
    raw =  ( msb << 8 ) + lsb
        
    uv = float(raw) / 100.00
    print("UV: %.2f [%d,%d]" %(uv,msb,lsb))
    return uv

"""Running in STAND ALONE mode."""
if __name__ == "__main__":
    
  SIUV = SI1145()

  while True:
    #This is what we do all the time
    try:

      #Serial.println("===================");
      print("===================")
      
      vis = SIUV.readVisible()
      #print("Vis: %d" % vis)

      ir = SIUV.readIR()
      #print("IR: %d" % ir)

      uv = SIUV.readUV()
      #print("UV: %.2f" % uv)

      #delay(1000);
      time.sleep(1)      

    #Unless there is a CTRL-C Keyboard interupt
    except KeyboardInterrupt:
      print("Ctrl-c received!")
      break     


