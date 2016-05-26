import os, sys
import datetime
from time import sleep
from logger import *
from picamera import PiCamera
from PIL import image



#http://imageio.readthedocs.io/en/latest/
try:
  import imageio
except ImportError:
  #logging.critical("This script requires imageio")
  sys.exit()

#https://www.raspberrypi.org/products/sense-hat/
try:
  from sense_hat import SenseHat
except ImportError:
  #logging.critical("This rPi has no SenseHat or the Library")
  sys.exit()

"""This is a picamera wrapper with helper methods for doing cool camera like things"""
class CamWrap():

    camera = None
    sHat = None
    ALPHA = 150 #Transparency of the preview

    ## This is the constructor
    def __init__(self):

        self.logger = initialize_logger()
        self.log("info","CamWrap Started and Logger Initialised")
          
        self.camera = PiCamera()
        self.camera.rotation = 0

        try:
          self.sHat = SenseHat()
          self.sHat.set_rotation(270)          
        except:
          self.log("critical","No SenseHat connected")






    ## This method takes a string and sets it as the message on the Sense Hat
    def setMessage(self,msg):
        if self.sHat is not None:
            self.sHat.show_message(msg)
        else:
            print(msg)


    ## Convert the current timestamp into a datetime string
    def getTimeStamp(self):
        ds = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        return ds


    ## Stop the camera previewing.
    def stopPreview(self):
        self.camera.stop_preview()  


    ## Take a single photo.
    def takePhoto(self,path,ext):
        try:
            self.camera.start_preview(alpha=self.ALPHA)
            sleep(3) #! Important Sleep for >2secs for light levels
            self.camera.capture(path + "." + ext)
            self.camera.stop_preview()
        except IOError as e:
            print(e)
        finally:
            self.camera.stop_preview()

    ## Record a timelapse series of images and create an animated gif.
    def recordTimeLapse(self, path, ext, length=10, delay=1):
        images = []
        try:
            #self.camera.start_preview(alpha=self.ALPHA)
            sleep(3) #! Important Sleep for >2secs for light levels
            for i in range(0,length):
                self.setMessage(str(i))
                imgname = path + "_" + str(i) + "." + ext
                self.camera.capture(imgname)
                images.append(imgname)
                sleep(delay)
            #self.camera.stop_preview()
        except IOError as e:
            print(e)
        finally:
            self.camera.stop_preview()
            self.sHat.clear()

        #If we have grabbed some images then we can make our gif and delete the captures.
        if len(images) > 2:
            agif = self.makeGif(images, path + ".gif")
            for image in images:
              os.remove(image)
            

    ## This method uses all the filenames to create a animated gif
    def makeGif(self, filenames, exportname):
            
        # Load each file into a list
        images = []
        for filename in filenames:
            images.append(imageio.imread(filename))

        # Save them as frames into a gif and return the filename
        imageio.mimsave(exportname, images)
        return exportname

    ## This is just a simple preview.
    def watchingYou(self):
        try:
            self.setMessage("Watching You! ;)")
            self.camera.start_preview()
        except IOError as e:
            print(e)
        finally:
            exit()


    ## Resize images
    def resizeImage(self):
      print("Resizing Image")


"""Running in STANDALONE mode."""
if __name__ == "__main__":

  if len(sys.argv) <= 1:
    print("""You need to tell me what to do.""")

  elif sys.argv[1] == '--timelapse':
    cw = CamWrap()
    ds = cw.getTimeStamp()
    cw.recordTimeLapse('./captures/' + ds,"jpg",5,1)

  elif sys.argv[1] == "--photo":
    cw = CamWrap()
    ds = cw.getTimeStamp()
    cw.takePhoto('./captures/' + ds,"jpg")

  else:
    print("Unknown Option")
