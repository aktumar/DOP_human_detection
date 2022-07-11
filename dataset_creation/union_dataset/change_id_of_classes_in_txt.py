"""
+ 1. Удалить пустые заметки
+ 2. Удалить ненужные фотки
+ 3. Удалить фотки и заметки где нет пар
4. Поменять айдишки классов под новый
5. Объеденить все фотки, со всех папок
"""

import os
from os import listdir
from os.path import isfile, join

# with open(os.path.join(pwd, "class_list.txt"), 'r') as f:
#     local_class = f.readlines()


# pwd = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/1 команда/"
# pwd_input = pwd + "input"
# pwd_output = pwd + "output/YOLO_darknet"
# for filename in os.listdir(pwd_output):
#     with open(os.path.join(pwd_output, filename), 'r') as f:
#         if filename[-3:] == "txt":
#             k = f.readlines()
#             lines = []
#             new_lines = []
#             for kon in k:
#                 if kon[0] == "0":
#                     new_kon = kon.replace(kon[0], "1", 1)
#                 elif kon[0] == "1":
#                     new_kon = kon.replace(kon[0], "0", 1)
#                 elif kon[0] == "2":
#                     new_kon = kon.replace(kon[0], "2", 1)
#                 elif kon[0] == "3":
#                     new_kon = kon.replace(kon[0], "5", 1)
#                 elif kon[0] == "4":
#                     new_kon = kon.replace(kon[0], "3", 1)
#                 lines.append(kon)
#                 new_lines.append(new_kon)
#             # print(filename, " ", lines, new_lines)
#
#     with open(filename, 'w') as f:
#         print(new_lines)
#         for new_line in new_lines:
#             f.write(new_line)
#         print("Changed successfully")


# pwd = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/2 команда/"
# pwd_input = pwd + "input"
# pwd_output = pwd + "output/YOLO_darknet"
# for filename in os.listdir(pwd_output):
#     with open(os.path.join(pwd_output, filename), 'r') as f:
#         if filename[-3:] == "txt":
#             k = f.readlines()
#             lines = []
#             new_lines = []
#             for kon in k:
#                 if kon[0] == "0":
#                     new_kon = kon.replace(kon[0], "0", 1)
#                 elif kon[0] == "1":
#                     new_kon = kon.replace(kon[0], "5", 1)
#                 elif kon[0] == "2":
#                     new_kon = kon.replace(kon[0], "3", 1)
#                 elif kon[0] == "3":
#                     new_kon = kon.replace(kon[0], "7", 1)
#                 elif kon[0] == "4":
#                     new_kon = kon.replace(kon[0], "9", 1)
#                 elif kon[0] == "5":
#                     new_kon = kon.replace(kon[0], "10", 1)
#                 elif kon[0] == "6":
#                     new_kon = kon.replace(kon[0], "11", 1)
#                 lines.append(kon)
#                 new_lines.append(new_kon)
#             # print(filename, " ", lines, new_lines)
#
#     with open(filename, 'w') as f:
#         print(new_lines)
#         for new_line in new_lines:
#             f.write(new_line)
#         print("Changed successfully")


# pwd = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/3 команда/"
# pwd_input = pwd + "input"
# pwd_output = pwd + "output/YOLO_darknet"
# for filename in os.listdir(pwd_output):
#     with open(os.path.join(pwd_output, filename), 'r') as f:
#         if filename[-3:] == "txt":
#             k = f.readlines()
#             lines = []
#             new_lines = []
#             for kon in k:
#                 if kon[0] == "0":
#                     new_kon = kon.replace(kon[0], "5", 1)
#                 elif kon[0] == "1":
#                     new_kon = kon.replace(kon[0], "2", 1)
#                 elif kon[0] == "2":
#                     new_kon = kon.replace(kon[0], "1", 1)
#                 elif kon[0] == "3":
#                     new_kon = kon.replace(kon[0], "0", 1)
#                 elif kon[0] == "4":
#                     new_kon = kon.replace(kon[0], "4", 1)
#                 elif kon[0] == "5":
#                     new_kon = kon.replace(kon[0], "6", 1)
#                 elif kon[0] == "6":
#                     new_kon = kon.replace(kon[0], "3", 1)
#                 lines.append(kon)
#                 new_lines.append(new_kon)
#             # print(filename, " ", lines, new_lines)
#
#     with open(filename, 'w') as f:
#         print(new_lines)
#         for new_line in new_lines:
#             f.write(new_line)
#         print("Changed successfully")

# pwd = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/4 команда/"
# pwd_input = pwd + "input"
# pwd_output = pwd + "output/YOLO_darknet"
# for filename in os.listdir(pwd_output):
#     with open(os.path.join(pwd_output, filename), 'r') as f:
#         if filename[-3:] == "txt":
#             k = f.readlines()
#             lines = []
#             new_lines = []
#             for kon in k:
#                 if kon[0] == "0":
#                     new_kon = kon.replace(kon[0], "1", 1)
#                 elif kon[0] == "1":
#                     new_kon = kon.replace(kon[0], "0", 1)
#                 elif kon[0] == "2":
#                     new_kon = kon.replace(kon[0], "2", 1)
#                 elif kon[0] == "3":
#                     new_kon = kon.replace(kon[0], "5", 1)
#                 elif kon[0] == "4":
#                     new_kon = kon.replace(kon[0], "3", 1)
#                 lines.append(kon)
#                 new_lines.append(new_kon)
#             # print(filename, " ", lines, new_lines)
#
#     with open(filename, 'w') as f:
#         print(new_lines)
#         for new_line in new_lines:
#             f.write(new_line)
#         print("Changed successfully")

# pwd = "/home/aktumar/my_projects/Freelance/D_human_detection/dataset_creation/main/command_dataset/5 команда/"
# pwd_input = pwd + "input"
# pwd_output = pwd + "output/YOLO_darknet"
# for filename in os.listdir(pwd_output):
#     with open(os.path.join(pwd_output, filename), 'r') as f:
#         if filename[-3:] == "txt":
#             k = f.readlines()
#             lines = []
#             new_lines = []
#             for kon in k:
#                 if kon[0] == "0":
#                     new_kon = kon.replace(kon[0], "0", 1)
#                 elif kon[0] == "1":
#                     new_kon = kon.replace(kon[0], "4", 1)
#                 elif kon[0] == "2":
#                     new_kon = kon.replace(kon[0], "2", 1)
#                 elif kon[0] == "3":
#                     new_kon = kon.replace(kon[0], "8", 1)
#                 elif kon[0] == "4":
#                     new_kon = kon.replace(kon[0], "1", 1)
#                 elif kon[0] == "5":
#                     new_kon = kon.replace(kon[0], "5", 1)
#                 elif kon[0] == "6":
#                     new_kon = kon.replace(kon[0], "7", 1)
#                 elif kon[0] == "7":
#                     new_kon = kon.replace(kon[0], "9", 1)
#                 elif kon[0] == "8":
#                     new_kon = kon.replace(kon[0], "3", 1)
#                 lines.append(kon)
#                 new_lines.append(new_kon)
#             # print(filename, " ", lines, new_lines)
#
#     with open(filename, 'w') as f:
#         print(new_lines)
#         for new_line in new_lines:
#             f.write(new_line)
#         print("Changed successfully")
