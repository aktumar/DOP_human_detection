import cv2
import os
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")

SYSTEM = '151'
USERNAME = config[SYSTEM]["USERNAME"]
PASSWORD = config[SYSTEM]["PASSWORD"]
IP_ADDRESS = config[SYSTEM]["IP_ADDRESS"]
PORT = config[SYSTEM]["PORT"]
DIR = config[SYSTEM]["DIR"]
COMPUTER = config[SYSTEM]["COMPUTER"]

# cap = cv2.VideoCapture('rtsp://[username]:[password]@[IP]:554/Streaming/Channels/1/')
RTSP_URL = f'rtsp://{USERNAME}:{PASSWORD}@{IP_ADDRESS}:{PORT}/{DIR}/Streaming/Channels/{COMPUTER}'

"""
Windows
"""
# os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
# cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)


"""
Ubuntu
"""
cap = cv2.VideoCapture(RTSP_URL)

if not cap.isOpened():
    print('Cannot open RTSP stream')
    exit(-1)

while True:
    _, frame = cap.read()
    cv2.imshow('RTSP stream', frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
