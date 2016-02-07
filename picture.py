import cv2
import numpy as np

cap = cv2.VideoCapture(0)
assert cap.isOpened(), 'No cam'

flag, frame = cap.read()
assert flag, 'No frame'

cv2.imwrite('img.png', frame)

cap.release()
