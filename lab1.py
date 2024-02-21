import sys
from Adafruit_IO import MQTTClient
import random
import time
import cv2
import numpy as np
from keras.models import load_model

# This part can extract to seperated file
model=load_model('keras_model.h5')

camera= cv2.VideoCapture(0)

labels = open('labels.txt','r').readlines()


def image_detector():
    ret,image=camera.read()
    
    image=cv2.resize(image,(224,224),interpolation=cv2.INTER_AREA)
    
    # cv2.imshow('Webcam Image',image)
    
    image=np.asarray(image,dtype=np.float32).reshape(1,224,224,3)
    
    image=(image/127.5)-1
    pro=model.predict(image)
    
    #print(labels[np.argmax(pro)])
    # keyboard = cv2.waitKey(1)
    
    return labels[np.argmax(pro)]


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
counter_ai = 5
previous_result=''
result=''
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
    
    counter_ai-=1
    if counter_ai <=0:
        result=image_detector()
        print(f'AI Output {result}')
        if(previous_result!=result):
            client.publish('ai',result)
            previous_result=result

    time.sleep(1)
    pass