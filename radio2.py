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
    url = '' #http://144.217.192.113:8120/mount"
 #   url = "http://stream1.chantefrance.com/Chante_France.m3u"
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
    #ser.write(time.time())
    cal = calendar.month(2018,4)
    print "Calendar:"
    print cal
    headers = {
    "User-Agent": "de1",
    "userId": "5ac3cf9f8ac834137ba00c3b"
    }
    while 1:
	print("In while loop")
#	r = requests.get("https://api.myjson.com/bins/pdgpr")
#	command = r.content
	r = requests.get("http://ec2-54-201-183-2.us-west-2.compute.amazonaws.com:8080/stream",headers=headers)
	command = r.content
#	command = ser.readline()
	print("We got here!")
	command = command.replace("mssg:","")
        print(command)
	if(command != ''):
		j = json.loads(command)
		status = j['isPlaying']
		if j['currentStreamUrl'] != url:
			url = j['currentStreamUrl']
			print(status)
			print(url)
			player = Instance.media_player_new()
	 		Media = Instance.media_new(url)
	  		Media_list = Instance.media_list_new([url])
	      		Media.get_mrl()
       			player.set_media(Instance.media_new(url)) #Media)	
	        	song = j['currentSong']
		#	imUrl = song['imageUrl']
		#	if (imUrl != ''): 
		#		imageColor(imUrl)
		if status == True:
	#           list_player.play()
        	    player.play()
 	 	elif status == False:
	#	    list_player.pause()
        	    player.pause()
#	player.play()



def imageColor(url):
	NUM_CLUSTERS = 5

	print 'reading image'
	#im = Image.open(urllib.urlopen('https://lastfm-img2.akamaized.net/i/u//300x300/32db4097dab14019c084f5c5514337f1.png'))
	im = Image.open(urllib.urlopen('https://static1.squarespace.com/static/588bab1086e6c0ffe0e62b3a/588bbb3459cc68c61c882d1c/588de2009f74563ea54ab42c/1485693441134/light+blue.jpg?format=500w'))

	im = im.resize((100, 100))      # optional, to reduce time
	ar = np.asarray(im)
	shape = ar.shape
	ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

	print 'finding clusters'
	codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
	#print 'cluster centres:\n', codes

	vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
	counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

	index_max = scipy.argmax(counts)                    # find most frequent
	peak = codes[index_max]
	colour = ''.join(chr(int(c)) for c in peak).encode('hex')

        print 'most frequent colour: (#%s)' % (colour)
#	print 'most frequent is %s (#%s)' % (peak, colour)

if __name__ == "__main__":
    main()

