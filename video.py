import cv2
import numpy as np

cap = cv2.VideoCapture(0)
assert cap.isOpened(), 'No cam'

while True:
    flag, frame = cap.read()
    assert flag, 'No frame'
    
    cv2.imshow('img', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destoyAllWindows()
