import os
import glob
import time
import datetime
from plotter import Plotter

class ReportGenerator():

    def __init__(self,logger,config,db):
      print ("Report Generator Intialisation")
      self.logger = logger
      self.config = config
      self.db = db 
      self.logger.log("info","Report Generator Set Up")
      print(self.config)  
      
      
    def run(self):
      self.logger.log("info","Running Reports")
      
      #For each of the plotting intervals in the configuration file
      for interval, parameters in self.config.items():
        self.logger.log("info","Running report for " + interval)
        
        if float(parameters['timediff']) > 0.0:
          endTs = time.time()
          startTs = endTs - float(parameters['timediff'])
          sql = "SELECT * FROM 'archive' WHERE ts between "+ str(startTs) +" and " + str(endTs) + " order by ts desc;"
        else:
          sql = "SELECT * FROM 'archive' order by ts desc;"
        
        
        response = self.db.runQuery(sql,fetchall=True)
        
        if len(response) <= 0:
          continue
          
        #Split the database response into timestamps and temps
        timeline, temps = zip(*response)
        
        #Convert them into lists
        timeline = list(timeline)
        temps = list(temps)
        print(timeline,temps)
        
        #plot chart
        timeline = [ datetime.datetime.fromtimestamp(int(d)).strftime('%Y-%m-%d %H:%M:%S') for d in timeline]
        Plotter(self.logger, interval, parameters, timeline, temps,)
        
        #Get maximums, minimums and averages
        maximum = max(temps)
        maximumTs = timeline[temps.index(maximum)]
        minimum = min(temps)
        minimumTs = timeline[temps.index(minimum)]
        average = sum(temps)/float(len(temps)) 

        print(maximum, maximumTs, minimum, minimumTs, average)

      