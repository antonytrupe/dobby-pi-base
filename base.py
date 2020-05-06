import serial
import json
import threading
import subprocess
import sqlite3 as lite
from datetime import datetime


def initDB(databaseName):
    con = lite.connect(databaseName)
    c = con.cursor()
            
    #get the count of tables with the name
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND (name='historicdata' or name='currentdata') ''')
    #print('foo')
    #print(c.fetchone()[0])
    #if the count is 1, then table exists
    if c.fetchone()[0] == 2 :
        print('dobby-pi-base: tables exist')
        None
    
    else :
        c.execute('''CREATE TABLE IF NOT EXISTS historicdata (
                        location text NOT NULL,
                        attribute text not null,
                        value text,
                        datetime text not null);''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS currentdata (
                        location text NOT NULL,
                        attribute text not null,
                        value text,
                        datetime text not null,
                        primary key (location,attribute));''')

def pollUSB(con):
    print('dobby-pi-base:usb polling starting...')
    con = lite.connect(databaseName)
    #TODO move this to config file
    USBPORT="/dev/ttyUSB0"
    #TODO catch SerialException error and log it
    serialport = serial.Serial(port=USBPORT, baudrate=9600, timeout=0.5)
    while True:
        try:
            #{"location":"living room","rh": 49.4}]
            command = serialport.readline()
            if command:
                #print('command:'+command.rstrip().decode('UTF-8').replace("'","\""))
                data=json.loads(command.rstrip().decode('UTF-8').replace("'","\""))
                #print('encoded:')
                #print(data)
                with con:

                    cur = con.cursor()
                    #print('about to insert')
                    #TODO mark old records not active
                    cur.execute("insert into historicdata (location,attribute,value,datetime) "+
                                "values (:location,:attribute,:value,:datetime)",
                                {"location":data[0]["location"],
                                 "attribute":data[0]["attribute"],
                                 "value":data[0]["value"],
                                 "datetime":datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    #print('inserted historical value')
                    #print('updating current value')
                    cur.execute("insert into currentdata (location,attribute,value,datetime) "+
                                "values (:location,:attribute,:value,:datetime) "+
                                "on conflict(location,attribute) do update set value=excluded.value, datetime=excluded.datetime",
                                {"location":data[0]["location"],
                                 "attribute":data[0]["attribute"],
                                 "value":data[0]["value"],
                                 "datetime":datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    #print('updated current value')
        except serial.SerialException as e:
            #usb got unplugged
            print('serial.SerialException:')
            print(e)
        except json.JSONDecodeError as e:
            print('serial.JSONDecodeError:')
            print(e)
            print(command)
        except Exception as e:
            print('Exception:')
            print(e)
            
def speedTest():
    print('starting speedtest...')
    response = subprocess.Popen('/usr/local/bin/speedtest-cli --json --server 29204', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    print(response)
    data=json.loads(response.rstrip().replace("'","\""))
    print('{},{},{}'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),data["client"]["lat"],data["client"]["lon"]))

if __name__ == "__main__":
#todo move file path to configuration
    databaseName="test.db"
    initDB(databaseName)
    thread1 = threading.Thread(target=pollUSB, args=(databaseName,))
    thread1.start()
    #speedTest()