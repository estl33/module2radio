station_cfg={}

station_cfg.ssid="abcdefg"
station_cfg.pwd=""

wifi.setmode(wifi.STATION)
wifi.sta.config(station_cfg)
wifi.sta.autoconnect(1)


tmr.delay(1000000)

-- This should print 5 if connection was successful
print(wifi.sta.status())
-- Prints the IP given to ESP8266
print(wifi.sta.getip())

-- Unfortunately, the Wi-FI dongle can only make unsecured HTTP requests, but Twilio requires 
-- secured HTTPS requests, so we will use a relay website to convert HTTP requests into HTTPS requests

SONG_HOST = "requestbin.fullcontact.com"
SONG_URI = "/11m0nmr1"
HOST = "ec2-54-201-183-2.us-west-2.compute.amazonaws.com"
URI = "/stream"

-------------------------------------------------------------------------------------------------------------------------------------
function build_post_request(host, uri, data_table)

      data = [[{
  "isPlaying": true,
  "currentStream": "5ac3cf45ea869483719d8eb8",
  "currentVolume": 5
}]]
     request = "POST "..uri.." HTTP/1.1\r\n"..
     "Host: "..host.."\r\n"..
  --   "Connection: close\r\n"..
     "Content-Type: application/json\r\n"..
     --"Content-Length: "..data:len().."\r\n"..
     "User-Agent: de1\r\n"..
     "userId: 5ac3cf9f8ac834137ba00c3b\r\n"..
     "\r\n"..
     data.."\r\n"
     
     print(request)
     return request
end

local function display(sck,response)
     print(response)
end

function send_info(isPlayingVal, streamId, streamVol)

     data = {
      isPlaying = isPlayingVal,
      currentStream = streamId,
      currentVolume = streamVol
     }

     socket = net.createConnection(net.TCP,0)
     socket:on("receive",display) 

     socket:on("connection",function(sck)
		  --isPlayingVal, streamId, streamVol)
          post_request = build_post_request(HOST,URI,data)
          sck:send(post_request)
     end)

     --change to 8080 for cloud server
     socket:connect(8080,HOST)
end

function check_stream(isPlayingVal, currentStreamVal)
    ip = wifi.sta.getip()

    if(ip==nil) then
        print("Connecting...")
    else
    tmr.stop(0)
    print("Connected to AP!")
    print(ip)
    send_info(isPlayingVal, currentStreamVal)
    gpio.mode(3, gpio.OUTPUT)
    gpio.write(3, gpio.LOW)
 end
end
----------------------------------------------------------------------------------------------------------------------------------------
function socket_setup(isPlayingVal, stationId, userId, volumeVal)

    data = isPlayingVal..','..stationId..','..volumeVal
    local ws = websocket.createClient()
    
    ws:config({headers={['UserId']= userId..'DE1'}})

    ws:connect('ws://ec2-54-201-183-2.us-west-2.compute.amazonaws.com:8080/sock')

        
    ws:on("connection", function()
        print('server:  ws conn!')
        ws:send(data)
    end)
    
    ws:on("receive", function(__,msg, __) --opcode,_)
      print('mssg:',msg, '\r\n')--'\r\n') -- opcode is 1 for text message, 2 for binary      
    end)
    -- '{"isPlaying":true,"currentPlaying":"5aab770ab359b46a78887497"}'
   
    ws:on("close", function(_, status)
       print('server:  connection closed', status)
       ws = nil 
   end)
    
end


function post_to_server(isPlaying, streamId, userId, volumeVal)
	srv = net.createConnection(net.TCP, 0)
	srv:on("receive", function(sck, c) print('answer',c) end)
	-- Wait for connection before sending.
	srv:on("connection", function(sck, c)

	sck:send("GET /stream/"..isPlaying.."/"..streamId.."/"..volumeVal.." HTTP/1.1\r\nHost: ec2-54-201-183-2.us-west-2.compute.amazonaws.com\r\nConnection: close\r\nAccept: */*\r\nUser-Agent: de1\r\nuserId:".. userId.."\r\n\r\n")
	end)

	srv:connect(8080,"ec2-54-201-183-2.us-west-2.compute.amazonaws.com")
end
----------------------------------------------------------------------------------------------------------------------

function url_get(url)
    http.get(url, nil, function(code, data)
    if (code < 0) then
      print("HTTP request failed")
    else
      print(code, data)
    end
  end)
end

function url_post(url)
   data =  '{"isPlaying":true,"currentStream":123}'
   --Content-Length:'..data:len()..'
      
    http.post('http://'..HOST..URI,'userId: 123\r\n',data,--Content-Type: application/json\nContent-Length:'..data:len()..'\r\n',data,--'{"hello":"world"}',
    function(code, data)
    if (code < 0) then
      print("HTTP request failed")
    else
      print(code, data)
      print("success")
    end
  end)
end

function wifi_connect(id, password)
	station_cfg={}
	--station_cfg.ssid="Koodo LTE"
	--station_cfg.pwd="bumblebee"
	station_cfg.ssid = id
	station_cfg.pwd = password

	-- configure ESP as a station
	wifi.setmode(wifi.STATION)
	wifi.sta.config(station_cfg)
	wifi.sta.autoconnect(1)

	tmr.delay(1000000)

	-- This should print 5 if connection was successful
	print(wifi.sta.status())
	-- Prints the IP given to ESP8266
	print(wifi.sta.getip())

	gpio.mode(3, gpio.OUTPUT)
	gpio.write(3, gpio.LOW)
end
