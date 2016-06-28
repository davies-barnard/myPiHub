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
import plotly.graph_objs as go # (*) Graph objects to piece together plots

import numpy as np # (*) numpy for math functions and arrays

_HEXDEC = {v: int(v, 16) for v in (x+y for x in _NUMERALS for y in _NUMERALS)}

class Plotter:
  
  """Awww, debugging!"""
  debug = True
  
  """The following are values for max and min temp as defined by
   http://www.hse.gov.uk/temperature/assets/docs/heat-stress-checklist.pdf
   http://www.hse.gov.uk/pubns/indg451.pdf """
  minT = 16.0
  maxT = 23.0
  
  
  """This is the initialisation function called when the program starts"""
  def __init__(self,logger,interval,parameters,xData,yData):
    self.logger = logger
    self.interval = interval
    self.parameters = parameters
    self.plotX = xData
    self.plotY = yData
    
    self.plotGen()


  """Convert HEX to RGB"""
  def rgb(triplet):
      return _HEXDEC[triplet[0:2]], _HEXDEC[triplet[2:4]], _HEXDEC[triplet[4:6]]

  """This method updates the plotly plot"""
  def plotGen(self):
  
    # Create a trace    
    trace = go.Scatter(
      x=self.plotX,
      y=self.plotY,
      mode = 'lines',
      marker = dict (
        color = rgb(self.interval['linecolor']),
        line = dict (
          width = 1,
        )
      )
    )
    
    # Load the data
    data = go.Data ([trace])
    
    #Update the plot
    try:
      #self.plot_url = py.plot(data, filename=self.plotname.lower().replace(" ","_"))
      layout = go.Layout(title=self.interval, width=800, height=640)
      fig = go.Figure(data=data, layout=layout)
      py.image.save_as(fig, filename=self.interval+'.png')
      
    except:
      self.logger.log("Plot Error: " + sys.exc_info()[0])
      return False
    
    #Return True if successful.
    return True

if __name__ == "__main__": 
  plot = Plotter()
