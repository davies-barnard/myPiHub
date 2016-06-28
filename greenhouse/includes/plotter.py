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

#http://stackoverflow.com/questions/4296249/how-do-i-convert-a-hex-triplet-to-an-rgb-tuple-and-back
_NUMERALS = '0123456789abcdefABCDEF'
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
  def __init__(self,logger, path, plotoptions, interval,parameters,xData,yData):
    self.logger = logger
    self.plotoptions = plotoptions
    self.interval = interval
    self.parameters = parameters
    self.plotX = xData
    self.plotY = yData
    self.plotPath = path + "/plots/"
    self.plotGen()


  """Convert HEX to RGB"""
  def rgb(self,triplet):    
      r = int(_HEXDEC[triplet[0:2]])
      g = int(_HEXDEC[triplet[2:4]])
      b = int(_HEXDEC[triplet[4:6]])
      retStr = "rgb(%d,%d,%d,1.0)" % (r, g, b)
      print (retStr)
      return retStr

  """This method updates the plotly plot"""
  def plotGen(self):

    self.rgb('AABBCC')
  
    # Create a trace    
    trace = go.Scatter(
      x=self.plotX,
      y=self.plotY,
      mode = 'lines',
      marker = dict (
        color = 'rgba(152, 0, 0, .8)',
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
      layout = go.Layout(
        title = self.interval.title(),
        font= dict(
          family = self.plotoptions['fontfamily'],
          size = self.plotoptions['fontsize'],
          color = self.plotoptions['fontcolor']
        ),
        width=self.plotoptions['width'],
        height=self.plotoptions['height'])
      fig = go.Figure(data=data, layout=layout)
      py.image.save_as(fig, filename=self.plotPath + self.interval+'.png')
      
    except:
      self.logger.log("Plot Error: " + sys.exc_info()[0])
      return False
    
    #Return True if successful.
    return True

if __name__ == "__main__": 
  plot = Plotter()
