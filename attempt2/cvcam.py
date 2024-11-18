import cv2
import serial
import time

# Arduino ile seri iletişim başlat
arduino = serial.Serial('COM3', 9600)  # COM portunu kendi sisteminize göre değiştirin
time.sleep(2)  # Arduino'nun başlaması için bekleme süresi

# OpenCV Haar Cascade yüz tanıma modeli yükle
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Kamerayı başlat
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Görüntüyü gri tona çevir
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Yüzleri tespit et
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Yüzün merkez koordinatlarını hesapla
        center_x = x + w // 2
        center_y = y + h // 2

        # Görüntüye yüz çevresi ve merkez noktası ekle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

        # Arduino'ya koordinatları gönder
        coords = f"{center_x},{center_y}\n"
        arduino.write(coords.encode('utf-8'))

        # Sadece bir yüz için işlem yap
        break

    # Kamerada "TARGET LOCKED" yazısını ekrana bas
    cv2.putText(frame, "TARGET LOCKED", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Görüntüyü göster
    cv2.imshow("Face Tracking", frame)

    # 'q' tuşuna basarak çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Temizlik işlemleri
cap.release()
cv2.destroyAllWindows()
arduino.close()
