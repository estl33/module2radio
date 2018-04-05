
import serial
import io
import requests
import vlc
import json
import datetime
import calendar
import time
from time import sleep
import websocket
from PIL import Image
try:
    import thread
except ImportError:
    import _thread as thread

ser = serial.Serial("/dev/ttyS0", 115200);
playlists = set(['pls','m3u'])
Instance = vlc.Instance()
player = None
list_player = None
url = "http://174.37.159.206:8262/stream"
ext = (url.rpartition(".")[2])[:3]
if ext in playlists:
    if list_player != None: list_player.stop()
else:
    if player != None: 
	player.stop()
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
            print 'test passed'
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
    ftime = str(now.strftime("%Y-%m-%d %H:%M"))
    ser.write('time: '+ ftime + '\n')
   	
def on_message(ws, command):
		ftime = str(now.strftime("%Y-%m-%d %H:%M"))
		ser.write('time: ' + ftime + '\n')
		
		global url
		global Media
		global player
		global Instance
		print(command)
		if(command != ''):
		    j = json.loads(command)
		    data = {}
		    status = int(j['isPlaying'] == True)
		    data['status'] = status
		    volume = j['currentVolume']
		    data['volume'] = volume
		    song = j['currentSong']
		    data['artist'] = song['name']
		    data['title'] = song['title']
		    station = j['currentStation']
		    data['stationName'] = station['name']
		    data['genre'] = station['genre']
		    country = station['country']
		    data['country'] = country['name']
		    print(data)
		    delimString = ''
		    for key, value in data.iteritems():
			delimString += key + ':' + str(value) + '\n'
		    delimSTring = delimString[:-1]
		    print(delimString)
		    json_data = json.dumps(data)
		    print(json_data)
		    
		    ser.write(delimString)
		    ser.write('\n')
		    
		    if j['currentStreamUrl'] != url:
			player.stop()
			url = j['currentStreamUrl']
			print(status)
			print(url)
			
		#	player = vlc.MediaPlayer(vlc.Instance("--video-filter=invert"))
		#	player.set_mrl(sys.argv[1])

			player = Instance.media_player_new()
	 		Media = Instance.media_new(url)
	  		Media_list = Instance.media_list_new([url])
	      		Media.get_mrl()
       			player.set_media(Instance.media_new(url))
	        	song = j['currentSong']
		
			imUrl = song['imageUrl']
			if (imUrl != ''): 
				imageColor(imUrl)
			#player.play()
		    if status == True:
	       	        player.play()
 	 	    #	player.audio_set_volume(volume)
		    elif status == False:
	       	        player.stop()

def on_error(ws, error):
	print(error)

def on_close(ws):
	print("### closed /###")
		
websocket.enableTrace(True)
ws = websocket.WebSocketApp("ws://ec2-54-201-183-2.us-west-2.compute.amazonaws.com:8080/sock",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
ws.run_forever()	


def imageColor(url):
	NUM_CLUSTERS = 5

	print 'reading image'
	#im = Image.open(urllib.urlopen('https://lastfm-img2.akamaized.net/i/u//300x300/32db4097dab14019c084f5c5514337f1.png'))
	im = Image.open(urllib.urlopen(url))

	im = im.resize((100, 100))      
	ar = np.asarray(im)
	shape = ar.shape
	ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

	print 'finding clusters'
	codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)

	vecs, dist = scipy.cluster.vq.vq(ar, codes)         
	counts, bins = scipy.histogram(vecs, len(codes))    

	index_max = scipy.argmax(counts)                    # find most frequent
	peak = codes[index_max]
	colour = ''.join(chr(int(c)) for c in peak).encode('hex')

        print 'most frequent colour: (#%s)' % (colour)

