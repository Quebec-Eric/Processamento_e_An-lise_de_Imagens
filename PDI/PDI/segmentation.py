import numpy as np
import imutils
import cv2

# Load image, resize smaller, HSV color threshold
image = cv2.imread("Images/DleftCC/d_left_cc (1).png")
image = imutils.resize(image, width=600)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([0, 0, 44])
upper = np.array([82, 78, 227])
mask = cv2.inRange(hsv, lower, upper)

# Remove small noise on mask with morph open
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=3)
smooth_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
opening = cv2.morphologyEx(opening, cv2.MORPH_OPEN, smooth_kernel, iterations=3)
result = cv2.bitwise_and(image, image, mask=opening)
# result[opening==0] = (255,255,255) # Optional for white background 

cv2.imshow('result', result)
cv2.imshow('mask', mask)
cv2.imshow('opening', opening)
cv2.waitKey()