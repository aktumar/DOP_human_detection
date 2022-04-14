import os
import cv2
import time
import math
import bisect
import argparse
import statistics
import numpy as np
import configparser
from sys import platform
from collections import deque

"""
VARIABLES
"""
global api_preferences
CONFIG_FILE = "settings.ini"
SYSTEM = ["151", "155", "157", "151_min", "155_min", "157_min"]

"""
OS platform
"""
if platform == "win32":
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
    api_preferences = cv2.CAP_FFMPEG
    path = "C:/Users/rakhymova.a/Desktop/vid/"
elif platform == "linux" or platform == "linux2":
    api_preferences = None
    path = "/home/aktumar/my_projects/Freelance/video_UNT/"

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


def rectangles_union(b_array):
    """
    :param b_array: - List of boxes that are in the neighborhood
    :return: - Returns the parameters of a single box obtained by unioning all received boxes.
    """

    posX = b_array[0].x
    posY = b_array[0].y
    posXR = b_array[0].x + b_array[0].w
    posYB = b_array[0].y + b_array[0].h

    for i in range(1, len(b_array)):
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

    return Rect(posX, posY, posW, posH)


def rectangles_nearest(e, b, dist):
    """
    :param e: - Main box
    :param b: - Box that is checked for neighborhood
    :param dist: - The maximum allowable distance between neighboring boxes
    :return: - Returns True if two boxes are neighbors, False if not
    """

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
    """
    :param b_array: - List of filtered boxes
    :param distance: - The maximum allowable distance between neighboring boxes
    :return: - List of merged neighboring boxes

    This function is required to identify and combine all potentially neighboring objects.
    This requires the use of all four corners of the box.
    """

    b_unions = []
    rec_unions = []
    q = deque()

    while b_array:
        if q:
            element = q.popleft()
            b_unions.append(element)
            for i in range(len(b_array)):
                if rectangles_nearest(element, b_array[i], distance):
                    q.append(b_array[i])
                    b_array[i] = None
            b_array[:] = (value for value in b_array if value is not None)
        else:
            if b_unions:
                rec_unions.append(rectangles_union(b_unions))
                b_unions.clear()

            element = b_array.pop(0)

            if not b_array:
                rec_unions.append(element)
                break

            b_unions.append(element)

            for i in range(len(b_array)):
                if rectangles_nearest(element, b_array[i], distance):
                    q.append(b_array[i])
                    b_array[i] = None

            b_array[:] = (value for value in b_array if value is not None)

        if not b_array:
            while q:
                b_unions.append(q.popleft())
            rec_unions.append(rectangles_union(b_unions))

    return rec_unions


def movement_detection(frame1, frame2, area):
    """
    :param frame1: - Old frame
    :param frame2: - New frame
    :param area: - Area of general frame
    :return:

    This function's primary responsibility is to compare old and new frames,
    using the standard method for detecting the contours of frame`s changed parts,
    filtering out unnecessary boxes, merging clusters of boxes.
    """

    diff = cv2.absdiff(frame1, frame2)

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
        # cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        rec_array.append(Rect(x, y, w, h))

    max_rec = None
    if rec_array:
        rec_cluster = rectangles_clustering(rec_array, math.sqrt(area * 0.05))
        max_rec = rec_cluster[0]
        for r in rec_cluster:
            # cv2.rectangle(frame1, (r.x, r.y), (r.x + r.w, r.y + r.h), (0, 0, 255), 2)
            if max_rec.w * max_rec.h < r.w * r.h:
                max_rec = r
        cv2.rectangle(frame1, (max_rec.x, max_rec.y), (max_rec.x + max_rec.w, max_rec.y + max_rec.h), (0, 0, 255), 2)

    # time.sleep(1)
    return frame1, max_rec


"""
Main function
"""


def file_open(file, sys, api_preferences):
    """
    :param file: - Formed path to video source
    :param sys: - Name of the window
    :param api_preferences: - For video capturing with API Preference
    :return:

    For motion detection, neighboring frames are compared, and then specific boxes with a constant
    change are identified. The movement_detection function is used to eliminate redundant data.
    """

    cap = cv2.VideoCapture(file, api_preferences)
    if not cap.isOpened():
        print("Cannot open file")
        exit(-1)

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    print("width = ", frame1.shape[1])
    print("height = ", frame1.shape[0])

    print("small boxes = ", frame1.shape[0] * frame1.shape[1] * 0.01)
    print("max distance between boxes = ", math.sqrt(frame1.shape[0] * frame1.shape[1] * 0.05))

    area = frame1.shape[0] * frame1.shape[1]

    """
    update = 0
    xr = []
    xl = []
    yt = []
    yb = []
    box = None

    while True:
        if update == 1000:
            update = 0
            xr = []
            xl = []
            yt = []
            yb = []

        frame, new_box = movement_detection(frame1, frame2, area)
        frame1 = frame2
        ret, frame2 = cap.read()

        if new_box:
            bisect.insort(xr, new_box.x + new_box.w)
            bisect.insort(xl, new_box.x)
            bisect.insort(yt, new_box.y)
            bisect.insort(yb, new_box.y + new_box.h)

            box = Rect(int(statistics.median(xl)),
                       int(statistics.median(yt)),
                       int(statistics.median(xr) - statistics.median(xl)),
                       int(statistics.median(yb) - statistics.median(yt)))
                       
    """
    update = 0
    old_box = None
    box = None
    while True:
        if update == 150:
            update = 0
            old_box = None
            box = None

        frame, new_box = movement_detection(frame1, frame2, area)
        frame1 = frame2
        ret, frame2 = cap.read()

        if new_box:
            if old_box:
                box = rectangles_union([new_box, old_box])
            else:
                box = new_box
        else:
            if old_box:
                box = old_box
            else:
                pass
        old_box = box

        if box:
            # print("-------->", box.x, box.y, box.w, box.h)
            cv2.rectangle(frame, (box.x, box.y), (box.x + box.w, box.y + box.h), (0, 255, 255), 2)

        cv2.imshow("frame", frame)
        update = update + 1

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def request_type(args):
    """
    :param args: - Pass a variable number of arguments to a function. camera:ON/video:local path/url:rtsp path
    :return:

    camera: The capturing device connects only if you have given permission by writing 'ON'
    video:  The video file will be launched if you specify the correct directory.
            If you want to specify full directory on the command line, you need to overwrite:
            file_open(args['video'], args['video'], None)
    url:    You can use the .ini file with the following parameters,
            .ini file filling example: rtsp://admin:12345@192.168.1.210:554/Streaming/Channels/101
            [10]
            USERNAME = admin
            PASSWORD = 12345
            IP_ADDRESS = 192.168.1.210
            PORT = 554
            DIR = Streaming/Channels
            COMPUTER = 101
            If you want to specify full directory on the command line, you need to overwrite:
            file_open('rtsp://admin:12345@192.168.1.210:554/Streaming/Channels/101', sys, api_preferences)
    """

    if args["camera"] is not None and args["camera"] == "ON":
        print("[INFO] Opening Web Cam.")
        file_open(0, "Camera", None)
    elif args["video"] is not None:
        print("[INFO] Opening Video from path.")
        file_open(path + args["video"], args["video"], None)
    elif args["url"] is not None and args["url"] in SYSTEM:
        print("[INFO] Opening URL of Real-Time Streaming Protocol.")
        sys = args["url"]
        username = config[sys]["USERNAME"]
        password = config[sys]["PASSWORD"]
        ip_address = config[sys]["IP_ADDRESS"]
        port = config[sys]["PORT"]
        dir = config[sys]["DIR"]
        computer = config[sys]["COMPUTER"]
        RTSP_URL = f"rtsp://{username}:{password}@{ip_address}:{port}/{dir}/{computer}"
        print(RTSP_URL)
        file_open(RTSP_URL, sys, api_preferences)


def argsParser():
    """
    camera: Use your local capturing device. Write ON to run camera.
    video:  Use local video file path. Make sure that you have entered the correct directory for the video folder.
    url:    Use IP video stream with given .ini file. Choose one computer(camera).
    """

    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument("-v", "--video", type=str, default=None,
                           help=f"Path to the local video file (select one video from default path \"{path}\"")
    arg_parse.add_argument("-u", "--url", type=str, default=None,
                           help="URL address of RTSP (select one computer: "
                                "151, 155, 157, 151_min, 155_min, 157_min)")
    arg_parse.add_argument("-c", "--camera", type=str, default=None,
                           help="Local Camera (write ON/OFF to use/cancel camera)")

    args = vars(arg_parse.parse_args())
    return args


if __name__ == "__main__":
    args = argsParser()
    request_type(args)
