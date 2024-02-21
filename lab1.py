import sys
from Adafruit_IO import MQTTClient
import random
import time

AIO_FEED_ID = ['nutnhan1','nutnhan2']
ADAFRUIT_IO_USERNAME = "thanhthien412"
ADAFRUIT_IO_KEY = "aio_uguT767kjg6Fsfv9WRoOBavNMa57"

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_ID:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload + f'feed id : {feed_id}')

client = MQTTClient(ADAFRUIT_IO_USERNAME , ADAFRUIT_IO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background() # for_blocking  (stop in heres)

counter=10
sensor_type=0

while True:
    counter=counter-1
    if counter<=0:
        counter=10
        print('Random data is publishing')
        if sensor_type==0:
            temp=random.randint(40,60)
            print('Temperature....')
            client.publish('cambien1',temp)
            sensor_type=1
        elif sensor_type==1:
            humi=random.randint(50,70)
            print('Humnity....')
            client.publish('cambien2',humi)
            sensor_type=2
        else:
            light=random.randint(20,100)
            print('Lightning....')
            client.publish('cambien3',light)
            sensor_type=0
    time.sleep(1)
    pass