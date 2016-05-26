from configobj import ConfigObj
from includes.logger import *
import time
from threading import Thread
import sys


""" This class extends Thread with a Timelapsing and tweeting Class
" This method will take a series of photos and then
" tweet the resulting image to tweeter. """
class TimelapseThread(Thread):

    """Set some args and start a thread."""
    def __init__(self,logger,duration,interval):
    
        #Our thread.
        Thread.__init__(self)

        # A flag to notify the thread that it should finish up and exit
        self.kill_received = False

        # The logger object from its parent
        self.logger = logger
        
        # Some args used by the main function
        self.duration = duration
        self.interval = interval


    """The run method that periodically checks for a kill flag"""
    def run(self):
        while not self.kill_received:
            self.timelapse()

    """The main timelapse method """
    def timelapse(self):
        log(self.logger,"info","Time Lapsing Tweet")

        self.count = int(self.duration / self.interval)
        for i in range(0,self.count):
            print("Take Photo")
            time.sleep(self.interval)
            
        print("Produce TL and Tweet")




""" The MAIN Greenhouse Program starts here """
def main(args):

    #Load the configuration file.
    config = ConfigObj('greenhouse.conf')

    #Initialize the logger and send a starting entry.
    logger = initialize_logger(config['Greenhouse']['log_folder'])
    log(logger,"info","Greenhouse System Started")

    #Create our threads for the system
    threads = []
    for i in range(10):
        t = TimelapseThread(logger,5,1)
        threads.append(t)
        t.start()

    #Keep the program running while we have threads and no one has pressed CTRL-C
    while len(threads) > 0:
        try:
            # Join all threads using a timeout so it doesn't block
            # Filter out threads which have been joined or are None
            threads = [t.join(1) for t in threads if t is not None and t.isAlive()]
        except KeyboardInterrupt, SystemExit:
            log(logger,"info","Ctrl-c received! Sending kill to threads...") 
            for t in threads:
                t.kill_received = True

      

"""Running in STAND ALONE mode."""
if __name__ == "__main__":
    main(sys.argv)

    
