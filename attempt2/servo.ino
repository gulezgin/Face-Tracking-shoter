#include <Servo.h>

// Servo motorlar için pinler
Servo servoX;
Servo servoY;

int posX = 90; // Başlangıç pozisyonu (X)
int posY = 90; // Başlangıç pozisyonu (Y)

void setup() {
  // Servoları bağla
  servoX.attach(9); // X ekseni için servo pini
  servoY.attach(10); // Y ekseni için servo pini

  // Başlangıç pozisyonları
  servoX.write(posX);
  servoY.write(posY);

  // Seri iletişim başlat
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    // Python'dan gelen veriyi oku
    String data = Serial.readStringUntil('\n');
    
    // Veriyi "X,Y" olarak ayır
    int commaIndex = data.indexOf(',');
    if (commaIndex > 0) {
      String xPart = data.substring(0, commaIndex);
      String yPart = data.substring(commaIndex + 1);
      
      int x = xPart.toInt();
      int y = yPart.toInt();

      // X ve Y'yi servo açılarına dönüştür
      posX = map(x, 0, 640, 0, 180); // 640, kameranın genişliği
      posY = map(y, 0, 480, 0, 180); // 480, kameranın yüksekliği

      // Servo hareketlerini uygula
      servoX.write(posX);
      servoY.write(posY);
    }
  }
}
