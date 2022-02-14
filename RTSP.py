import cv2
import os

# cap = cv2.VideoCapture('rtsp://[username]:[password]@[IP]:554/Streaming/Channels/1/')
RTSP_URL = ''

"""
Windows
"""
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
