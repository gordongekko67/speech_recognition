import pyautogui
import speech_recognition as sr
from PIL.Image import Image
from imageai.Detection import ObjectDetection
import os
import shutil
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import numpy as np

import paho.mqtt.client as mqtt
import time

# referenze libreria: https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst#speech-recognition-library-reference

recognizer_instance = sr.Recognizer() # Crea una istanza del recognizer

text = ""

def on_connect(client, userdata, flags, rc):
    print("connected with code "+ str(rc))
    # substrice topic
    client.subscribe("Topic/#")

def on_message(client, userdata, msg):
    print(str(msg.payload))

def avanti():
    print("robot avanti")

def elaborazione():
    
    execution_path = os.getcwd()
    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path, "opencv0.png"),
                                                 output_image_path=os.path.join(execution_path, "imagenew.jpg"))
    for eachObject in detections:
        print(eachObject["name"], " : ", eachObject["percentage_probability"])


    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set("fkjqkoul", "wK0aUWpQWS35")
    client.connect("tailor.cloudmqtt.com", 16434, 60)
    client.publish("Tutorial2", "Connesso a MQTT")


    time.sleep(2)
    while True:
        for eachObject in detections:
            payload1 = str(eachObject["name"])
            payload2 = " : "
            payload3 = str(eachObject["percentage_probability"])
            payload = payload1 + payload2 + payload3
            client.publish("Tutorial2", payload)
            time.sleep(2)

    client.loop_stop()
    client.disconnect()

def riconosciimmagine():
    camera = cv2.VideoCapture(0)
    for i in range(1):
        return_value, image = camera.read()
        cv2.imwrite('opencv' + str(i) + '.png', image)
        elaborazione()

def indietro():
    print("robot indietro")
    riconosciimmagine()

while(text != "esci"):
    with sr.Microphone() as source:
        recognizer_instance.adjust_for_ambient_noise(source)
        print("Sono in ascolto... parla pure!")
        audio = recognizer_instance.listen(source)
        print("Ok! sto ora elaborando il messaggio!")
    try:
        text = recognizer_instance.recognize_google(audio, language="it-IT")
        print("Google ha capito: \n", text)
        if (text == "esci"):
             break
        if (text =="avanti"):
            avanti()
        if (text =="indietro"):
            indietro()
    except Exception as e:
         print(e)