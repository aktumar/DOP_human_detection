import os
import cv2
import argparse
import numpy as np
import configparser
from sys import platform

"""
VARIABLES
"""
global api_preferences
CONFIG_FILE = "settings.ini"
# SYSTEM = ['151', '155', '157']
# SYSTEM = ['151_min', '155_min', '157_min']
SYSTEM = ['155_min']

"""
OS platform
"""
if platform == "win32":
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
    api_preferences = cv2.CAP_FFMPEG
    path = 'C:/Users/rakhymova.a/Desktop/vid/'
    file = '1.mp4'
elif platform == "linux" or platform == "linux2":
    api_preferences = None
    path = '/home/aktumar/my_projects/video_UNT/'
    file = '1.mp4'

"""
Camera configuration
"""
config = (configparser.ConfigParser())
config.read(CONFIG_FILE)

"""
Functions
"""


def image_contour_finder(frame):
    kernel = np.ones((5, 5), np.uint8)
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (15, 15), 0, 1, 0, 1)
    ret, img_thresh = cv2.threshold(img_blur, 91, 255, cv2.THRESH_BINARY)
    img_erosion = cv2.erode(img_thresh, kernel, iterations=3)
    img_dilation = cv2.dilate(img_erosion, kernel, iterations=3)

    contours = cv2.findContours(img_dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2]
    for c in contours:
        cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)

    cv2.imshow(f'{SYSTEM} gray', img_gray)
    cv2.imshow(f'{SYSTEM} blur', img_blur)
    cv2.imshow(f'{SYSTEM} thresh_img', img_thresh)
    cv2.imshow(f'{SYSTEM} img_dilation', img_dilation)
    cv2.imshow(f'{SYSTEM} img_erosion', img_erosion)


def image_delete_background(frame):
    lower = np.array([170, 170, 170])
    upper = np.array([255, 255, 255])

    img_thresh = cv2.inRange(frame, lower, upper)
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))

    img_morph = cv2.morphologyEx(img_thresh, cv2.MORPH_CLOSE, ker)
    img_mask = 255 - img_morph
    result = cv2.bitwise_and(frame, frame, mask=img_mask)

    cv2.imshow(f'{SYSTEM} thresh_img', img_thresh)
    cv2.imshow(f'{SYSTEM} img_morph', img_morph)
    cv2.imshow(f'{SYSTEM} result', result)


def image_delete_background_upgrade(frame):
    min_area = 0.0005
    max_area = 0.95
    mask_color = (100.0, 100.0, 100.0)

    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img_gray, 15, 150)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)
    contour_info = [(c, cv2.contourArea(c),) for c in
                    cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[-2]]
    image_area = frame.shape[0] * frame.shape[1]
    max_area = max_area * image_area
    min_area = min_area * image_area
    mask = np.zeros(edges.shape, dtype=np.uint8)
    for contour in contour_info:
        if min_area < contour[1] < max_area:
            mask = cv2.fillConvexPoly(mask, contour[0], 255)
            mask = cv2.dilate(mask, None, iterations=10)
            mask = cv2.erode(mask, None, iterations=10)
            mask = cv2.GaussianBlur(mask, (21, 21), 0)

            mask_stack = np.dstack([mask] * 3)
            mask_stack = mask_stack.astype('float32') / 255.0
            frame = frame.astype('float32') / 255.0
            masked = (mask_stack * frame) + ((1 - mask_stack) * mask_color)
            masked = (masked * 255).astype('uint8')

            cv2.imshow(f'{SYSTEM} mask', mask)
            cv2.imshow(f'{SYSTEM} mask', mask)

    cv2.imshow(f'{SYSTEM} gray', img_gray)
    cv2.imshow(f'{SYSTEM} edges', edges)


"""
Main function
"""


def file_open(file, sys, api_preferences):
    cap = cv2.VideoCapture(file, api_preferences)

    if not cap.isOpened():
        print('Cannot open RTSP stream')
        exit(-1)

    while True:
        _, frame = cap.read()

        image_contour_finder(frame)
        # image_delete_background(frame)
        # image_delete_background_upgrade(frame)

        cv2.imshow(sys, frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def request_type(args):
    if args['camera'] is not None:
        print('[INFO] Opening Web Cam.')
        file_open(0, 'Camera', None)
    elif args['video'] is not None:
        print('[INFO] Opening Video from path.')
        file_open(path + file, file, None)
    elif args['url'] is not None:
        print('[INFO] Opening URL of Real-Time Streaming Protocol.')
        for sys in SYSTEM:
            username = config[sys]["USERNAME"]
            password = config[sys]["PASSWORD"]
            ip_address = config[sys]["IP_ADDRESS"]
            port = config[sys]["PORT"]
            dir = config[sys]["DIR"]
            computer = config[sys]["COMPUTER"]
            RTSP_URL = f'rtsp://{username}:{password}@{ip_address}:{port}/{dir}/Streaming/Channels/{computer}'
            print(RTSP_URL)
            file_open(RTSP_URL, sys, api_preferences)


def argsParser():
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument("-v", "--video", default=None, help="Local Video File")
    arg_parse.add_argument("-u", "--url", default=None, help="URL to Real-Time Streaming Protocol")
    arg_parse.add_argument("-c", "--camera", default=None, help="Set true if you want to use the camera.")
    args = vars(arg_parse.parse_args())
    return args


if __name__ == "__main__":
    args = argsParser()
    request_type(args)
