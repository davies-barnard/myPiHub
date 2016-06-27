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

