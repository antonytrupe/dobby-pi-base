import serial
import json
import sqlite3 as lite
from datetime import datetime

#print("hello world")
#i=''' [{"room":"living room","t":44.5,"rh":28}] '''
#j=json.loads(i)
#print(len(j))
#print(j)
#quit()

con = lite.connect('test.db')

def init():
    c = con.cursor()
            
    #get the count of tables with the name
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND (name='historicdata' or name='currentdata') ''')
    print('foo')
    #print(c.fetchone()[0])
    #if the count is 1, then table exists
    if c.fetchone()[0] == 2 :
        #print('Table exists.')
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


init()
#TODO move this to config file
USBPORT="/dev/ttyUSB0"
#TODO catch SerialException error and log it
serialport = serial.Serial(port=USBPORT, baudrate=9600, timeout=0.5)

while True:
    try:
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
                #temp
                cur.execute("insert into historicdata (location,attribute,value,datetime) "+
                            "values (:location,:attribute,:value,:datetime)",
                            {"location":data[0]["location"],
                             "attribute":"tempC",
                             "value":data[0]["t"],
                             "datetime":datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                #relative humidity
                cur.execute("insert into historicdata (location,attribute,value,datetime) "+
                            "values (:location,:attribute,:value,:datetime)",
                            {"location":data[0]["location"],
                             "attribute":"rh",
                             "value":data[0]["rh"],
                             "datetime":datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                
                #current data upserts
                cur.execute("insert into currentdata (location,attribute,value,datetime) "+
                            "values (:location,:attribute,:value,:datetime) on conflict(location,attribute) do update set value=excluded.value, datetime=excluded.datetime",
                             {"location":data[0]["location"],
                              "attribute":"tempC",
                              "value":data[0]["t"],
                              "datetime":datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

                cur.execute("insert into currentdata (location,attribute,value,datetime) "+
                            "values (:location,:attribute,:value,:datetime) "+
                            "on conflict(location,attribute) do update set value=excluded.value, datetime=excluded.datetime",
                            {"location":data[0]["location"],
                             "attribute":"rh",
                             "value":data[0]["rh"],
                             "datetime":datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

    except serial.SerialException as e:
        #usb got unplugged
        pass
    except Exception as e:
        print('e:')
        print(e)
        pass