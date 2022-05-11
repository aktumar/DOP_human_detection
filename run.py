import os
import cv2
import config
import argparse
import configparser
from video_processing import CaptureThread

from sys import platform

"""
VARIABLES
"""
global api_preferences

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
file = (configparser.ConfigParser())
file.read(config.INI_FILE)


def url_gen(sys):
    username = file[sys]["USERNAME"]
    password = file[sys]["PASSWORD"]
    ip_address = file[sys]["IP_ADDRESS"]
    port = file[sys]["PORT"]
    dir = file[sys]["DIR"]
    computer = file[sys]["COMPUTER"]
    return f"rtsp://{username}:{password}@{ip_address}:{port}/{dir}/{computer}"


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

    if args["camera"] is not None and args["camera"] == "true":
        print("[INFO] Opening Web Cam.")
        CaptureThread(0, "Camera", None).start()
    elif args["video"] is not None:
        print("[INFO] Opening Video from path.")
        CaptureThread(path + args["video"], args["video"], None).start()
    elif args["url"] is not None:
        if args["url"] == "all":
            print("[INFO] Opening URL of Real-Time Streaming Protocol.")
            for sys in config.COMPUTERS:
                rtsp_url = url_gen(sys)
                print(rtsp_url)
                CaptureThread(rtsp_url, sys, api_preferences).start()

        elif args["url"] in config.COMPUTERS:
            print("[INFO] Opening URL of Real-Time Streaming Protocol.")
            rtsp_url = url_gen(args["url"])
            print(rtsp_url)
            CaptureThread(rtsp_url, args["url"], api_preferences).start()


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
                           help="URL address of RTSP (select one computer from .ini file")
    arg_parse.add_argument("-c", "--camera", type=str, default=None,
                           help="Local Camera (write true/false to use/cancel camera)")

    args = vars(arg_parse.parse_args())
    return args


if __name__ == "__main__":
    args = argsParser()
    request_type(args)
