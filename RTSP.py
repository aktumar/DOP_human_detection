import os
import cv2
import configparser
from sys import platform

"""
OS platform
"""
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
if platform == "linux" or platform == "linux2":
    apiPreference = None
elif platform == "win32":
    apiPreference = None
    # apiPreference = cv2.CAP_FFMPEG

"""
Camera configuration
"""
config = (configparser.ConfigParser())
config.read("settings.ini")

SYSTEM = '151'
USERNAME = config[SYSTEM]["USERNAME"]
PASSWORD = config[SYSTEM]["PASSWORD"]
IP_ADDRESS = config[SYSTEM]["IP_ADDRESS"]
PORT = config[SYSTEM]["PORT"]
DIR = config[SYSTEM]["DIR"]
COMPUTER = config[SYSTEM]["COMPUTER"]

RTSP_URL = f'rtsp://{USERNAME}:{PASSWORD}@{IP_ADDRESS}:{PORT}/{DIR}/Streaming/Channels/{COMPUTER}'


def main():
    cap = cv2.VideoCapture(RTSP_URL, apiPreference)

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


if __name__ == "__main__":
    main()

print("Guru99")
