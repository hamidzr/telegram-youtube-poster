#!/usr/bin/python3
# -*- coding: utf-8 -*-
# encoding=utf8



import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import os
import requests
import json
import sys
import pafy
import datetime
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

TARGET_CHAT = config['DEFAULT']['TARGET_CHAT']
TARGET_CHANNEL = config['DEFAULT']['TARGET_CHANNEL']
BOT_TOKEN = config['DEFAULT']['BOT_TOKEN']
YOUTUBE_API = config['DEFAULT']['YOUTUBE_API']

update_id = None



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
  global update_id
  # Telegram Bot Authorization Token
  bot = telegram.Bot(BOT_TOKEN)

  # get the first pending update_id, this is so we can skip over it in case
  # we get an "Unauthorized" exception.
  try:
    update_id = bot.getUpdates()[0].update_id
  except IndexError:
    update_id = None

  logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



  date = datetime.date.today().strftime('%d, %b %Y')
  bot.sendMessage(chat_id= TARGET_CHANNEL, text= "Top trending youtube videos for {}".format(date))

  # search youtube and create a list of urls
  trendsJson = getTrends();
  for idx, res in enumerate(trendsJson['items']):
    id = res['id']
    try:
      video = pafy.new("https://www.youtube.com/watch?v={}".format(id))
      print(idx + 1, video.title, id)
      # title = res['snippet']['title']
      # thumbnail = res['snippet']['thumbnails']['standard']['url']
      # duration = res['contentDetails']['duration'][2:]
      # print(str(idx+1),title,duration,thumbnail)

      # get download the video and get status
      os.system('wget -q {} -O /tmp/{}.jpg'.format(video.bigthumbhd,id))
      status = os.system('youtube-dl -q -f 18,36 --max-filesize 45m --output "/tmp/%(id)s.mp4"  -- {}'.format(id))
      if status == 0:
        fileAddress= ('/tmp/' + id + '.jpg')
        print(fileAddress)
        with open(fileAddress,'rb') as photoFile:
          print('sending photo')
          bot.sendPhoto(chat_id= TARGET_CHANNEL, photo=photoFile, caption= video.title[:45] + ' .. ' +  video.description[:140], disable_notification= True)
        fileAddress= ('/tmp/' + id + '.mp4')
        print(fileAddress)
        with open(fileAddress,'rb') as videoFile:
          print('sending video')
          bot.sendVideo(chat_id= TARGET_CHANNEL, video=videoFile, caption= video.title[:150] + ' @freetube' , duration=video.length, disable_notification= True, timeout=150)
    except Exception as e:
      print(e)
      print('error ', idx, id)


if __name__ == '__main__':
  main()
