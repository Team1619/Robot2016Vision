import cv2
import numpy as np

cap = cv2.VideoCapture(1)
assert cap.isOpened(), 'No cam'

flag, frame = cap.read()

loop = True

lower_thresh = np.array([0, 0, 0], dtype=np.uint8)
upper_thresh = np.array([180, 255, 255], dtype=np.uint8)
chooseMode = 0
adjustVal = 10


def l(thresh):
    global chooseMode
    chooseMode = 0
def u(thresh):
    global chooseMode
    chooseMode = 1
def p(thresh):
    global adjustVal
    if adjustVal == 10:
        adjustVal = 2
    else:
        adjustVal = 10
def a(thresh):
    thresh[0] = thresh[0] + adjustVal
def s(thresh):
    thresh[1] = thresh[1] + adjustVal
def d(thresh):
    thresh[2] = thresh[2] + adjustVal
def z(thresh):
    thresh[0] = thresh[0] - adjustVal
def x(thresh):
    thresh[1] = thresh[1] - adjustVal
def c(thresh):
    thresh[2] = thresh[2] - adjustVal
def q(thresh):
    global loop
    loop = False

chooser = {
    'l': l,
    'u': u,
    'p': p,
    'a': a,
    's': s,
    'd': d,
    'z': z,
    'x': x,
    'c': c,
    'q': q
}

while loop:
    flag, frame = cap.read()
    assert flag, 'No frame'

    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_thresh, upper_thresh)

    frame = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('frame', frame)
    key = chr(cv2.waitKey(100) & 0xFF)
    # print(key)
    print(lower_thresh, upper_thresh)
    func = chooser.get(key, lambda x: "Nothing")
    if chooseMode:
        func(upper_thresh)
    else:
        func(lower_thresh)

cap.release()
cv2.destroyAllWindows()
