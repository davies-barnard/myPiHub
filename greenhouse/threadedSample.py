#!/usr/bin/python

import os, sys, threading, time

class Worker(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    # A flag to notify the thread that it should finish up and exit
    self.kill_received = False

  def run(self):
      while not self.kill_received:
          self.do_something()

  def do_something(self):
      [i*i for i in range(10000)]
      time.sleep(1)



""" This class extends Thread with a Timelapsing and tweeting Class
" This method will take a series of photos and then
" tweet the resulting image to tweeter. """
class TimelapseThread(threading.Thread):

    """Set some args and start a thread."""
    def __init__(self,duration,interval):
    
        #Our thread.
        threading.Thread.__init__(self)

        # A flag to notify the thread that it should finish up and exit
        self.kill_received = False

        # The logger object from its parent
        #self.logger = logger
        
        # Some args used by the main function
        self.duration = duration
        self.interval = interval


    """The run method that periodically checks for a kill flag"""
    def run(self):
        while not self.kill_received:
            self.timelapse()

    """The main timelapse method """
    def timelapse(self):
        #log(self.logger,"info","Time Lapsing Tweet")

        self.count = int(self.duration / self.interval)
        for i in range(0,self.count):
            print("Take Photo")
            time.sleep(self.interval)
            
        print("Produce TL and Tweet")

def main(args):

    threads = []
    for i in range(10):
        t = TimelapseThread(5,1)
        threads.append(t)
        t.start()

    while len(threads) > 0:
        try:
            # Join all threads using a timeout so it doesn't block
            # Filter out threads which have been joined or are None
            threads = [t.join(1) for t in threads if t is not None and t.isAlive()]
        except KeyboardInterrupt:
            print "Ctrl-c received! Sending kill to threads..."
            for t in threads:
                t.kill_received = True

if __name__ == '__main__':
  main(sys.argv)
