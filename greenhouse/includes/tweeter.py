#Get our imports
from configobj import ConfigObj
import time
import json
import tweepy #Non-native Tweeter App.
from pprint import pprint

""" Tweeter Class used to interact with Twitter. """
class Tweeter():



  

  """ The Constructor Method """
  def __init__(self, myconfig):

    #Load the Tweeter configuration from the config file
    self.config = myconfig
    
    # Application twitter object that will be used to interact with the api
    # Tweepy Read The Docs - Introduction
    auth = tweepy.OAuthHandler(self.config['consumer_key'],self.config['consumer_secret'])
    auth.set_access_token(self.config['access_token'],self.config['access_secret'])
    self.appTwitter = tweepy.API(auth)
    
    

    #User twitter authentication
    #MY_TWITTER_CREDS = os.path.expanduser('~/.twitter_credentials')
    #if not os.path.exists(MY_TWITTER_CREDS):
    #  oauth_token("GH Twitter",CONSUMER_KEY,CONSUMER_SECRET,MY_TWITTER_CREDS)

    #oauth_token,oauth_token_secret = read_token_file(MY_TWITTER_CREDS)

    


  """ Get the latest tweet """
  def getLatestTweets(self,user=False,count=1):
    
    if user:
      templine = self.appTwitter.user_timeline()
    else:
      templine = self.appTwitter.home_timeline()

    self.timeline = []
    templine = templine[:count]
    for tweet in templine:
      temp = {
        'created_at' : tweet.created_at,
        'text' : tweet.text,      
      }
      self.timeline.append(temp)

    return (self.timeline)


  """ Send a tweet """
  def sendTweet(self,status):
    self.appTwitter.update_status(status)

  """ Send with image """
  def sendTweetWithMedia(self,status,photo_path):
    self.appTwitter.update_with_media(photo_path,status)

"""Running in TEST mode."""
if __name__ == "__main__":

    #Load our configuration file
    config = ConfigObj('greenhouse.conf')

    config = config['Tweeter']
  
    tw = Tweeter(config)

    #timeline = tw.getLatestTweets(True)
    #pprint (timeline)
  
    #tw.sendTweet("Using @sixohsix's sweet Python Twitter Tools.")
  
    tw.sendTweetWithMedia("Testing from Python...","./captures/cat.jpg")
