import cv2
import math
import config
from collections import deque


class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


def rectangles_union(b_array):
    """
    :param b_array: - List of boxes that are in the neighborhood
    :return: - Returns the parameters of a single box obtained by unioning all received boxes.
    """

    posX = b_array[0].x
    posY = b_array[0].y
    posXR = b_array[0].x + b_array[0].w
    posYB = b_array[0].y + b_array[0].h

    for i in range(1, len(b_array)):
        if b_array[i].x < posX:
            posX = b_array[i].x
        if b_array[i].y < posY:
            posY = b_array[i].y
        if b_array[i].x + b_array[i].w > posXR:
            posXR = b_array[i].x + b_array[i].w
        if b_array[i].y + b_array[i].h > posYB:
            posYB = b_array[i].y + b_array[i].h

    posW = posXR - posX
    posH = posYB - posY

    return Rect(posX, posY, posW, posH)


def rectangles_nearest(e, b, dist):
    """
    :param e: - Main box
    :param b: - Box that is checked for neighborhood
    :param dist: - The maximum allowable distance between neighboring boxes
    :return: - Returns True if two boxes are neighbors, False if not
    """

    exl = e.x
    exr = e.x + e.w
    eyt = e.y
    eyb = e.y + e.h

    bxl = b.x
    bxr = b.x + b.w
    byt = b.y
    byb = b.y + b.h

    cont = False

    if abs(exl - bxl) <= dist:
        cont = True
    if abs(exl - bxr) <= dist:
        cont = True
    if abs(exr - bxl) <= dist:
        cont = True
    if abs(exr - bxr) <= dist:
        cont = True

    if cont:
        if abs(eyt - byt) <= dist:
            return True
        if abs(eyt - byb) <= dist:
            return True
        if abs(eyb - byt) <= dist:
            return True
        if abs(eyb - byb) <= dist:
            return True

    return False


def rectangles_clustering(b_array, distance):
    """
    :param b_array: - List of filtered boxes
    :param distance: - The maximum allowable distance between neighboring boxes
    :return: - List of merged neighboring boxes

    This function is required to identify and combine all potentially neighboring objects.
    This requires the use of all four corners of the box.
    """

    b_unions = []
    rec_unions = []
    q = deque()

    while b_array:
        if q:
            element = q.popleft()
            b_unions.append(element)
            for i in range(len(b_array)):
                if rectangles_nearest(element, b_array[i], distance):
                    q.append(b_array[i])
                    b_array[i] = None
            b_array[:] = (value for value in b_array if value is not None)
        else:
            if b_unions:
                rec_unions.append(rectangles_union(b_unions))
                b_unions.clear()

            element = b_array.pop(0)

            if not b_array:
                rec_unions.append(element)
                break

            b_unions.append(element)

            for i in range(len(b_array)):
                if rectangles_nearest(element, b_array[i], distance):
                    q.append(b_array[i])
                    b_array[i] = None

            b_array[:] = (value for value in b_array if value is not None)

        if not b_array:
            while q:
                b_unions.append(q.popleft())
            rec_unions.append(rectangles_union(b_unions))

    return rec_unions


def movement_detection(frame1, frame2, area):
    """
    :param frame1: - Old frame
    :param frame2: - New frame
    :param area: - Area of general frame
    :return:

    This function's primary responsibility is to compare old and new frames,
    using the standard method for detecting the contours of frame`s changed parts,
    filtering out unnecessary boxes, merging clusters of boxes.
    """

    diff = cv2.absdiff(frame1, frame2)

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)

    rec_array = []
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < area * config.PERCENT_BOX_AREA:
            continue
        # cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        rec_array.append(Rect(x, y, w, h))

    max_rec = None
    if rec_array:
        rec_cluster = rectangles_clustering(rec_array, math.sqrt(area * config.PERCENT_BOX_DISTANCE))
        max_rec = rec_cluster[0]
        for r in rec_cluster:
            # cv2.rectangle(frame1, (r.x, r.y), (r.x + r.w, r.y + r.h), (0, 0, 255), 2)
            if max_rec.w * max_rec.h < r.w * r.h:
                max_rec = r
        # cv2.rectangle(frame1, (max_rec.x, max_rec.y), (max_rec.x + max_rec.w, max_rec.y + max_rec.h), (0, 0, 255), 2)

    return frame1, max_rec
