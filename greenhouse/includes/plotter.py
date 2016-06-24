#!/usr/bin/env python

#python -c "import plotly; plotly.tools.set_credentials_file(username='compu2learn', api_key='78cmuvi4ho')"
#http://www.modmypi.com/blog/ds18b20-one-wire-digital-temperature-sensor-and-the-raspberry-pi
#https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing?view=all
#http://data.designspark.info/uploads/images/53bc258dc6c0425cb44870b50ab30621

from random import uniform
import os
import glob
import time

import plotly.plotly as py # (*) To communicate with Plotly's server, sign in with credentials file
import plotly.tools as tls # (*) Useful Python/Plotly tools
from plotly.graph_objs import *  # (*) Graph objects to piece together plots
import numpy as np # (*) numpy for math functions and arrays

class App:
	
	"""Awww, debugging!"""
	debug = True
	
	
	"""The following are values for max and min temp as defined by
	 http://www.hse.gov.uk/temperature/assets/docs/heat-stress-checklist.pdf
	 http://www.hse.gov.uk/pubns/indg451.pdf """
	minT = 16.0
	maxT = 23.0
	
	
	"""These are for our archive temperatures and interval temps"""
	archive = "temp.csv"
	temps = None
	

	"""These are for the temperature sensor attached to the RPI
	 depending on the value of temppi the sensor will be read or a random value will be used."""
	sensorpin = 28  #Default values are 28 or None
	base_dir = ''
	device_folder = None
	device_file = ''
	
	
	"""We can monitor the sensor more often than we plot."""
	monitorPeriod = 60 #How many periods due you want to average over?
	monitorStep = 1 #What step (in secs) do you want to make. 
	
	
	"""This vars are related to the plotly calls.
	https://plot.ly/python/getting-started/ """
	plotPeriod = 300 #This is the period at which we post to Plotly - should not be less than 60.
	plot_ts = 0 #This is a timestamp for the last time that we posted to plotly.
	plotX = []
	plotY = []
	ploturl = None
	#plotname = 'Eye See Tea Won Temps'
	plotname = 'Test'
	
	"""This is the initialisation function called when the program starts"""
	def __init__(self):
		
		# If the sensor pin has a value then set up and use the sensor else run in sim mode.
		if self.sensorpin:
			self.base_dir = '/sys/bus/w1/devices/'
			self.device_folder = glob.glob(self.base_dir + str(self.sensorpin) + '*')[0]
			self.device_file = self.device_folder + '/w1_slave'
		else:
			self.log("Running in Sim Mode")

		self.initPlotly()

		#Clear the archive and start monitoring.
		if self.clearArchive:
			self.log("Archive cleared OK!")
		self.run()

	"""This is the main program for the App.
	It calls an interval function which checks the temperature for a set period 
	and then uses the generated list for archiving"""
	def run(self):
		
		#While the program is running
		while True:
			
			#Monitor the temps for a given interval
			self.monitorInterval()
			
			#Calculate the average and record it with a timestamp
			now_ts = time.time()
			ctime = time.strftime("%Y/%m/%d %H:%M:%S")
			avgtemp = sum(self.temps) / len(self.temps)
			self.plotX.append(ctime)
			self.plotY.append(str(avgtemp))
			self.log(ctime + ": " + str(avgtemp))

			#If enough time has passed then we can pass our average dictionary to Plotly
			if (now_ts - self.plot_ts) > self.plotPeriod:
				#If our call to updatePlot returns true then everything went ok
				#Else there was a problem and we can try again next interval
				if self.updatePlot():
					self.plot_ts = now_ts


	"""This method gets a number of temp readings over a given period and then passes them back for averaging.""" 
	def monitorInterval(self):
		
		#Reset some vars
		self.temps = []
		i = 0;
		
		#While our monitoring period has not expired, read the temps
		while i < self.monitorPeriod:
			t = self.read_temp()
			if t:
				self.temps.append(t)
				i = i + 1
			time.sleep(self.monitorStep)

	"""This is where we set up our plot
	based on https://plot.ly/python/streaming-line-tutorial/"""
	def initPlotly(self):

		# Initialize trace of streaming plot by embedding the unique stream_id
		self.plot = Scatter(
			x=[],
			y=[],
			mode='lines+markers',
		)
		data = Data([self.plot])
		layout = Layout(title=self.plotname)

		fig = Figure(data=data,layout=layout)
		self.ploturl = py.plot(fig,filename=self.plotname.lower().replace(" ","_"), fileopt='extend', auto_open=False)

	"""This method updates the plotly plot"""
	def updatePlot(self):
		self.log("Time to plot!")
		self.log(",".join(self.plotX))
		self.log(",".join(self.plotY))

		#Create new data
		new_data = Scatter(x=self.plotX, y=self.plotY)
		data = Data ([new_data])
		
		#Update the plot
		try:
			self.plot_url = py.plot(data, filename=self.plotname.lower().replace(" ","_"), fileopt='extend', auto_open=False)
		except:
			self.log("Plot Error: " + sys.exc_info()[0])
		#Reset the lists
		self.plotX = []
		self.plotY = []
		return True


	"""Update our archive file"""
	def updateArchive(self,temp):
		try:
			archivefile = open(self.archive,"a")
			archivefile.write(ctime + ";" + str(temp) + "\n")
		except IOError, e:
			return False
		finally:
			if archivefile:
				archivefile.close()
			return True


	"""Clear the archive file"""
	def clearArchive(self,temp):
		try:
			archivefile = open(self.archive,"a")
		except IOError, e:
			return False
		finally:
			if archivefile:
				archivefile.close()
			return True


	"""This is a debugging method."""
	def log(self,message):
		if self.debug:
			print(message)


	"""Get a raw temperature value from the sensor or create a random value if in Sim mode."""
	def read_temp(self):
		#We have an attached sensor
		try:
			if self.sensorpin:		
				lines = self.read_temp_raw()
				while lines[0].strip()[-3:] != 'YES':
					time.sleep(0.2)
					lines = self.read_temp_raw()
				equals_pos = lines[1].find('t=')
				if equals_pos != -1:
					temp_string = lines[1][equals_pos+2:]
					temp_c = float(temp_string) / 1000.0
					#temp_f = temp_c * 9.0 / 5.0 + 32.0
				
			#We are in Sim Mode
			else:
					temp_c = uniform(15.0,30.0)
					#temp_f = temp_c * 9.0 / 5.0 + 32.0

			#return our values
			return temp_c #, temp_f
		except:
			self.log("Plot Error: " + sys.exc_info()[0])
			return None
		

	"""This reads a raw value from the w1 sensor"""
	def read_temp_raw(self):
		f = open(self.device_file, 'r')
		lines = f.readlines()
		f.close()
		return lines


	"""This is an alternative to the raw above in case of issues"""
	def read_temp_raw_alt(self):
		catdata = subprocess.Popen(['cat',self.device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out,err = catdata.communicate()
		out_decode = out.decode('utf-8')
		lines = out_decode.split('\n')
		return lines


"""
END OF App Class
"""

"""
MAIN - This is where it all starts from - keeping stuff to the bare minimum.
""" 
app = App()
