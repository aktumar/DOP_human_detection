import os
import cv2
import time
import argparse
import numpy as np
import configparser
from sys import platform

"""
VARIABLES
"""
global api_preferences
CONFIG_FILE = "settings.ini"
SYSTEM = ['151', '155', '157', '151_min', '155_min', '157_min', '1a', '2a', '3a']

"""
OS platform
"""
if platform == "win32":
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
    api_preferences = cv2.CAP_FFMPEG
    path = 'C:/Users/rakhymova.a/Desktop/vid/'
elif platform == "linux" or platform == "linux2":
    api_preferences = None
    path = '/home/aktumar/my_projects/Freelance/video_UNT/'

"""
Camera configuration
"""
config = (configparser.ConfigParser())
config.read(CONFIG_FILE)

"""
Functions
"""


def image_movement_detection(frame1, frame2, xl, yt, xr, ym):
    diff = cv2.absdiff(frame1, frame2)

    res = diff.astype(np.uint8)
    percentage = (np.count_nonzero(res) * 100) / res.size
    if percentage > 30:
        print("percentage = ", percentage)

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)

    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        cv2.rectangle(frame1, (xl, yt), (xr, ym), (0, 255, 255), 2)
        (x, y, w, h) = cv2.boundingRect(contour)
        # print(x, y, w, h)
        # print(cv2.contourArea(contour))
        if cv2.contourArea(contour) < 1000:
            continue
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if xl > x and abs(xl - xr) < 150:
            xl = x
        if yt > y and abs(yt - y) < 150:
            yt = y
        if xr < x + w and abs(xr - x + w) < 150:
            xr = x + w
        if ym < y + h and abs(ym - y + h) < 150:
            ym = y + h

        # print(xl, yt, xr, ym)

    if abs(ym - yt) * abs(xl - xr) > 20000:
        cv2.rectangle(frame1, (xl, yt), (xr, ym), (0, 0, 255), 2)
        cv2.putText(frame1, "Movement", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)

    cv2.imshow("frame1", frame1)
    # time.sleep(0.005)


"""
Main function
"""


def file_open(file, sys, api_preferences):
    movement_detector = 1
    contour_finder = None
    delete_background = None
    delete_background_upgrade = None

    cap = cv2.VideoCapture(file, api_preferences)
    if not cap.isOpened():
        print('Cannot open file')
        exit(-1)

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    width = cap.get(3)
    height = cap.get(4)

    global xl, yt, xr, ym
    xl = int(width / 2 - 20)
    yt = int(height / 2 - 20)
    xr = int(width / 2 + 20)
    ym = int(height / 2 + 20)

    print(xl, yt, xr, ym)

    while True:
        if movement_detector:
            image_movement_detection(frame1, frame2, xl, yt, xr, ym)
            frame1 = frame2
            ret, frame2 = cap.read()
        if contour_finder:
            _, frame = cap.read()
            image_contour_finder(frame)
            cv2.imshow(sys, frame)
        if delete_background:
            _, frame = cap.read()
            image_delete_background(frame)
            cv2.imshow(sys, frame)
        if delete_background_upgrade:
            _, frame = cap.read()
            image_delete_background_upgrade(frame)
            cv2.imshow(sys, frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def request_type(args):
    if args['camera'] is not None and args['camera'] == "ON":
        print('[INFO] Opening Web Cam.')
        file_open(0, 'Camera', None)
    elif args['video'] is not None:
        print('[INFO] Opening Video from path.')
        file_open(path + args['video'], args['video'], None)
    elif args['url'] is not None and args['url'] in SYSTEM:
        print('[INFO] Opening URL of Real-Time Streaming Protocol.')
        # for sys in SYSTEM:
        sys = args['url']
        username = config[sys]["USERNAME"]
        password = config[sys]["PASSWORD"]
        ip_address = config[sys]["IP_ADDRESS"]
        port = config[sys]["PORT"]
        dir = config[sys]["DIR"]
        computer = config[sys]["COMPUTER"]
        RTSP_URL = f'rtsp://{username}:{password}@{ip_address}:{port}/{dir}/{computer}'
        print(RTSP_URL)
        file_open(RTSP_URL, sys, api_preferences)


def argsParser():
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument("-v", "--video", type=str, default=None,
                           help=f"Path to the local video file (select one video from default path \"{path}\"")
    arg_parse.add_argument("-u", "--url", type=str, default=None,
                           help="URL address of RTSP (select one computer: "
                                "151, 155, 157, 151_min, 155_min, 157_min, 1a, 2a, 3a)")
    arg_parse.add_argument("-c", "--camera", type=str, default=None,
                           help="Local Camera (write ON/OFF to use/cancel camera)")

    args = vars(arg_parse.parse_args())
    return args


if __name__ == "__main__":
    args = argsParser()
    request_type(args)
