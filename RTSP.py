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
SYSTEM = ['155']

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
    # cap = cv2.VideoCapture(RTSP_URL, apiPreference)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print('Cannot open RTSP stream')
        exit(-1)

    while True:
        _, frame = cap.read()

        # Functions for contours
        # kernel = np.ones((5, 5), np.uint8)
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # blur = cv2.GaussianBlur(gray, (15, 15), 0, 1, 0, 1)
        # ret, thresh_img = cv2.threshold(blur, 91, 255, cv2.THRESH_BINARY)
        # img_erosion = cv2.erode(thresh_img, kernel, iterations=3)
        # img_dilation = cv2.dilate(img_erosion, kernel, iterations=3)
        #
        # contours = cv2.findContours(img_dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2]
        # for c in contours:
        #     cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
        #
        # cv2.imshow(f'{SYSTEM} gray', gray)
        # cv2.imshow(f'{SYSTEM} blur', blur)
        # cv2.imshow(f'{SYSTEM} thresh_img', thresh_img)
        # cv2.imshow(f'{SYSTEM} img_dilation', img_dilation)
        # cv2.imshow(f'{SYSTEM} img_erosion', img_erosion)

        # Delete background
        # lower = np.array([170, 170, 170])
        # upper = np.array([255, 255, 255])
        # thresh = cv2.inRange(frame, lower, upper)
        # cv2.imshow("thresh", thresh)
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))
        # morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        # cv2.imshow("morph", morph)
        # mask = 255 - morph
        # result = cv2.bitwise_and(frame, frame, mask=mask)
        # cv2.imshow(f'{SYSTEM} result', result)

        # Delete background better
        min_area = 0.0005
        max_area = 0.95
        mask_color = (100.0, 100.0, 100.0)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("gray", gray)
        edges = cv2.Canny(gray, 15, 150)
        edges = cv2.dilate(edges, None)
        edges = cv2.erode(edges, None)
        contour_info = [(c, cv2.contourArea(c),) for c in
                        cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[-2]]
        cv2.imshow("edges", edges)
        image_area = frame.shape[0] * frame.shape[1]
        max_area = max_area * image_area
        min_area = min_area * image_area
        mask = np.zeros(edges.shape, dtype=np.uint8)
        for contour in contour_info:
            print(contour)
            if contour[1] > min_area and contour[1] < max_area:
                mask = cv2.fillConvexPoly(mask, contour[0], (255))
                mask = cv2.dilate(mask, None, iterations=10)
                mask = cv2.erode(mask, None, iterations=10)
                mask = cv2.GaussianBlur(mask, (21, 21), 0)
                cv2.imshow("mask", mask)
                mask_stack = np.dstack([mask] * 3)
                mask_stack = mask_stack.astype('float32') / 255.0
                frame = frame.astype('float32') / 255.0
                masked = (mask_stack * frame) + ((1-mask_stack) * mask_color)
                masked = (masked * 255).astype('uint8')
                cv2.imshow("Foreground", masked)

        # Show final result
        cv2.imshow(sys, frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
