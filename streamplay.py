from ffpyplayer.player import MediaPlayer
import cv2
import numpy as np
import threading
import libtorrent as lt
import time
import sys
import requests
import re
#music file
#filename='C:\\Users\\龔鈺翔\\01 Lemon.flac'
#filename='C:\\Users\\龔鈺翔\\01 Lemon.flac'


def music(name):
   musicfile=name
   player = MediaPlayer(musicfile)
   val = ''
   while val != 'eof':
      frame, val = player.get_frame()
      if val != 'eof' and frame is not None:
         img, t = frame
         # display img


def video(name):
   

   video_path="C:\\Users\\seank\\"
   video_path=video_path+name
   #video_path="D:\\富江\\國文報告\\個角色簡介\\山本\\比起其他人，我們比較對山本能產生共鳴，.mp3"
   def PlayVideo(video_path):
      video=cv2.VideoCapture(video_path)
      player = MediaPlayer(video_path)
      while True:
         grabbed, frame=video.read()
         audio_frame, val = player.get_frame()
         if not grabbed:
            print("End of video")
            break
         if cv2.waitKey(28) & 0xFF == ord("q"):
            break
         cv2.imshow("Video", frame)
         if val != 'eof' and audio_frame is not None:
            #audio
            img, t = audio_frame
      video.release()
      cv2.destroyAllWindows()
   PlayVideo(video_path)








r = requests.post("http://27f92cdd.ngrok.io", data={'type': 'music'})
link=r.text
print(link)
ses = lt.session()
ses.listen_on(6881, 6891)
params = {'save_path': '.'}

print('1')
ses.add_dht_router("router.utorrent.com", 6881)
ses.add_dht_router("router.bittorrent.com", 6881)
ses.add_dht_router("dht.transmissionbt.com", 6881)

ses.add_dht_router("tracker.opentrackr.org",1337)
ses.add_dht_router("tracker.openbittorrent.com",80)

ses.start_dht()

#link="magnet:?xt=urn:btih:7ac259f4e330d097a7d18b133c10037107943d9b&dn=a&tr=udp%3a%2f%2ftracker.leechers-paradise.org%3a6969&tr=udp%3a%2f%2fp4p.arenabg.com%3a1337%2fannounce&tr=http%3a%2f%2f54.39.98.124%3a80%2fannounce&tr=udp%3a%2f%2f140.115.152.14%3a2255&tr=udp%3a%2f%2ftracker.coppersurfer.tk%3a6969&tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337&tr=udp%3a%2f%2fopen.stealth.si%3a80&tr=udp%3a%2f%2ftracker.publicbt.com%3a80"
#link = "magnet:?xt=urn:btih:ff5474fa8b1554e3401077e185fb314c0473e6c7&dn=Kimi+no+Na+wa+%28Your+Name%29+HDrip+720p+aac+x264+English+hardsub&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&tr=udp%3A%2F%2Ftracker.ccc.de%3A80"
#link = "magnet:?xt=urn:btih:9fe8d477e2fa4245a6b3911d5ed7d18cb7510853&dn=Call+Me+By+Your+Name+2017+DVDSCR+X264+CataVentos%5BEtMovies%5D&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&tr=udp%3A%2F%2Ftracker.ccc.de%3A80"
h = lt.add_magnet_uri(ses, link, params)
h.set_sequential_download(1)
print('start try')
while (not h.has_metadata()):
    print('can\'t find')
    time.sleep(1)
    

torinfo = h.get_torrent_info()
for x in range(torinfo.files().num_files()):
   print(x,torinfo.files().file_path(x))
fileIndex=int(input("which one to play?"))
filename=torinfo.files().file_path(fileIndex)

if filename.endswith(".flac") or filename.endswith('.mp3'):
   thread2 = threading.Thread(target=music,args=(filename,))
   thread2.setDaemon(True)
elif filename.endswith('.mp4') or filename.endswith('.mkv'):
   thread2 = threading.Thread(target = video, args=(filename,))
   thread2.setDaemon(True)
i=0
for f in torinfo.files():
    if fileIndex == i:
        fileStr = f
        break
    i += 1
print (fileStr.path)
h = ses.add_torrent(torinfo,'.')

pr = torinfo.map_file(fileIndex,0,fileStr.size)
n_pieces = int(pr.length / torinfo.piece_length()) + 1 
print(n_pieces)
for i in range(torinfo.num_pieces()):
   if i in range(pr.piece,pr.piece+n_pieces):
        h.piece_priority(i,7)
   else:
      h.piece_priority(i,0)
s = h.status()
print(s.total_wanted)
while (s.progress * 100<(1000000 / s.total_wanted)):
   s = h.status()

   state_str = ['queued', 'checking', 'downloading metadata', \
    'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
   #print (s.download_rate)
   print ('%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
         (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
         s.num_peers, state_str[s.state]))

   if s.progress>=1:
      break

   time.sleep(1)
print('predownload finish!')
try:
   thread2.start()
except :
   pass


while (not h.is_seed()):
   s = h.status()

   state_str = ['queued', 'checking', 'downloading metadata', \
    'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
   #print (s.download_rate)
   print ('%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
         (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
         s.num_peers, state_str[s.state]))

   if s.progress>=1:
      break

   time.sleep(1)
while True:
   try:
      pass


   except KeyboardInterrupt:
      print('stop')
      break
print('play complete')




'''
for x in range(torinfo.files().num_files()):
   print(x,torinfo.files().file_path(x))
i=int(input("which one to play?"))


filename=torinfo.files().file_path(i)
#h = ses.add_torrent({'ti': torinfo, 'save_path': './'})
print('starting', h.name())
if filename.endswith(".flac") or filename.endswith('.mp3'):
   thread2 = threading.Thread(target=music,args=(filename,))
   thread2.setDaemon(True)
elif filename.endswith('.mp4') or filename.endswith('.mkv'):
   thread2 = threading.Thread(target = video, args=(filename,))
   thread2.setDaemon(True)
#thread2 = threading.Thread(target = video, args=(filename,))
#thread2.setDaemon(True)
#predownload
s = h.status()

while(s.progress * 100<2):
   s = h.status()

   state_str = ['queued', 'checking', 'downloading metadata', \
      'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
   print ('\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
      (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
      s.num_peers, state_str[s.state]),)
   sys.stdout.flush()

   time.sleep(0.5)

print("start")
try:
   thread2.start()
except expression as identifier:
   pass

while (not h.is_seed()):
   s = h.status()

   state_str = ['queued', 'checking', 'downloading metadata', \
      'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
   print ('\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
      (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
      s.num_peers, state_str[s.state]),)
   sys.stdout.flush()

   time.sleep(0.5)

print(h.name(), 'complete')
#thread2.join()
while True:
   try:
      pass


   except KeyboardInterrupt:
      print('stop')
      break
print('play complete')

'''
