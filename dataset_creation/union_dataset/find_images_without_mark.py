import os
from os import listdir
from os.path import isfile, join

my_dir = "/home/aktumar/my_projects/Freelance/DOP_Dataset_creation/main/command_dataset/7 команда/input"
# my_dir = "/home/aktumar/my_projects/Freelance/DOP_Dataset_creation/main/output/YOLO_darknet"
allfiles = [f for f in listdir(my_dir) if isfile(join(my_dir, f))]

allfiles.sort()

for i in range(len(allfiles)):
    allfiles[i] = allfiles[i][:-3]

onefile = []
for i in range(len(allfiles)):
    count = allfiles.count(allfiles[i])
    print(allfiles[i], " ", count)
    if count == 1:
        onefile.append(allfiles[i])

print(onefile)
i = 0
for fname in os.listdir(my_dir):
    for on in onefile:
        if fname.startswith(on):
            os.remove(os.path.join(my_dir, fname))
            i = i + 1
            print("Deleted successfully = ", i)
