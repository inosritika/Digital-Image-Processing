import cv2

img_path=input('Give Image Path\n')

img_raw = cv2.imread(img_path)


roi = cv2.selectROI(img_raw)


roi_cropped = img_raw[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
cv2.imwrite("cropped_part.jpeg",roi_cropped)
