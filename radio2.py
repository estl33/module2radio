import serial
import io
import requests
import vlc
import json
import datetime
import calendar
import time
from time import sleep
def main():
    ser = serial.Serial("/dev/ttyS0", 115200);
    playlists = set(['pls','m3u'])
    Instance = vlc.Instance()
    player = None
    list_player = None
    url = "http://144.217.192.113:8120/mount"
#    url = "http://stream1.chantefrance.com/Chante_France.m3u"
    ext = (url.rpartition(".")[2])[:3]
    if ext in playlists:
        if list_player != None: list_player.stop()
    else:
        if player != None: player.stop()
    test_pass = False
    try:
        if url[:4] == 'file':
            test_pass = True
        else:
            r = requests.get(url, stream=True)
            test_pass = r.ok
    except Exception as e:
        print('failed to get stream: {e}'.format(e=e))
        test_pass = False
    else:
        if test_pass:
            player = Instance.media_player_new()
            Media = Instance.media_new(url)
            Media_list = Instance.media_list_new([url])
            Media.get_mrl()
            player.set_media(Media)
            if ext in playlists:
                list_player = Instance.media_list_player_new()
                list_player.set_media_list(Media_list)
                if list_player.play() == -1:
                    print ("Error playing playlist")
            else:
                if player.play() == -1:
                    print ("Error playing Stream")
        else:
            print('error getting the audio')
    now = datetime.datetime.now()
    print now.strftime("%Y-%m-%d %H:%M")
    print time.time()
    cal = calendar.month(2018,4)
    print "Calendar:"
    print cal
    while 1:
#	r = requests.get("https://api.myjson.com/bins/pdgpr")
#	command = r.content
	command = ser.readline()
	command = command.replace("mssg:","")
        print(command)
	if(command != ''):
		j = json.loads(command)
		status = j['isPlaying']
		station = j['currentStation']
		if station['streamUrl'] != url:
			url = station['streamUrl']
			print(status)
			print(url)
			player = Instance.media_player_new()
	 		Media = Instance.media_new(url)
	  		Media_list = Instance.media_list_new([url])
	      		Media.get_mrl()
       			player.set_media(Instance.media_new(url)) #Media)	
	        if status == True:
	#           list_player.play()
        	    player.play()
 	 	elif status == False:
	#	    list_player.pause()
        	    player.pause()
#	player.play()
if __name__ == "__main__":
    main()

