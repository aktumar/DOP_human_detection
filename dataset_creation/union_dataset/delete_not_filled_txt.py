import os

# pwd = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/1 команда/output/YOLO_darknet"
# pwd = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/2 команда/output/YOLO_darknet"
# pwd = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/3 команда/output/YOLO_darknet"
# pwd = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/4 команда/output/YOLO_darknet"
# pwd = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/5 команда/output/YOLO_darknet"

i = 0
for filename in os.listdir(pwd):
    with open(os.path.join(pwd, filename), 'r') as f:
        if filename[-3:] == "txt":
            if os.path.getsize(pwd + "/" + filename) == 0:
                print(pwd + "/" + filename)
                os.remove(os.path.join(pwd, filename))
                i = i + 1
                print("Deleted successfully = ", i)
