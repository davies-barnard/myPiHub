## http://stackoverflow.com/questions/3688870/create-animated-gif-from-a-set-of-jpeg-images
import sys
from os import walk

#http://imageio.readthedocs.io/en/latest/
try:
  import imageio
except ImportError:
  print("This script requires imageio")
  sys.exit()

"""The TimeLapse class uses imageio to create an animated gif from a set of images"""
class TimeLapse():
  
  ## The CONSTRUCTOR
  def __init__(self, tPath = None):
    self.path = tPath

    
  ##  This method gets all the filenames in our given timelapse folder. 
  def getFilenames(self):
    self.filenames = []
    for (dirpath, dirnames, self.filenames) in walk(self.path):
        break

  
  ## This method uses all the filenames to create a animated gif
  def makeGif(self):
    
    # Load the filename and return False if there is none.
    self.getFilenames()
    if self.filenames == None:
      return False
    
    # Load each file into a list
    images = []
    exportname = '/movie.gif'
    for filename in self.filenames:
        images.append(imageio.imread(self.path + '/' + filename))

    # Save them as frames into a gif and return the filename
    imageio.mimsave(self.path + exportname, images)
    return self.path + exportname 
    
    
"""Running in TEST mode."""
if __name__ == "__main__":
  
  #Create a new Time Lapse object
  tl = TimeLapse('./tl_images')
  
  #Make our animated gif
  result = tl.makeGif()
  