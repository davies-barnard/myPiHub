#!/usr/bin/python

import sys
import os
from subprocess import *
from time import sleep, time, mktime #For date and time related stuff
from datetime import datetime, timedelta

#Custom PIP imports
from configobj import ConfigObj #For configuration.
from PIL import Image
import imageio  #http://imageio.readthedocs.io/en/latest/
import tweepy #http://docs.tweepy.org/en/v3.5.0/
import ephem #For Sun Rise and Set

#Greenhouse include imports
from includes.database import Database
from includes.logger import *
from includes.reportgenerator import ReportGenerator

#Raspberry Pi specific imports
try:
  from picamera import PiCamera
  from includes.tempprobe import TempProbe #For the temperature probes etc.
  from includes.lcdcontroller import LCDController
except ImportError:
  print ("Are we running on a RPi?")



""" This class extends Thread with a Timelapsing and tweeting Class
This method will take a series of photos and then
tweet the resulting image to tweeter. """
class Greenhouse():


    camera = None
    images = []
        

    """Set some args and start a thread."""
    def __init__(self):

        #Load the configuration file.
        self.config = ConfigObj('greenhouse.conf')
        
        #Initialize the logger and send a starting entry.
        self.logger = Logger(self.config['Greenhouse']['log_folder'], self.config['Greenhouse']['debug'])
        self.logger.log("info","Greenhouse System Started")

        #Set up the temp probe etc.
        self.db = Database(self.logger,self.config['Database'])

        #Create a report generator object
        self.reporter = ReportGenerator(self.logger,self.config['Reports'],self.db)

	self.config['Greenhouse']['looptime'] = int(self.config['Greenhouse']['looptime'])
	self.config['Camera']['interval'] = int(self.config['Camera']['interval'])

        
        #Set up the twitter and the camera
        self.twitterSetup()
        self.cameraSetup()

	self.systime = int(time())
        self.sunSetRise()
        self.countToShot = 0
        
        #Raspberry Pi / Run mode specifics
        if self.config['Greenhouse']['simulator'] == "True":
          self.config['Greenhouse']['simulator'] = True
        else:
          self.config['Greenhouse']['simulator'] = False
          self.tp = TempProbe()
          self.lcd = LCDController(self.logger)
        
    
    """Set up the camera"""
    def cameraSetup(self):
        self.logger.log("info","Camera Set Up")
          
        self.camera = PiCamera()
        self.camera.rotation = self.config['Camera']['rotation']

        res = (int(self.config['Camera']['resolution'][0]),int(self.config['Camera']['resolution'][1]))
        self.logger.log("info",str(res))
        self.camera.resolution = res


    """Application twitter object that will be used to interact with the api"""
    def twitterSetup(self):
        self.logger.log("info","Twitter Set Up")
        auth = tweepy.OAuthHandler(self.config['Twitter']['consumer_key'],self.config['Twitter']['consumer_secret'])
        auth.set_access_token(self.config['Twitter']['access_token'],self.config['Twitter']['access_secret'])
        self.twitter = tweepy.API(auth)       


    """The run method that periodically checks for a kill flag"""
    def run(self):

        self.logger.log("info","Greenhouse is running")
        while True:
            
            #This is what we do all the time
            try:

		#Update system time.
		self.systime = int(time())

                #Capture the next image (if its time)
                self.captureTimeLapseImage()

                #Get the current temperature
                if not self.config['Greenhouse']['simulator']:
                  self.getMetrics()

                #Sleep the system for the specified time.
                sleep(self.config['Greenhouse']['looptime'])

                #Updates Reports based on interval.
                #self.report()
                
            #Unless there is a CTRL-C Keyboard interupt
            except KeyboardInterrupt:
                self.logger.log("info","Ctrl-c received!")
                break

        #Log that we are shuting down the system    
        self.logger.log("info","Greenhouse is closing")


    """Run the reports as per the configuration file"""
    def report(self):
        
        self.reporter.run()
    

    """Run a terminal command on the pi"""
    def runCommand(self,cmd):
        process = Popen(cmd, shell=True, stdout=PIPE)
        output = process.communicate()[0]
        return output


    """Convert the current timestamp into a datetime string"""
    def getTimeStamp(self):
        ds = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return ds


    """Get the IP Address of the Pi"""
    def getIpAddress(self):
        cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
        ipaddress = self.runCommand(cmd)
        ipaddress = ipaddress.split("\n")
        self.logger.log("info",ipaddress[0])
        return ipaddress[0]


    """This method calculates the delay in seconds till the next hour"""
    def delayTime(self):
        self.countToShot = int(self.config['Camera']['interval']) 
        self.logger.log("info",str(self.countToShot) + " to next photo")


    """Record a timelapse series of images and create an animated gif."""
    def captureTimeLapseImage(self):

        #Is it time to capture an image?
        self.countToShot -=  self.config['Greenhouse']['looptime']
    
        #If sunrise is greater than sunset.
        if self.sunset < self.sunrise:
	    
	    self.gifDone = False

            #If our countdown has reached zero take a photo
            if self.countToShot <= 0:
                
                #Try and capture an image
                try:
                    sleep(3) #! Important Sleep for >2secs for light levels
                    imgname = self.config['Greenhouse']['image_folder'] + "image" + "_" + self.getTimeStamp() + ".jpg"
                    self.camera.capture(imgname)
                    self.images.append(imgname)
                    self.logger.log("info","Capture Time Lapse Caught" + str(len(self.images)))       
                    self.delayTime()

                #Camera IO Error
                except IOError as e:
                    self.logger.log("critical","Capture Time Lapse Error:" + e)

        #Its night time and we should compile our timelapse
        elif self.gifDone == False:

            self.logger.log("info","Produce Time Lapse Caught")
            #If we have grabbed some images then we can make our gif and delete the captures.
            agif = self.makeGif(self.images)
            for image in self.images:
                os.remove(image)

	    #Reset the images and recalculate sunrise/sunset
            self.images = []
	    self.sunSetRise()
	    self.gifDone = True

            #Tweet the timelapse
            self.sendTweetWithMedia("Greenhouse Tweet Test",agif)
	
	else:
	   self.logger.log("info","Gif done and waiting for the morning")


    """ This method uses all the filenames to create a animated gif """
    def makeGif(self, filenames):

        # Load each file into a list
        frames = []
        for filename in filenames:
            frames.append(imageio.imread(filename))

        # Save them as frames into a gif and return the filename
        filename = str(int(time())) #str(self.sunset).replace("/","").replace(":","").replace(" ","")
        exportname = self.config['Greenhouse']['image_folder'] + filename + ".gif"
        imageio.mimsave(exportname, frames)
        return exportname


    """ Send with image """
    def sendTweetWithMedia(self,status,photo_path):
        self.twitter.update_with_media(photo_path,status)


    """Calculate the Naval Sun Rise and Set so we don't take photos during the night"""
    def sunSetRise(self):
        somewhere = ephem.Observer()
        somewhere.lat = self.config['Greenhouse']['Location']['latitude']
        somewhere.lon = self.config['Greenhouse']['Location']['longitude']
        somewhere.elevation = int(self.config['Greenhouse']['Location']['elevation'])
        somewhere.horizon = '-0:34'

        sun = ephem.Sun()
        self.sunriseStr = somewhere.next_rising(sun)
        self.sunsetStr = somewhere.next_setting(sun)
        self.sunrise = int(mktime(ephem.localtime(self.sunriseStr).timetuple()))
        self.sunset = int(mktime(ephem.localtime(self.sunsetStr).timetuple()))
        self.logger.log ("info", ("Sun Rise/Set at %s is %s %s" %(self.systime,self.sunrise, self.sunset)))
	if self.sunrise > self.sunset:
		self.logger.log("info","Currently Day Time")
	else:
		self.logger.log("info","Currently Night Time")



    """Get the current temperature and other metrics"""
    def getMetrics(self):
        temps = self.tp.readTemp()
        ipaddr = self.getIpAddress()
        outStr = "Temp: %.2fC (%.2fF)" % temps
        self.logger.log("info","Temp: %.2fC (%.2fF)" % temps)
        self.lcd.setMessage("Temp: %.2fC\nIP: %s" % (temps[0],ipaddr))
        self.db.createArchive(time(),temps[0])
        
    

"""Running in STAND ALONE mode."""
if __name__ == "__main__":
  
  if len(sys.argv) == 1 or sys.argv[1] == '-run':
    greenhouse = Greenhouse()
    greenhouse.run()
    
  elif sys.argv[1] == '-report':
    greenhouse = Greenhouse()
    greenhouse.report()
    
  else:
    print ("Help")
  
    
