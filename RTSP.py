import os
import cv2
import time
import math
import argparse
import numpy as np
import configparser
from sys import platform
from collections import deque

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


class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


def rectangles_global(rec_new, rec_old):
    return rec_new


def rectangles_union(b_array):
    posX = b_array[0].x
    posY = b_array[0].y
    posXR = b_array[0].x + b_array[0].w
    posYB = b_array[0].y + b_array[0].h

    for i in range(1, len(b_array)):
        # print(posX, posY, posXR, posYB)
        if b_array[i].x < posX:
            posX = b_array[i].x
        if b_array[i].y < posY:
            posY = b_array[i].y
        if b_array[i].x + b_array[i].w > posXR:
            posXR = b_array[i].x + b_array[i].w
        if b_array[i].y + b_array[i].h > posYB:
            posYB = b_array[i].y + b_array[i].h

    posW = posXR - posX
    posH = posYB - posY

    # print("len(b_array) = ", len(b_array))

    return Rect(posX, posY, posW, posH)


def rectangles_nearest(e, b, dist):
    exl = e.x
    exr = e.x + e.w
    eyt = e.y
    eyb = e.y + e.h

    bxl = b.x
    bxr = b.x + b.w
    byt = b.y
    byb = b.y + b.h

    cont = False

    if abs(exl - bxl) <= dist:
        cont = True
    if abs(exl - bxr) <= dist:
        cont = True
    if abs(exr - bxl) <= dist:
        cont = True
    if abs(exr - bxr) <= dist:
        cont = True

    if cont:
        if abs(eyt - byt) <= dist:
            return True
        if abs(eyt - byb) <= dist:
            return True
        if abs(eyb - byt) <= dist:
            return True
        if abs(eyb - byb) <= dist:
            return True

    return False


def rectangles_clustering(b_array, distance):
    b_unions = []
    rec_unions = []
    q = deque()

    while b_array:
        if q:
            # print("Second")
            element = q.popleft()
            # print("element = ", element.x, element.y)
            b_unions.append(element)

            for i in range(len(b_array)):
                # print(f"b_array[{i}] = ", b_array[i].x, b_array[i].y)
                if rectangles_nearest(element, b_array[i], distance):
                    # print("OK")
                    q.append(b_array[i])
                    b_array[i] = None
            b_array[:] = (value for value in b_array if value is not None)
            # print()


        else:
            # print("First")
            if b_unions:
                # print("Third, unions = ", len(b_unions))
                # print(rectangles_union(b_unions).x, rectangles_union(b_unions).y, rectangles_union(b_unions).x +
                #       rectangles_union(b_unions).w, rectangles_union(b_unions).y + rectangles_union(b_unions).h)
                rec_unions.append(rectangles_union(b_unions))
                b_unions.clear()
                # print()

            element = b_array.pop(0)
            if not b_array:
                # print("Last one = ")
                rec_unions.append(element)
                break

            # print("element = ", element.x, element.y)
            b_unions.append(element)

            for i in range(len(b_array)):
                # print("b_array[", i, "] = ", b_array[i].x, b_array[i].y)
                if rectangles_nearest(element, b_array[i], distance):
                    # print("OK")
                    q.append(b_array[i])
                    b_array[i] = None
            b_array[:] = (value for value in b_array if value is not None)

        if not b_array:
            # print("All, unions = ", len(b_unions))
            while q:
                b_unions.append(q.popleft())
            # print(rectangles_union(b_unions).x, rectangles_union(b_unions).y, rectangles_union(b_unions).x +
            #       rectangles_union(b_unions).w, rectangles_union(b_unions).y + rectangles_union(b_unions).h)
            rec_unions.append(rectangles_union(b_unions))
            # print()

    return rec_unions


def movement_detection(frame1, frame2, area, rec_glob):
    diff = cv2.absdiff(frame1, frame2)

    res = diff.astype(np.uint8)
    percentage = (np.count_nonzero(res) * 100) / res.size
    if percentage > 30:
        # print("percentage = ", percentage)
        pass

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)

    rec_array = []
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < area * 0.01:
            continue
        # print(x, y, x + w, y + h)
        # cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        rec_array.append(Rect(x, y, w, h))

    if rec_array:
        rec_cluster = rectangles_clustering(rec_array, math.sqrt(area * 0.05))
        max_rec = rec_cluster[0]
        for r in rec_cluster:
            # print("result = ", r.x, r.y, r.x + r.w, r.y + r.h)
            # cv2.rectangle(frame1, (r.x, r.y), (r.x + r.w, r.y + r.h), (0, 0, 255), 2)
            if max_rec.w * max_rec.h < r.w * r.h:
                max_rec = r
        cv2.rectangle(frame1, (max_rec.x, max_rec.y), (max_rec.x + max_rec.w, max_rec.y + max_rec.h), (0, 0, 255), 2)
        rec_glob = rectangles_global(max_rec, rec_glob)

    # print()

    # cv2.imshow("frame1", frame1)

    return frame1, rec_glob
    # time.sleep(1)


"""
Main function
"""


def file_open(file, sys, api_preferences):
    cap = cv2.VideoCapture(file, api_preferences)
    if not cap.isOpened():
        print('Cannot open file')
        exit(-1)

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    print("width = ", frame1.shape[1])
    print("height = ", frame1.shape[0])

    print("small boxes = ", frame1.shape[0] * frame1.shape[1] * 0.01)
    print("max distance between boxes = ", math.sqrt(frame1.shape[0] * frame1.shape[1] * 0.05))

    while True:
        frame, rec = movement_detection(frame1, frame2, frame1.shape[0] * frame1.shape[1], Rect(450, 500, 1, 1))
        frame1 = frame2
        ret, frame2 = cap.read()

        cv2.rectangle(frame, (rec.x, rec.y), (rec.x + rec.w, rec.y + rec.h), (0, 255, 255), 5)

        cv2.imshow("frame1", frame)

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
