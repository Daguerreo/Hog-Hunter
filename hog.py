__author__ = 'Daguerreo'

import cv2
import util

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
hogParams = {'winStride': (8, 8), 'padding': (8, 8), 'scale': 1.05}

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

def draw_detections(img, rects, thickness=1, color=(0, 255, 0)):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), color, thickness)

    return

def detect():
    result,w = hog.detectMultiScale(frame, **hogParams)
    found_filtered = []

    for ri, r in enumerate(result):
        for qi, q in enumerate(result):
            if ri != qi and inside(r, q):
                break
            else:
                found_filtered.append(r)
    draw_detections(frame, result)
    draw_detections(frame, found_filtered, 3)
    print '%d (%d) found' % (len(found_filtered), len(result))

    return

cap = cv2.VideoCapture(0)
flag=cap.isOpened()
# cap.set(3,320)
# cap.set(4,240)

while True:
    flag, frame=cap.read()
    # frame2=cv2.cvtColor(frame,cv2.COLOR_BGR2YCR_CB)
    #
    # frame_col=frame2[:,:,1]

    result,w = hog.detectMultiScale(frame, **hogParams)

    found_filtered = []
    for ri, r in enumerate(result):
        for qi, q in enumerate(result):
            if ri != qi and inside(r, q):
                break
            else:
                found_filtered.append(r)
    draw_detections(frame, result, 1, (255,0,0))
    draw_detections(frame, found_filtered, 3)
    print '%d (%d) found' % (len(found_filtered), len(result))

    cv2.imshow('img', frame)
    ch = cv2.waitKey(5)
    if ch == 27:
        cap.release()
        break

cv2.destroyAllWindows()