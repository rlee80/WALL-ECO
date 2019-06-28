#https://devpost.com/software/wall-eco/
import cv2
import requests
import time
import json
import pigpio
import sys
import RPi.GPIO as GPIO

camera_port = 0
ramp_frames = 30

image_url = "http://ambulo.serveo.net/image/img.jpg"
auth = ('apikey', 'hSjAEiuBeXWx6JsfEemY54LHZUw1QX84KC21vWtdRTC3')
ip = "http://64.187.241.17:5000/image_proc"
imgsrc = "/home/pi/Downloads/images/img.jpg"

pi = pigpio.pi()
pi.set_mode(18, pigpio.OUTPUT)
pi.set_mode(4, pigpio.OUTPUT)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(19,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)

print("TrashTalker Started")
camera = cv2.VideoCapture(camera_port)

print("Green LED Flash = Recyclable")
print("Red LED Flash = Nonrecyclable")

def greenLightOn():
    GPIO.setup(19,GPIO.OUT)
    GPIO.output(19,GPIO.LOW)

def greenLightOff():
    GPIO.output(19,GPIO.HIGH)

def redLightOn():
    GPIO.setup(13,GPIO.OUT)
    GPIO.output(13,GPIO.LOW)

def redLightOff():
    GPIO.output(13,GPIO.HIGH)

def wave():
    pi.set_servo_pulsewidth(4, 2000)
    time.sleep(1)
    pi.set_servo_pulsewidth(4, 1500)
    time.sleep(1)
    pi.set_servo_pulsewidth(4, 1000)
    
def get_image ():
    retval, im = camera.read()
    return im
x = 0;

try:
    while 1==1:
        GPIO.output(13,GPIO.HIGH)
        GPIO.output(19,GPIO.HIGH)
        GPIO.output(26,GPIO.HIGH)
        for i in range(ramp_frames):
            temp = get_image()
        print("Taking Picture")
        camera_capture = get_image()

        print("Saving Picture")
        file = imgsrc
        cv2.imwrite(file, camera_capture)
        params = {"image": open(file, 'rb')}
        url = "http://ambulo.serveo.net/upload"
        r = requests.get(url, files=params)
        print(r.text)
        rj = json.loads(r.text)
        image_url = rj['url']
        url = "http://gateway.watsonplatform.net/visual-recognition/api/v3/classify?version=2018-03-19&url={}".format(image_url)


        print("Analyzing Picture")
        r = requests.get(url, auth=auth)
        print("Displaying Output")
        data = json.loads(r.text)
        print(data)
        print("Potential Item:");

        try:
            for c in data['images'][0]['classifiers'][0]['classes']:
                print(c['class'])

                if c['class'] == "beverage" or c['class'] == "water" or c['class'] == "can":
                    print("Item is recyclable - Rotating Servo")
                    greenLightOn()
                    wave()
                    pi.set_servo_pulsewidth(18, 1000)
                    time.sleep(2)
                    pi.set_servo_pulsewidth(18, 1500)
                    pi.set_servo_pulsewidth(18, 1750)
                    greenLightOff()
                    time.sleep(2)
                    break
                elif c['class'] == "candy" or c['class'] == "bag" or c['class'] == "nutrition" or c['class'] == "sweet" or c['class'] == "sweets" or c['class'] == "wrapping" or c['class'] == "wrapper":
                    print("Item is nonrecyclable - Rotating Servo")
                    redLightOn()
                    pi.set_servo_pulsewidth(18, 2000)
                    time.sleep(2)
                    pi.set_servo_pulsewidth(18, 1500)
                    pi.set_servo_pulsewidth(18, 1750)
                    redLightOff()
                    time.sleep(2)
                    break
                elif c['class'] == "cardboard":
                    time.sleep(3)
                    break; 
        except json.decoder.JSONDecodeError:
            print("No Item Found")
except KeyboardInterrupt:
    pi.set_servo_pulsewidth(18, 0)                  
    pi.set_servo_pulsewidth(4, 0)