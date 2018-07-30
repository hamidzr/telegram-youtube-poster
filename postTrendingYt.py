#!/usr/bin/python3
# -*- coding: utf-8 -*-
# encoding=utf8

import logging
from time import sleep
import requests
import json
import sys
import datetime
import configparser
from modules.youtube import *
from modules.poster import *

config = configparser.ConfigParser()
config.read('config.ini')

TARGET_CHAT = config['DEFAULT']['TARGET_CHAT']
TARGET_CHANNEL = config['DEFAULT']['TARGET_CHANNEL']
BOT_TOKEN = config['DEFAULT']['BOT_TOKEN']
YOUTUBE_API = config['DEFAULT']['YOUTUBE_API']

bot = Poster(token=BOT_TOKEN, target_chat=TARGET_CHAT, target_channel=TARGET_CHANNEL)

# pre: gets an encoded url pointing to a json endpoint
# post: returns a python dic representing the response
def getJson(url):
  print('Calling url: ',url)
  # httpResponse = urllib.request.urlopen(url)
  httpResponse = requests.get(url)
  return httpResponse.json()

def getTrends():
  url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&chart=mostPopular&maxResults=10&key={}'.format(YOUTUBE_API)
  return getJson(url)

def main():
  logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

  date = datetime.date.today().strftime('%d, %b %Y')
  bot.sendMessage(text= "Top trending youtube videos for {}".format(date))

  # search youtube and create a list of urls
  trendsJson = getTrends();
  for idx, res in enumerate(trendsJson['items']):
    id = res['id']
    bot.sendYoutubeVideo(id)

if __name__ == '__main__':
  main()
