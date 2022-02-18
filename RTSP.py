import os
import cv2
import numpy as np
import configparser
from sys import platform

# OS platform
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
apiPreference = None
if platform == "win32":
    apiPreference = cv2.CAP_FFMPEG

# Camera configuration
config = (configparser.ConfigParser())
config.read("settings.ini")

# SYSTEM = ['151', '155', '157']
# SYSTEM = ['151_min', '155_min', '157_min']
SYSTEM = ['155_min']

for sys in SYSTEM:
    USERNAME = config[sys]["USERNAME"]
    PASSWORD = config[sys]["PASSWORD"]
    IP_ADDRESS = config[sys]["IP_ADDRESS"]
    PORT = config[sys]["PORT"]
    DIR = config[sys]["DIR"]
    COMPUTER = config[sys]["COMPUTER"]

    RTSP_URL = f'rtsp://{USERNAME}:{PASSWORD}@{IP_ADDRESS}:{PORT}/{DIR}/Streaming/Channels/{COMPUTER}'
    print(RTSP_URL)

    # Open video streaming
    cap = cv2.VideoCapture(RTSP_URL, apiPreference)

    if not cap.isOpened():
        print('Cannot open RTSP stream')
        exit(-1)

    while True:
        _, frame = cap.read()

        # Functions for contours
        kernel = np.ones((5, 5), np.uint8)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (15, 15), 0, 1, 0, 1)
        ret, thresh_img = cv2.threshold(blur, 91, 255, cv2.THRESH_BINARY)
        img_erosion = cv2.erode(thresh_img, kernel, iterations=3)
        img_dilation = cv2.dilate(img_erosion, kernel, iterations=3)

        contours = cv2.findContours(img_dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2]
        for c in contours:
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 3)

        cv2.imshow(f'{SYSTEM} gray', gray)
        cv2.imshow(f'{SYSTEM} blur', blur)
        cv2.imshow(f'{SYSTEM} thresh_img', thresh_img)
        cv2.imshow(f'{SYSTEM} img_dilation', img_dilation)
        cv2.imshow(f'{SYSTEM} img_erosion', img_erosion)

        # Delete background
        lower = np.array([120, 120, 120])
        upper = np.array([255, 255, 255])
        thresh = cv2.inRange(frame, lower, upper)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))
        morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        mask = 255 - morph
        result = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow(f'{SYSTEM} result', result)

        # Show final result
        cv2.imshow(sys, frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
