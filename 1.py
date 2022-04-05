import copy

import cv2
import numpy as np
import random
import matplotlib.pyplot as plt

img = cv2.imread('2.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert gray scale
print(np.unique(img))
img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]
cv2.imshow("j lj", img)

labels = random.sample(range(1, 255), 254)

x = 0
for i in range(160):
    for j in range(240):
        if (i == 0 and j == 0 and img[i][j] == 255):
            img[i][j] = labels[x]
            x += 1
        else:
            if (i == 0):
                if (img[i][j] == 255):
                    if (img[i][j - 1] != 0):
                        img[i][j] = img[i][j - 1]
                    else:
                        img[i][j] = labels[x]
                        x += 1
            if (j == 0):
                if (img[i][j] == 255):
                    if (img[i - 1][j] != 0):
                        img[i][j] = img[i - 1][j];
                    else:
                        img[i][j] = labels[x]
                        x += 1

            else:
                if (img[i][j] == 255):
                    if (img[i - 1][j] != 0):
                        img[i][j] = img[i - 1][j]
                    elif (img[i][j - 1] != 0):
                        img[i][j] = img[i][j - 1]
                    else:
                        img[i][j] = labels[x]
                        x += 1

cv2.imshow("j lj", img)

num_epochs = 15
for epoch in range(num_epochs):
    Dict = {}
    for i in range(160):
        for j in range(240):
            if (img[i][j] != 0):
                if (img[i][j - 1] != 0 and img[i - 1][j] != 0):
                    if (img[i][j - 1] != img[i - 1][j]):
                        Dict[img[i][j - 1]] = img[i - 1][j]

    # replacing multiple label to single label
    for key in Dict.keys():
        for i in range(160):
            for j in range(240):
                if (img[i][j] == Dict[key]):
                    img[i][j] = key
cv2.imshow("j lj", img)
labels = np.unique(img)
print(labels)
img_index = copy.deepcopy(img)
for index, label in zip(range(len(labels)), labels):
    # print(index,label)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img_index[i][j] == label:
                img_index[i][j] = index

labels = np.unique(img_index)

labels = np.unique(img_index)
label_hue = np.uint8(179 * img / np.max(labels))
blank_ch = 255 * np.ones_like(label_hue)
labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
print(img.shape, labeled_img.shape)
# set bg label to black
labeled_img[label_hue == 0] = 0

cv2.imshow("j lj", img)
# cv2_imshow(labeled_img)
# Showing Original Image
plt.imshow(cv2.cvtColor(labeled_img, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.title("labelled img")
plt.show()
