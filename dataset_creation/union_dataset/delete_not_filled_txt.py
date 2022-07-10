import os

pwd = "/home/aktumar/my_projects/Freelance/DOP_Dataset_creation/main/command_dataset/7 команда/input"
i = 0
for filename in os.listdir(pwd):
    with open(os.path.join(pwd, filename), 'r') as f:
        if filename[-3:] == "txt":
            if os.path.getsize(pwd + "/" + filename) == 0:
                print(pwd + "/" + filename)
                os.remove(os.path.join(pwd, filename))
                i = i + 1
                print("Deleted successfully = ", i)
