
import cv2

def checkLabel(img_fillter,img_raw):
    contours, hier = cv2.findContours(img_fillter, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        ep = 0.1*cv2.arcLength(cnt, True)
        ap = cv2.approxPolyDP(cnt, ep, True)
        
        area = cv2.contourArea(cnt)
        if (len(ap)==4 and area<25000 and area>142):
            cv2.drawContours(img_raw, cnt,-1,(0,255,0),2)
            print("No Issue.Label Is Detected")
            return 1
        
    print("No Label Detected.Activate Ejection")
    return 0

pic_directory = "imageBottle//bottle_label.jpg"
#pic_directory = "imageBottle//bottle.jpg"


original_color = cv2.imread(pic_directory)
original = cv2.imread(pic_directory, cv2.IMREAD_GRAYSCALE)

#th, image = cv2.threshold(original, 240, 255, cv2.THRESH_BINARY)
image = cv2.adaptiveThreshold(original, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 5)
cv2.imwrite("imageBottle//bottle-binary.jpg", image)


checkLabel(image,original_color)
    
    

cv2.imwrite("imageBottle//bottle-contour.jpg", original_color)

