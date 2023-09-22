import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

left_image = cv.imread('tsukuba_l.png', cv.IMREAD_GRAYSCALE)
right_image = cv.imread('tsukuba_r.png', cv.IMREAD_GRAYSCALE)

stereo = cv.StereoBM_create(numDisparities=16, blockSize=21)


depth = stereo.compute(left_image, right_image)

cv.imshow("Left", left_image)
cv.imshow("right", right_image)

plt.imshow(depth)
plt.axis('off')
plt.show()