#!/usr/bin/python

import sys
import os
import re
from subprocess import *
from time import sleep, time, mktime #For date and time related stuff
from datetime import datetime, timedelta

#Custom PIP imports
from configobj import ConfigObj #For configuration.
import tweepy #http://docs.tweepy.org/en/v3.5.0/
import ephem #For Sun Rise and Set

#Greenhouse include imports
from includes.database import Database
from includes.logger import *
from includes.reportgenerator import ReportGenerator
from includes.cameraengine import CameraEngine
from includes.twitterengine import TwitterEngine

#Raspberry Pi specific imports
try:
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
				
				#Set up some times before converting our looping and interval times into integers.
				self.systime = int(time())
				self.sunSetRise()
				self.config['Greenhouse']['looptime'] = int(self.config['Greenhouse']['looptime'])
				self.config['Camera']['interval'] = int(self.config['Camera']['interval'])

				#Set up the twitter
				self.twitter = TwitterEngine(self.logger,self.config['Twitter'])

				#Create a camera object
				self.camera = CameraEngine(self.logger,self.config['Camera'])
				self.countToShot = 0
				
				#Raspberry Pi / Run mode specifics
				if self.config['Greenhouse']['simulator'] == "True":
					self.config['Greenhouse']['simulator'] = True
				else:
					self.config['Greenhouse']['simulator'] = False
					self.tp = TempProbe()
					self.lcd = LCDController(self.logger)

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
				self.countToShot -=	 self.config['Greenhouse']['looptime']
		
				#Sunrise greater than sunset equals daytime and we have reached our interval take images
				if self.sunrise > self.sunset and self.countToShot <= 0:

						self.gifDone = False

						#Try and capture an image
						try:
								imgname = self.camera.captureImage(self.getTimeStamp)
								if imgname is not None:
										self.images.append(imgname)
								self.delayTime()

						#Camera IO Error
						except IOError as e:
								self.logger.log("critical","Capture Time Lapse Error:" + e)
						
						print("Updating Sun Rise/Set for Testing")
						self.sunset = 1000
						self.sunrise = 2000


				#Its night time and we should compile our timelapse
				elif self.gifDone == False:

						self.logger.log("info","Produce Time Lapse Caught")
						
						#If we have grabbed some images then we can make our gif and delete the captures.
						filename = re.sub(r'[\W_]',"",str(self.sunsetStr))
						agif = self.camera.makeGif(self.images,filename,deleteImages=False)
						
						#Reset the images and recalculate sunrise/sunset
						self.images = []
						self.sunSetRise()
						self.gifDone = True

						#Tweet the timelapse
						if not self.config['Greenhouse']['simulator']:
							self.logger.log ("info", "Dummy Tweeting %s %s" %(photo_path,status))
						else:
							self.twitter.sendTweetWithMedia("Greenhouse Tweet Test",agif)
							sys.exit()

				else:
					 self.logger.log("info","Gif done and waiting for the morning")


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
	
		
