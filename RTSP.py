import os
import cv2
import numpy as np
import configparser
from sys import platform

"""
OS platform
"""
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

if platform == "linux" or platform == "linux2":
    apiPreference = None
elif platform == "win32":
    apiPreference = cv2.CAP_FFMPEG

"""
Camera configuration
"""
config = (configparser.ConfigParser())
config.read("settings.ini")

SYSTEM = '155'
USERNAME = config[SYSTEM]["USERNAME"]
PASSWORD = config[SYSTEM]["PASSWORD"]
IP_ADDRESS = config[SYSTEM]["IP_ADDRESS"]
PORT = config[SYSTEM]["PORT"]
DIR = config[SYSTEM]["DIR"]
COMPUTER = config[SYSTEM]["COMPUTER"]

RTSP_URL = f'rtsp://{USERNAME}:{PASSWORD}@{IP_ADDRESS}:{PORT}/{DIR}/Streaming/Channels/{COMPUTER}'

"""
Open video streaming
"""
cap = cv2.VideoCapture(RTSP_URL, apiPreference)

if not cap.isOpened():
    print('Cannot open RTSP stream')
    exit(-1)

while True:
    _, frame = cap.read()
    kernel = np.ones((5, 5), np.uint8)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (15, 15), 0, 1, 0, 1)
    ret, thresh_img = cv2.threshold(blur, 91, 255, cv2.THRESH_BINARY)
    img_erosion = cv2.erode(thresh_img, kernel, iterations=2)
    img_dilation = cv2.dilate(img_erosion, kernel, iterations=2)

    contours = cv2.findContours(img_dilation, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)[-2]
    for c in contours:
        cv2.drawContours(frame, [c], -1, (0, 255, 0), 3)

    cv2.imshow(f'{SYSTEM} gray', gray)
    cv2.imshow(f'{SYSTEM} blur', blur)
    cv2.imshow(f'{SYSTEM} thresh_img', thresh_img)
    cv2.imshow(f'{SYSTEM} img_dilation', img_dilation)
    cv2.imshow(f'{SYSTEM} img_erosion', img_erosion)

    cv2.imshow(SYSTEM, frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
