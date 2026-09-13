import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")

# 0 = laptop webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Camera could not be opened.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("ERROR: Could not read camera.")
        break

    # Run YOLO detection
    results = model(frame, conf=0.5)

    # Draw detections
    annotated_frame = results[0].plot()

    cv2.imshow("AI Border Surveillance - YOLO Detection", annotated_frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()