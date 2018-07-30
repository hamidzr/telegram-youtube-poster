import pafy
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


