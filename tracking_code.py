## Bu program, Viola ve Jones algoritmasına dayalı Haar Cascade sınıflandırıcısını kullanır
## Gerçek zamanlı olarak algılanan yüzlerin veritabanını oluşturur
## Kullanılan mikrodenetleyici kartı: "Arduino Uno"

import numpy as np
import cv2
import serial

# Seri iletişim ayarları
ser = serial.Serial(port='COM5', baudrate=9600, timeout=1)

# Servo motoru döndürmek için seri veri gönderme fonksiyonu
def servo_rotate_serialdata(motornum, AngleServo):
    ser.write(chr(255).encode())
    ser.write(chr(motornum).encode())
    ser.write(chr(AngleServo).encode())

# Algılanan yüzün etrafına kutu çizen fonksiyon
def create_box(a, b, c, d):
    cv2.rectangle(imag, (a, b), (a + c, b + d), (0, 255, 0), 2)

# Sayacı artıran fonksiyon
def variable_iteration(l):
    return l + 1

# Algılanan yüz kısmını kaydeden fonksiyon
def write_image():
    face_image = imag[y:y+h, x:x+w]  # Yüz kısmını kes
    cv2.imwrite(f"face_{n}.png", face_image)

# Servo motor açısını kontrol eden fonksiyon
def angle_servo(angle):
    if angle > 230:
        prov = 2  # Servo motoru sağa döndür
        servo_rotate_serialdata(1, prov)
    elif angle < 195:
        prov = 1  # Servo motoru sola döndür
        servo_rotate_serialdata(1, prov)

# Haar Cascade sınıflandırıcıyı yükle
face_cascade = cv2.CascadeClassifier(r'C:\Python27\libs\haarcascade_frontalface_default.xml')

# Video yakalama aygıtını başlat
video_capture = cv2.VideoCapture(0)

# Dosya isimlendirme için başlangıç numarası
n = 0

while video_capture.isOpened():
    ret, imag = video_capture.read()
    if not ret:
        print("Kameradan görüntü alınamadı. Program sonlandırılıyor.")
        break

    # Yüz algılama
    faces = face_cascade.detectMultiScale(
        imag, 
        scaleFactor=1.2, 
        minNeighbors=5, 
        minSize=(10, 10), 
        maxSize=(500, 500)
    )

    # Algılanan her yüz için işlemler
    for (x, y, w, h) in faces:
        create_box(x, y, w, h)       # Kutuyu çiz
        n = variable_iteration(n)   # Sayacı artır

        # Eğer algılanan yüzlerin kaydedilmesi isteniyorsa, aşağıdaki satırı aktif edin
        # write_image()

        # Servo motor açısını kontrol etmek için fonksiyonu çağır
        angle_servo(x)

    # Görüntüyü ekranda göster
    cv2.imshow('Detected Faces', imag)

    # Çıkış için 'ESC' tuşu kontrolü
    k = cv2.waitKey(10)
    if k == 27:  # ESC tuşu
        print("Program sonlandırılıyor.")
        break

# Kaynakları serbest bırak ve pencereleri kapat
video_capture.release()
cv2.destroyAllWindows()
