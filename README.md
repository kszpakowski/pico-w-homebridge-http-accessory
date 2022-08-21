# Raspberry Pico W Homebridge accessory

Micropython implementation of custom https server of homebridge accessory - https://github.com/rudders/homebridge-http#readme

## Homebridge http accessory plugin issues

There are unresolved issues with http plugin, but you can fix it manually on raspberry
Login to raspberry over ssh and edit `/usr/lib/node_modules/homebridge-http/index.js` file.

### Prevent homebridge restart on error

line 47: callback(error) -> done(null)

### Decrease poll interval, so pico can keep up with responding

line 50: interval:300 -> interval:700

## Example plugin configuration

```json
{
     "accessory": "Http",
     "name": "Pico-Dev",
     "service": "Light",
     "http_method": "GET",
     "on_url": "http://192.168.1.206/light/on",
     "off_url": "http://192.168.1.206/light/off",
     "status_url": "http://192.168.1.206/light/status",
     "switchHandling": "realtime",
     "brightness_url": "http://192.168.1.206/light/brightness?value=%b",
     "brightnesslvl_url": "http://192.168.1.206/light/brightness_value",
     "brightnessHandling": "realtime"
}
```

## Testing

You can easily test server implementation using curl e.g. `curl -vvvv http://192.168.1.206/light/on`

## TODO

- describe how to install code on Pico W using Thonny
- describe how to configure Homebridge
- add wiring diagram
- describe how to configure wifi credentials using settings-editor.py
