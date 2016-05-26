from configobj import ConfigObj
from logger import *

""" Greenhouse Class used for monitoring the GH. """
class Greenhouse():

    """ The Constructor Method """
    def __init__(self):

        #Load the configuration file.
        config = ConfigObj('greenhouse.conf')

        #

        print("New Greenhouse")


"""Running in STAND ALONE mode."""
if __name__ == "__main__":

    gh = Greenhouse()
    
