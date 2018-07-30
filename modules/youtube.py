import pafy
import re
import os

def download_video(id):
  video = pafy.new("https://www.youtube.com/watch?v={}".format(id))
  print('downlowding', video.title, id)
  # title = res['snippet']['title']
  # thumbnail = res['snippet']['thumbnails']['standard']['url']
  # duration = res['contentDetails']['duration'][2:]
  # print(str(idx+1),title,duration,thumbnail)

  # get download the video and get status
  os.system('wget -q {} -O /tmp/{}.jpg'.format(video.bigthumbhd,id))
  status = os.system('youtube-dl -q -f 18,36 --max-filesize 45m --output "/tmp/%(id)s.mp4"  -- {}'.format(id))
  if status != 0:
    return False
  video.thumbPath = '/tmp/' + id + '.jpg'
  video.videoPath = '/tmp/' + id + '.mp4'
  return video

def isValidYtUrl(string):
  match = re.match(r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+', string)
  return match

def idFromYtUrl(url):
  regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')
  match = regex.match(url)
  if not match:
      print('no match')
  print(match.group('id'))
  return match.group('id')

if __name__ == '__main__':
  idFromYtUrl('https://www.youtube.com/watch?v=xI99blNzaKs')
