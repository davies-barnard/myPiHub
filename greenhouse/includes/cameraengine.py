#Raspberry Pi specific imports
try:
	from picamera import PiCamera
except ImportError:
	pass

from PIL import Image
import imageio	#http://imageio.readthedocs.io/en/latest/

class CameraEngine():
	
	camera = None
		
	"""Initisation of camera and its resolution and rotation"""
	def __init__(self,logger,config):
		
		self.logger = logger
		
		self.config = config
		
		try:
			self.camera = PiCamera()
			self.camera.rotation = self.config['rotation']

			res = (int(self.config['resolution'][0]),int(self.config['resolution'][1]))
			self.camera.resolution = res

			self.logger.log("info","Camera Set Up @ " + str(self.camera.rotation) + " and " + str(res))
			
		except NameError, e:
			self.logger.log("info","Failed Camera.	Sim Mode?")
			return None
		
		
	"""This method captures an image with the given timestamp"""	
	def captureImage(self,ts):
			if self.camera is not None:
				#sleep(3) #! Important Sleep for >2secs for light levels
				imgname = self.config['path'] + "image" + "_" + str(ts) + ".jpg"
				self.camera.capture(imgname)
				self.logger.log("info","Image Caught" + imgname)
				return imagename
			self.logger.log("info","Camera Offline")
			return None
		
		
	""" This method uses all the filenames to create a animated gif """
	def makeGif(self, images, filename, deleteImages=True):
			
			# Load each file into a list
			frames = []
			count = 0
			skip = 50
			try:
				for image in images:
					if count % skip == 0:
						frames.append(imageio.imread(image))
					count += 1
			except IOError, e:
				self.logger.log("info","GIF Error - problem loading frames " + filename)
			
			# Save them as frames into a gif and return the filename
			exportname = self.config['path'] + "/" + filename + ".gif"
			try:
				imageio.mimsave(exportname, frames)
				self.logger.log("info","GIF created " + exportname)
			except IOError, e:
				self.logger.log("info","GIF Error - not possible to save " + exportname)
				
			#Delete our images
			if deleteImages == True:
				self.logger.log("info","GIF Deleting Images " + exportname)
				for image in images:
						os.remove(image)
			return exportname
			
			
"""Running in TEST mode."""
if __name__ == "__main__":

		#Load our configuration file, initialize the logger and send a starting entry.
		from configobj import ConfigObj #For configuration.
		from logger import *
		config = ConfigObj('greenhouse.conf')
		logger = Logger(config['Greenhouse']['log_folder'], config['Greenhouse']['debug'])
		logger.log("info","Greenhouse System Started")

		camera = CameraEngine(logger,config['Camera'])
		
		# Load each file into a list
		images = []
		for root, dirs, filenames in os.walk("captures"):
			for filename in filenames:
				if filename.endswith(".jpg"):
						images.append(config['Camera']['path']+ "/" + filename)

		camera.makeGif(images,"export",deleteImages=False)