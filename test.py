from pytube import Playlist
from pytube import YouTube

playlist = Playlist('https://www.youtube.com/playlist?list=PLDV1Zeh2NRsAWrxWRTHJrsgBrbwqGzt-z')

for video in playlist.videos:
    print('downloading : {} with url : {}'.format(video.title, video.watch_url))
    # In medium-low quality
    # YouTube(video.watch_url).streams.first().download("D:/")
    # In high quality
    YouTube(video.watch_url).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download("D:/")
