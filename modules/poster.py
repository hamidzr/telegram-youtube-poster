import telegram
from telegram.error import NetworkError, Unauthorized
from .youtube import *

update_id = None

class Poster():
  def __init__(self, token='', target_chat='', target_channel=''):
    self.BOT_TOKEN = token
    self.TARGET_CHAT = target_chat
    self.TARGET_CHANNEL = target_channel
    # Telegram Bot Authorization Token
    self.bot = telegram.Bot(self.BOT_TOKEN)
    try:
      update_id = self.bot.getUpdates()[0].update_id
    except IndexError:
      update_id = None

  def sendMessage(self, **kwargs):
    self.bot.sendMessage(chat_id=self.TARGET_CHANNEL, **kwargs)

  def sendPhoto(self, **kwargs):
    self.bot.sendPhoto(chat_id=self.TARGET_CHANNEL, **kwargs)

  def sendVideo(self, **kwargs):
    self.bot.sendVideo(chat_id=self.TARGET_CHANNEL, **kwargs)


  def sendYoutubeVideo(self, id, image_caption=None, video_caption=None):
    video = download_video(id)
    if video:
      try:
        with open(video.thumbPath,'rb') as photoFile:
          print('sending photo', video.thumbPath)
          imageCaption = image_caption if image_caption else  video.title[:45] + ' .. ' +  video.description[:140]
          self.sendPhoto(photo=photoFile, caption=imageCaption , disable_notification= True)
        with open(video.videoPath,'rb') as videoFile:
          print('sending video', video.videoPath)
          videoCaption =  video_caption if video_caption else  video.title[:150] + ' @freetube'
          self.sendVideo(video=videoFile, caption=videoCaption , duration=video.length, disable_notification= True, timeout=300) # wait up to 5 min for upload
        return video
      except Exception as e:
        print(e)
        print('error ', id)
        return False
