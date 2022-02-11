import cv2
import os

# cap = cv2.VideoCapture('rtsp://[username]:[password]@[IP]:554/Streaming/Channels/1/')
RTSP_URL = 'rtsp://admin:Ustudy101@10.200.11.4:554/ISAPI/Streaming/Channels/101'

os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'

cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)

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
