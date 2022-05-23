from sys import platform

# process_video.py
PROCESS_NEXT_BOX = False
PROCESS_MEDIAN = True

PERCENT_BOX_AREA = 0.01
PERCENT_BOX_DISTANCE = 0.05

COUNT_NEXT_BOX_FRAME_UPDATE = 400
COUNT_MEDIAN_FRAME_UPDATE = 150

BOX_COLOR = (0, 255, 255)
BOX_THICKNESS = 2

# log.py
LOG_IP = '127.0.0.1'
LOG_PORT = 19996

# run.py
INI_FILE = "config.ini"
# COMPUTERS = ["151", "155", "157", "151_min", "155_min", "157_min", "1a", "2a", "3a"]
# COMPUTERS = ["151_min", "155_min", "157_min", "151", "155", "157"]
# COMPUTERS = ["151_min", "155_min", "157_min"]
# COMPUTERS = ["151", "155", "157"]
COMPUTERS = ["1a", "2a", "3a"]

if platform == "win32":
    PATH_TO_VIDEO = "C:/Users/rakhymova.a/Desktop/vid/"
elif platform == "linux" or platform == "linux2":
    PATH_TO_VIDEO = "/home/aktumar/my_projects/Freelance/video_UNT/"
