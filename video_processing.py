import cv2
import math
import bisect
import log as l
import statistics
import geometry_proccessing as gp


def file_open(file, sys, api_preferences):
    """
    :param file: - Formed path to video source
    :param sys: - Name of the window
    :param api_preferences: - For video capturing with API Preference
    :return:

    For motion detection, neighboring frames are compared, and then specific boxes with a constant
    change are identified. The movement_detection function is used to eliminate redundant data.
    """

    next_box_union = False
    median_box = True

    cap = cv2.VideoCapture(file, api_preferences)
    if not cap.isOpened():
        print("Cannot open file")
        exit(-1)

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    print("width = ", frame1.shape[1])
    print("height = ", frame1.shape[0])

    print("small boxes = ", frame1.shape[0] * frame1.shape[1] * 0.01)
    print("max distance between boxes = ", math.sqrt(frame1.shape[0] * frame1.shape[1] * 0.05))

    area = frame1.shape[0] * frame1.shape[1]

    update = 0  # general variable
    box = None  # general variable
    xr = []  # for median_box
    xl = []  # for median_box
    yt = []  # for median_box
    yb = []  # for median_box
    old_box = None  # for next_box_union
    event = False

    while True:
        frame, new_box = gp.movement_detection(frame1, frame2, area)
        frame1 = frame2
        ret, frame2 = cap.read()

        if median_box:
            if update == 400:
                update = 0
                xr.clear()
                xl.clear()
                yt.clear()
                yb.clear()
                box = None

            if new_box:
                if not event:
                    event = True

                bisect.insort(xr, new_box.x + new_box.w)
                bisect.insort(xl, new_box.x)
                bisect.insort(yt, new_box.y)
                bisect.insort(yb, new_box.y + new_box.h)

                box = gp.Rect(int(statistics.median(xl)),
                              int(statistics.median(yt)),
                              int(statistics.median(xr) - statistics.median(xl)),
                              int(statistics.median(yb) - statistics.median(yt)))
            else:
                event = False

        if next_box_union:
            if update == 150:
                update = 0
                old_box = None
                box = None

            if new_box:
                if event:
                    event = False
                else:
                    event = True

                if old_box:
                    box = gp.rectangles_union([new_box, old_box])
                else:
                    box = new_box
            else:
                if old_box:
                    box = old_box
                else:
                    pass
            old_box = box

        if box:
            cv2.rectangle(frame, (box.x, box.y), (box.x + box.w, box.y + box.h), (0, 255, 255), 2)
            if event:
                l.log.warning(f"Зафиксировано движение. Источник: {sys}")

        cv2.imshow("frame", frame)
        update = update + 1

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
