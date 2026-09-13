import cv2
from ultralytics import YOLO
import numpy as np
from datetime import datetime

# Load YOLO model
model = YOLO("yolo11n.pt")

# Store which people have already generated an alert
last_alert_time = {}

# Open camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera could not be opened.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Could not read camera.")
        break

    # Reduce resolution
    frame = cv2.resize(frame, (640, 480))

    # Restricted zone
    zone = np.array([
        (180, 120),
        (500, 120),
        (560, 420),
        (120, 420)
    ], np.int32)

    # Draw restricted zone
    cv2.polylines(
        frame,
        [zone],
        True,
        (0, 0, 255),
        2
    )

    cv2.putText(
        frame,
        "RESTRICTED ZONE",
        (180, 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2
    )

    intrusion = False

    # YOLO tracking
    results = model.track(
        frame,
        persist=True,
        conf=0.5,
        classes=[0],
        verbose=False
    )

    if results[0].boxes is not None:

        boxes = results[0].boxes

        for i, box in enumerate(boxes):

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            # Get tracking ID
            if box.id is not None:
                track_id = int(box.id[0])
            else:
                track_id = i + 1

            # Person center
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            # Check whether person is inside restricted zone
            inside = cv2.pointPolygonTest(
                zone,
                (center_x, center_y),
                False
            )

            if inside >= 0:
                intrusion = True

                current_time = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                # Create alert only once for each person
                if track_id not in last_alert_time:

                    print(
                        f"INTRUSION: Person ID {track_id} "
                        f"at {current_time}"
                    )

                    with open("alerts.txt", "a") as log:
                        log.write(
                            f"INTRUSION | Person ID: "
                            f"{track_id} | Time: "
                            f"{current_time}\n"
                        )

                    last_alert_time[track_id] = current_time

            # Draw person box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # Display person ID
            cv2.putText(
                frame,
                f"Person ID: {track_id}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            # Draw center point
            cv2.circle(
                frame,
                (center_x, center_y),
                5,
                (255, 0, 0),
                -1
            )

    # Display status
    if intrusion:

        cv2.putText(
            frame,
            "!!! INTRUSION DETECTED !!!",
            (80, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 255),
            3
        )

    else:

        cv2.putText(
            frame,
            "STATUS: NORMAL",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    # Show camera
    cv2.imshow(
        "AI Border Surveillance",
        frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()