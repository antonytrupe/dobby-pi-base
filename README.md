Python NodeJS module that runs on the raspberrypi and reads from jeenode connected on usb serial port  

**Other Projects**  
| project name | description | language/framework |
| - | - | - |
| [dobby-jeenode-base](//github.com/antonytrupe/dobby-jeenode-base) | collect local and remote temp/rh/etc data and send to dobby-pi-base over usb/serial | c++/arudiuno |
| [dobby-jeenode-remote](//github.com/antonytrupe/dobby-jeenode-remote) | collect local temp/rh and send to dobby-jeenode-base over radio | c++/arduino |
| [dobby-pi-base](//github.com/antonytrupe/dobby-pi-base) (THIS) | read from jeenode board over usb/serial | python/nodejs module |
| [MMM-IndoorTemp](//github.com/antonytrupe/MMM-IndoorTemp) | mm module for temp/rh | javascript/nodejs module/MM module |
| [dobby-cloud-sync](//github.com/antonytrupe/dobby-cloud-sync) | sync to google sheets | javascript/nodejs module |
| [dobby-speedtest](//github.com/antonytrupe/dobby-speedtest) | collect internet speedtest data | python/nodejs module |
| MMM-InternetStatus | display internet speedtest results | javascript/nodejs module/MM module |


npm install -g node-gyp  
npm install electron-rebuild  
./node_modules/.bin/electron-rebuild -w sqlite3 -p  

get a list of usb devices
lsusb
