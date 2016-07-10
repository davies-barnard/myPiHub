#Get our imports
from configobj import ConfigObj
import time
import json
import tweepy #Non-native Tweeter App.
from pprint import pprint

""" Tweeter Class used to interact with Twitter. """
class TwitterEngine():

	""" The Constructor Method """
	def __init__(self, logger,config):

		self.logger = logger
		self.config = config
		
		# Application twitter object that will be used to interact with the api
		# Tweepy Read The Docs - Introduction
		
		auth = tweepy.OAuthHandler(self.config['consumer_key'],self.config['consumer_secret'])
		auth.set_access_token(self.config['access_token'],self.config['access_secret'])
		self.appTwitter = tweepy.API(auth)
		self.logger.log("info","Twitter Set Up")

		
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
		try:
			self.appTwitter.update_with_media(photo_path,status)
		except tweepy.error.TweepError, te:
			self.logger.log("info","Twitter Error %s"%te)

"""Running in TEST mode."""
if __name__ == "__main__":

		#Load our configuration file, initialize the logger and send a starting entry.
		from configobj import ConfigObj #For configuration.
		from logger import *
		config = ConfigObj('greenhouse.conf')
		logger = Logger(config['Greenhouse']['log_folder'], config['Greenhouse']['debug'])
		logger.log("info","Greenhouse System Started")

		tw = TwitterEngine(logger, config['Twitter'])
		tw.sendTweetWithMedia("This is a test.","captures/201679203220.gif")
