
import cv2

# Open the default camera (0 = first webcam)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Read one frame
ret, frame = cap.read()
cap.release()

# Check if frame was captured
if not ret:
    print("Can't receive frame (stream end?). Exiting ...")
else:
    cv2.imshow("Captured Photo", frame)
    
    # Wait until key is pressed
    cv2.waitKey(0)
    cv2.destroyAllWindows()   
    