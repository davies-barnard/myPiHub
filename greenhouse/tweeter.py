#Get our imports
import time
import json
from twitter import *
from pprint import pprint

""" Tweeter Class used to interact with Twitter. """
class Tweeter():

  #My app keys and secrets
  CONSUMER_KEY = "FbmP1fVhbyxh086wqOTn8QGuJ"
  CONSUMER_SECRET = "DUPWuI6zFqCjSqxkC2VGhF3VSViQVVjdg9PGx763Nel7Ux89HC"
  ACCESS_TOKEN = "576973720-hWobEhUViR85iOtDxNepichkWC1trSTvMTh8JCMO"
  ACCESS_SECRET = "AqgDkqbxrVINU60UFp083iAYqlFCAHXj3ISFIz8cWknmf"

  """ The Constructor Method """
  def __init__(self):
    
    # My twitter object that will be used to interact with the api
    self.myTwitter = Twitter(
    	auth=OAuth(self.ACCESS_TOKEN,self.ACCESS_SECRET,self.CONSUMER_KEY,self.CONSUMER_SECRET)
    )


  """ Get the latest tweet """
  def getLatestTweets(self,user=False,count=1):
    self.turl = "http://api.twitter.com/1.1/search/tweets.json?q="
    self.timeline = []
    if user:
      templine = self.myTwitter.statuses.user_timeline()
    else:
      templine = self.myTwitter.statuses.home_timeline()
    templine = templine[:count]
    for tweet in templine:
      temp = {
        'created_at' : tweet['created_at'],
        'text' : tweet['text'],      
      }
      self.timeline.append(temp)


  """ Send a tweet """
  def sendTweet(self,statusUpdate):
    self.myTwitter.statuses.statuses.update(status=statusUpdate)



"""Running in TEST mode."""
if __name__ == "__main__":
  
  tw = Tweeter()
  tw.getLatestTweets(True)
  
  tw.sendTweet("Using @sixohsix's sweet Python Twitter Tools.")
  