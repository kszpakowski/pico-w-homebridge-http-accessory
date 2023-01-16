import network
import socket
from machine import Pin
onboard_led = Pin('LED', Pin.OUT)

## TODO implement reconnect

from settings import Settings

settings = Settings('wifi.dat').get_settings()
ap = network.WLAN(network.AP_IF)
sta = network.WLAN(network.STA_IF)
html = ""

with open('index.html') as f:
    lines = f.read()
    html = str(lines)



def getNetworks():
    sta.active(True)
    return set(ssid.decode('utf-8') for ssid, *_ in sta.scan())

def checkConnection():
    pass

def startAccessPoint():
    ap.config(ssid='Homebrige accessory',security=0)
    ap.active(True)

    while ap.active() == False:
      pass

    print('AP started')
    print(ap.ifconfig())

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    try:
      s.bind(addr)
      s.listen(1)
    except:
      print("Error during socket binding")
    
    while True:
        try:
            cl, addr = s.accept()
            print('client connected from', addr)
            request = cl.recv(1024)
            print(request)

            networks = getNetworks()
            options = ''.join(f"<option>{network}</option>" for network in networks if network)
            rendered = html.replace("{{options}}", options)
            # print(rendered)
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(rendered)
            cl.close()
            onboard_led.toggle()


        except OSError as e:
            cl.close()
            print('connection closed')

    
    
    #ap.active(False)

def connect():
    ssid = settings['ssid']
    password = settings['pass']
    print(f'Connecgting to: {ssid}')

# if(ssid):
#     connect()

startAccessPoint()