import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import os

def SIFT():
    root = os.getcwd()
    imgPath = os.path.join(root,'data', '1.png')
    if not os.path.exists(imgPath):
        print(f"Error: The file at {imgPath} does not exist.")
        return
    
    imgGray = cv.imread(imgPath, cv.IMREAD_GRAYSCALE)
    if imgGray is None:
        print(f"Error: Failed to read the image file from {imgPath}.")
        return

    sift = cv.SIFT_create()
    keypoints = sift.detect(imgGray, None)
    imgKeypoints = cv.drawKeypoints(imgGray, keypoints, None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv.imshow('img', imgKeypoints)
    cv.waitKey(0)

    # plt.figure()
    # plt.imshow(imgKeypoints, cmap='gray')
    # plt.show()

if __name__ == '__main__':
    SIFT()
