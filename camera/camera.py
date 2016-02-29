from picamera import PiCamera
from time import sleep
import datetime

#http://imageio.readthedocs.io/en/latest/
try:
  import imageio
except ImportError:
  print("This script requires imageio")
  sys.exit()

#
try:
  from sense_hat import SenseHat
except ImportError:
  print("This script requires imageio")
  sys.exit()
  
class CamWrap():

    camera = None
    sHat = None
    ALPHA = 150 #Transparency of the preview

    ## This is the constructor
    def __init__(self):
        self.camera = PiCamera()
        self.camera.rotation = 0

        self.sHat = SenseHat()
        self.sHat.set_rotation(270)

    def setMessage(self,msg):
        if self.sHat is not None:
            self.sHat.show_message(msg)

    def getTimeStamp(self):
        ds = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        return ds

    def stopPreview(self):
        self.camera.stop_preview()  

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

        if len(images) > 2:
            agif = self.makeGif(images, path + ".gif")

    ## This method uses all the filenames to create a animated gif
    def makeGif(self, filenames, exportname):
            
        # Load each file into a list
        images = []
        for filename in filenames:
            images.append(imageio.imread(filename))

        # Save them as frames into a gif and return the filename
        imageio.mimsave(exportname, images)
        return exportname

    def watchingYou(self):
        try:
            self.setMessage("Watching You! ;)")
            self.camera.start_preview()
        except IOError as e:
            print(e)
        finally:
            exit()

cw = CamWrap()
ds = cw.getTimeStamp()
cw.recordTimeLapse('./captures/' + ds,"jpg",5,1)
#cw.takePhoto('./captures/' + ds,"jpg")
#cw.watchingYou()
