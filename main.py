import network
import socket
import time

import request_handler as rh
import http_req_parser as rp
from lights import PwmLight
from settings import Settings


from machine import Pin
import uasyncio as asyncio

debug = True

onboard_led = Pin('LED', Pin.OUT)
light = PwmLight(4)
settings = Settings('wifi.dat').get_settings()

def connect_to_network(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140)
        
    wlan.connect(ssid,password)

    max_wait = 30
    for _ in range(0,max_wait):
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        print('waiting for connection...')
        onboard_led.toggle()
        time.sleep(0.3)

    if wlan.status() != 3:
        led.value(1)
        raise RuntimeError('network connection failed, error code: ' + str(wlan.status()))
    else:
        status = wlan.ifconfig()
        print('connected, ip = ' + status[0])
        onboard_led.value(0)


"""
"on_url": "http://192.168.1.206/light/on"
"""
@rh.request_handler('/light/on')
def turn_on(req):
    light.turn_on()
    
"""
"off_url": "http://192.168.1.206/light/off"
"""
@rh.request_handler('/light/off')
def turn_off(req):
    light.turn_off()

"""
"status_url": "http://192.168.1.206/light/status",
"""
@rh.request_handler('/light/status')
def get_status(req):
    return 1 if light.is_on else 0

"""
"brightnesslvl_url": "http://192.168.1.206/light/brightness_value"
"""
@rh.request_handler('/light/brightness_value')
def get_brightness(req):
    return light.brightness

"""
"brightness_url": "http://192.168.1.206/light/brightness?value=2"
"""
@rh.request_handler('/light/brightness')
def set_brightness(req):
    brightness = int(req["params"]["value"])
    light.set_brightness(brightness)
    


async def serve_client(reader, writer):
    request_line = str(await reader.readline()) # TODO read all request lines
    
    while await reader.readline() != b"\r\n": # Without this writer.wait_closed doesn't work
        pass
    
    try:
        req = rp.parse_raw_request(request_line)
        print(f"Handling request {req} using {len(rh.request_handlers)} registerd handlers")
        for handler in rh.request_handlers: # TODO sort handlers by uri length descending, to prioritize more precise matchers
            result = handler(req)
            if result is not None: # TODO extract into response mapper
                # TOOD if result error is not none, respond with error
                writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                data = result["result"]
                if data is not None:
                    writer.write(str(data)+'\r\n')
                break
                
#    except Exception as e:
#        print("Error " + str(e))
#        writer.write('HTTP/1.0 500 OK\r\nContent-type: text/html\r\n\r\nUnknown server error')
    finally:
        await writer.drain()
        await writer.wait_closed()
    

async def main():
    print("Connecting to network")
    connect_to_network(settings['ssid'], settings['pass'])
    
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0",80))

    while True:
        onboard_led.value(1)
        await asyncio.sleep(.1)
        onboard_led.value(0)
        await asyncio.sleep(2)

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
