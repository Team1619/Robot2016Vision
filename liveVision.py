import cv2
import numpy as np

cap = cv2.VideoCapture(0)
assert cap.isOpened(), 'No cam'

lower_thresh = np.array([140, 70, 120], dtype=np.uint8)
upper_thresh = np.array([180, 255, 255], dtype=np.uint8)

while True:
    flag, frame = cap.read()
    assert flag, 'No frame'

    frame = cv2.GaussianBlur(frame, (5, 5), 0)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_thresh, upper_thresh)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = cv2.bitwise_and(gray, gray, mask=mask)

    # edges = cv2.Canny(img, 150, 200)

    contours, hierarchy = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours):
        cont = max(contours, key=cv2.contourArea)
        poly = cv2.approxPolyDP(cont, 0.05*cv2.arcLength(cont,True), True)

        cv2.drawContours(frame, [poly], 0, (255, 0, 255), 3)

    cv2.imshow('image', frame)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
