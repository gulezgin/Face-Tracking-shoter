import cv2
import numpy as np
import torch

# YOLO modelini yükle
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Kamera başlat
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO ile algılama
    results = model(frame)
    detections = results.xyxy[0]  # Detaylı sonuçlar

    for *box, conf, cls in detections:
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Hedef merkezini hesapla
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

    # Görüntüyü göster
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
