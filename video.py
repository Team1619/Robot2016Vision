import cv2
import numpy as np

cap = cv2.VideoCapture(0)
assert cap.isOpened(), 'Nope camera'

while True:
    flag, frame = cap.read()
    assert flag, 'Nope frame'

    cv2.imshow('img', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
