import os
from os import listdir
from os.path import isfile, join

# my_dir_input = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/1 команда/input"
# my_dir_output = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/1 команда/output/YOLO_darknet"
#
# my_dir_input = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/2 команда/input"
# my_dir_output = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/2 команда/output/YOLO_darknet"
#
# my_dir_input = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/3 команда/input"
# my_dir_output = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/3 команда/output/YOLO_darknet"
#
# my_dir_input = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/4 команда/input"
# my_dir_output = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/4 команда/output/YOLO_darknet"
#
# my_dir_input = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/5 команда/input"
# my_dir_output = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/5 команда/output/YOLO_darknet"


allfiles_input = [f for f in listdir(my_dir_input) if isfile(join(my_dir_input, f))]
allfiles_output = [f for f in listdir(my_dir_output) if isfile(join(my_dir_output, f))]

allfiles = allfiles_input + allfiles_output

allfiles.sort()

# print(allfiles)

for i in range(len(allfiles)):
    allfiles[i] = allfiles[i][:-3]

onefile = []
for i in range(len(allfiles)):
    count = allfiles.count(allfiles[i])
    # print(allfiles[i], " ", count)
    if count == 1:
        onefile.append(allfiles[i])

i = 0
for fname in os.listdir(my_dir_input):
    for on in onefile:
        if fname.startswith(on):
            os.remove(os.path.join(my_dir_input, fname))
            i = i + 1
print("Deleted successfully from input = ", i)

i = 0
for fname in os.listdir(my_dir_output):
    for on in onefile:
        if fname.startswith(on):
            os.remove(os.path.join(my_dir_output, fname))
            i = i + 1
print("Deleted successfully from output = ", i)
