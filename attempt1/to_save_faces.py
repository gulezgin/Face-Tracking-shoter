import numpy as np
import cv2

# Fonksiyon: Algılanan yüzün etrafına dikdörtgen çiz
def create_box(a, b, c, d):
    cv2.rectangle(imag, (a, b), (a + c, b + d), (0, 255, 0), 2)

# Fonksiyon: Değişkeni artır
def variable_iteration(l):
    return l + 1

# Dosya isimlendirme için başlangıç numarası
n = 140

# Haar Cascade sınıflandırıcıyı yükle
face_cascade = cv2.CascadeClassifier(r'...haarcascade_frontalface_default.xml')

# Kameradan video akışını başlat
vid = cv2.VideoCapture(0)

while vid.isOpened():
    ret, imag = vid.read()  # Kameradan görüntü oku
    if not ret:
        print("Kameradan görüntü alınamadı.")
        break

    # Yüzleri algıla
    faces = face_cascade.detectMultiScale(
        imag, 
        scaleFactor=1.2, 
        minNeighbors=5, 
        minSize=(10, 10), 
        maxSize=(500, 500)
    )

    # Algılanan her yüz için işlemleri gerçekleştir
    for (x, y, w, h) in faces:
        n = variable_iteration(n)  # İsimlendirme numarasını artır
        create_box(x, y, w, h)     # Algılanan yüzün etrafına kutu çiz
        save_image = imag[y:y+h, x:x+w]  # Yüz kısmını kes
        cv2.imwrite(f"face_{n}.png", save_image)  # Kesilen yüzü kaydet
        print(f"Kaydedilen dosya numarası: {n}")

    # Görüntüyü ekranda göster
    cv2.imshow('Detected Faces', imag)

    # Çıkış için 'ESC' tuşuna basma kontrolü
    k = cv2.waitKey(10)
    if k == 27:  # ESC tuşu
        print("Çıkış yapılıyor.")
        break

# Pencereyi ve video akışını kapat
vid.release()
cv2.destroyAllWindows()
