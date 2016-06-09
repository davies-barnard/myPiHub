import time
import Adafruit_CharLCD as LCD

class LCDController():

    # Raspberry Pi pin configuration:
    lcd_rs        = 25  # Note this might need to be changed to 21 for older revision Pi's.
    lcd_en        = 24
    lcd_d4        = 23
    lcd_d5        = 17
    lcd_d6        = 21
    lcd_d7        = 22
    lcd_backlight = 4

    # Define LCD column and row size for 16x2 LCD.
    lcd_columns = 16
    lcd_rows    = 2

    # Initialize the LCD using the pins above.
    def __init__(self,logger):

        self.lcd = LCD.Adafruit_CharLCD(
            self.lcd_rs,
            self.lcd_en,
            self.lcd_d4,
            self.lcd_d5,
            self.lcd_d6,
            self.lcd_d7,
            self.lcd_columns,
            self.lcd_rows,
            self.lcd_backlight)

        self.logger = logger
        

    # Print a two line message - use \n to use both lines
    def setMessage(self,message,backlight=False):
        debugMessage = message.split("\n")
        self.lcd.clear()
        if len(debugMessage) > self.lcd_rows:
            self.logger.log("info","WARNING: Message contains more rows than display.  Suggest scrolling.")

        for line in debugMessage:
            if len(line) > self.lcd_columns:    
                self.logger.log("info","WARNING: A Line is longer than the display.  Suggest scrolling.")
            
        self.lcd.set_backlight(backlight)
        self.lcd.message(message)
        

    # Stop blinking and showing cursor.
    def setCursor(self,show=True,blink=True):
        self.lcd.show_cursor(show)
        self.lcd.blink(show)

    # Demo scrolling message right/left.
    def scrollingText(self,message,backlight=False):
        self.backlight(backlight)
        self.lcd.clear()
        self.lcd.message(message)
        print(self.lcd_columns,len(message))
        
        for i in range(self.lcd_columns-len(message)):
            print("Right",i)
            time.sleep(0.5)
            self.lcd.move_right()

        for i in range(self.lcd_columns-len(message)):
            print("Left",i)
            time.sleep(0.5)
            self.lcd.move_left()

    def seesaw(self,message,backlight):
        self.backlight(backlight)
        
        for i in range(0,len(message)):
            
            self.lcd.clear()
            self.lcd.message(message)
            time.sleep(0.5)

            self.lcd.clear()
            self.lcd.message("\n"+message)
            time.sleep(0.5)

    def backlight(self,status = True):
        if status: 
            self.lcd.set_backlight(0)
        else:
            self.lcd.set_backlight(1)
            
    def cleanup(self):
        #self.backlight(False)
        pass
        #GPIO.cleanup()


if __name__ == '__main__':

  try:
    lcd = LCDController()
    lcd.seesaw("Miss Ryan Rocks!",True)
    #lcd.cleanup()
  except KeyboardInterrupt:
    pass
  finally:
    lcd.cleanup()
