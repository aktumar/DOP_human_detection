import os

pwd1 = "/home/aktumar/my_projects/Freelance/DOP_Dataset_creation/main/output/YOLO_darknet"
for filename in os.listdir(pwd1):
    with open(os.path.join(pwd1, filename), 'r') as f:
        if filename[-3:] == "txt":
            k = f.readlines()
            lines = []
            for kon in k:
                if kon[0] == "0":
                    kon = kon.replace(kon[0], "1", 1)
                elif kon[0] == "1":
                    kon = kon.replace(kon[0], "0", 1)
                elif kon[0] == "2":
                    kon = kon.replace(kon[0], "2", 1)
                elif kon[0] == "3":
                    kon = kon.replace(kon[0], "5", 1)
                elif kon[0] == "4":
                    kon = kon.replace(kon[0], "3", 1)
                lines.append(kon)
            print(filename, " ", lines)

            with open(filename, 'w') as f:
                for line in lines:
                    f.write(line)
                    print("Changed successfully")

# pwd1 = "/home/aktumar/my_projects/Freelance/DOP_Dataset_creation/main/command_dataset/2 команда/input"
# for filename in os.listdir(pwd1):
#     with open(os.path.join(pwd1, filename), 'r') as f:
#         if filename[-3:] == "txt":
#             k = f.readlines()
#             lines = []
#             for kon in k:
#                 if kon[0] == "0":
#                     kon = kon.replace(kon[0], "0", 1)
#                 if kon[0] == "1":
#                     kon = kon.replace(kon[0], "5", 1)
#                 if kon[0] == "2":
#                     kon = kon.replace(kon[0], "3", 1)
#                 if kon[0] == "3":
#                     kon = kon.replace(kon[0], "7", 1)
#                 if kon[0] == "4":
#                     kon = kon.replace(kon[0], "9", 1)
#                 if kon[0] == "5":
#                     kon = kon.replace(kon[0], "10", 1)
#                 if kon[0] == "6":
#                     kon = kon.replace(kon[0], "11", 1)
#                 lines.append(kon)
#             print(filename, " ", lines)
#
#             with open(filename, 'w') as f:
#                 for line in lines:
#                     f.write(line)
#                     print("Changed successfully")
#
# # pwd1 = "/home/aktumar/my_projects/Freelance/DOP_Dataset_creation/main/command_dataset/3 команда/input"
# for filename in os.listdir(pwd1):
#     with open(os.path.join(pwd1, filename), 'r') as f:
#         if filename[-3:] == "txt":
#             k = f.readlines()
#             lines = []
#             for kon in k:
#                 if kon[0] == "0":
#                     kon = kon.replace(kon[0], "5", 1)
#                 if kon[0] == "1":
#                     kon = kon.replace(kon[0], "2", 1)
#                 if kon[0] == "2":
#                     kon = kon.replace(kon[0], "1", 1)
#                 if kon[0] == "3":
#                     kon = kon.replace(kon[0], "0", 1)
#                 if kon[0] == "4":
#                     kon = kon.replace(kon[0], "4", 1)
#                 if kon[0] == "5":
#                     kon = kon.replace(kon[0], "6", 1)
#                 if kon[0] == "6":
#                     kon = kon.replace(kon[0], "3", 1)
#                 lines.append(kon)
#             print(filename, " ", lines)
#
#             with open(filename, 'w') as f:
#                 for line in lines:
#                     f.write(line)
#                     print("Changed successfully")
#
# # pwd1 = "/home/aktumar/my_projects/Freelance/DOP_Dataset_creation/main/command_dataset/4 команда/input"
# for filename in os.listdir(pwd1):
#     with open(os.path.join(pwd1, filename), 'r') as f:
#         if filename[-3:] == "txt":
#             k = f.readlines()
#             lines = []
#             for kon in k:
#                 if kon[0] == "0":
#                     kon = kon.replace(kon[0], "1", 1)
#                 if kon[0] == "1":
#                     kon = kon.replace(kon[0], "0", 1)
#                 if kon[0] == "2":
#                     kon = kon.replace(kon[0], "2", 1)
#                 if kon[0] == "3":
#                     kon = kon.replace(kon[0], "5", 1)
#                 if kon[0] == "4":
#                     kon = kon.replace(kon[0], "3", 1)
#                 lines.append(kon)
#             print(filename, " ", lines)
#
#             with open(filename, 'w') as f:
#                 for line in lines:
#                     f.write(line)
#                     print("Changed successfully")
#
# # pwd1 = "/home/aktumar/my_projects/Freelance/DOP_Dataset_creation/main/command_dataset/5 команда/input"
# for filename in os.listdir(pwd1):
#     with open(os.path.join(pwd1, filename), 'r') as f:
#         if filename[-3:] == "txt":
#             k = f.readlines()
#             lines = []
#             for kon in k:
#                 if kon[0] == "0":
#                     kon = kon.replace(kon[0], "0", 1)
#                 if kon[0] == "1":
#                     kon = kon.replace(kon[0], "4", 1)
#                 if kon[0] == "2":
#                     kon = kon.replace(kon[0], "2", 1)
#                 if kon[0] == "3":
#                     kon = kon.replace(kon[0], "8", 1)
#                 if kon[0] == "4":
#                     kon = kon.replace(kon[0], "1", 1)
#                 if kon[0] == "5":
#                     kon = kon.replace(kon[0], "5", 1)
#                 if kon[0] == "6":
#                     kon = kon.replace(kon[0], "7", 1)
#                 if kon[0] == "7":
#                     kon = kon.replace(kon[0], "9", 1)
#                 if kon[0] == "8":
#                     kon = kon.replace(kon[0], "3", 1)
#
#                 lines.append(kon)
#             print(filename, " ", lines)
#
#             with open(filename, 'w') as f:
#                 for line in lines:
#                     f.write(line)
#                     print("Changed successfully")
#
# # pwd1 = "/home/aktumar/my_projects/Freelance/DOP_Dataset_creation/main/command_dataset/6 команда/input"
# for filename in os.listdir(pwd1):
#     with open(os.path.join(pwd1, filename), 'r') as f:
#         if filename[-3:] == "txt":
#             k = f.readlines()
#             lines = []
#             for kon in k:
#                 if kon[0] == "0":
#                     kon = kon.replace(kon[0], "0", 1)
#                 if kon[0] == "1":
#                     kon = kon.replace(kon[0], "6", 1)
#                 if kon[0] == "2":
#                     kon = kon.replace(kon[0], "5", 1)
#                 if kon[0] == "3":
#                     kon = kon.replace(kon[0], "3", 1)
#                 if kon[0] == "4":
#                     kon = kon.replace(kon[0], "1", 1)
#                 if kon[0] == "5":
#                     kon = kon.replace(kon[0], "2", 1)
#                 lines.append(kon)
#             print(filename, " ", lines)
#
#             with open(filename, 'w') as f:
#                 for line in lines:
#                     f.write(line)
#                     print("Changed successfully")
#
# # pwd1 = "/home/aktumar/my_projects/Freelance/DOP_Dataset_creation/main/command_dataset/7 команда/input"
# for filename in os.listdir(pwd1):
#     with open(os.path.join(pwd1, filename), 'r') as f:
#         if filename[-3:] == "txt":
#             k = f.readlines()
#             lines = []
#             for kon in k:
#                 if kon[0] == "0":
#                     kon = kon.replace(kon[0], "0", 1)
#                 if kon[0] == "1":
#                     kon = kon.replace(kon[0], "1", 1)
#                 if kon[0] == "2":
#                     kon = kon.replace(kon[0], "2", 1)
#                 if kon[0] == "3":
#                     kon = kon.replace(kon[0], "5", 1)
#                 if kon[0] == "4":
#                     kon = kon.replace(kon[0], "3", 1)
#                 lines.append(kon)
#             print(filename, " ", lines)
#
#             with open(filename, 'w') as f:
#                 for line in lines:
#                     f.write(line)
#                     print("Changed successfully")
