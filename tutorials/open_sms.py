import cv2
import nexmo
import time

# load pre-trainer classifier
classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# initialize nexmo SMS client
client_nexmo = nexmo.Client(key='your_project_key', secret='your_secret_key')

# grab video from the first camera available
video_captured = cv2.VideoCapture(0)

while (True):
    # read frame-by-frame
    ret, frame = video_captured.read()

    # set the frame to gray as we do not need color, save up the resources
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # pass the frame to the classifier
    persons_detected = classifier.detectMultiScale(gray_frame, 1.3, 5)

    # how many people have been detected on the frame
    try:
        human_count = persons_detected.shape[0]
    except:
        human_count = 0

    if (human_count > 0):
        client_nexmo.send_message({
            'from': '<your_outbound_number>',
            'to': '<your_inbound_number',
            'text': 'There has been ' + str(human_count) + ' human(s) detected!',
        })

    # extract boxes so we can visualize thifs better
    # for actual deployment with hardware, not needed
    for (x, y, w, h) in persons_detected:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        break
    cv2.imshow('Video footage', frame)

    time.sleep(5)
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

# release the video stream
video_captured.release()

# close all windows
cv2.destroyAllWindows()
