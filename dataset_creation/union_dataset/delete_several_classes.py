import os
from os import listdir
from os.path import isfile, join

# pwd_output = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/1 команда/output/YOLO_darknet"
# pwd_output = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/2 команда/output/YOLO_darknet"
# pwd_output = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/3 команда/output/YOLO_darknet"
# pwd_output = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/4 команда/output/YOLO_darknet"
# pwd_output = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/5 команда/output/YOLO_darknet"

deleted_txt = []

for filename in os.listdir(pwd_output):
    with open(os.path.join(pwd_output, filename), 'r') as f:
        if filename[-3:] == "txt":
            k = f.readlines()
            for kon in k:
                if kon[0:2] == "9" or kon[0:2] == "10" or kon[0:2] == "11":
                    deleted_txt.append(filename)

for f in deleted_txt:
    os.remove(os.path.join(pwd_output, f))
    print("Deleted successfully from output => ", f)
