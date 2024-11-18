import cv2
import serial

# Arduino ile bağlantı
arduino = serial.Serial('COM3', 9600)

# Kamerayı başlat
camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    if not ret:
        break

    # Nesne algılama
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        center_x = x + w // 2
        center_y = y + h // 2
        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

        # Arduino'ya veri gönder
        data = f"{center_x},{center_y}\n"
        arduino.write(data.encode())

    # Görüntüyü göster
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
