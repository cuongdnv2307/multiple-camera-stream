import numpy as np
import cv2
import time


def get_output(out=None):
    #Specify the path and name of the video file as well as the encoding, fps and resolution
    if out:
        out.release()
    return cv2.VideoWriter(str(time.strftime('%d %m %Y - %H %M %S' )) + '.avi',   cv2.VideoWriter_fourcc(*'MJPG'),
                             30, (640,480))

cap = cv2.VideoCapture(0)
next_time = time.time() + 60
out = get_output()

while True:
    if time.time() > next_time:
        next_time += 60
        out = get_output(out)

    # Capture frame-by-frame
    ret, frame = cap.read() 

    if ret:
        out.write(frame)
        cv2.imshow('Frame', frame)
    # Break the loop
    else:
        break    

cap.release()
cv2.destroyAllWindows()